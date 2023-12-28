import subprocess
import time
import json
import re
import logging
from urllib.parse import urlparse
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

PATH = '/var/lib/docker/containers/be6e3c97605f2c3f49e9eb3e7773c0d22956f4a5f9352a23a62dc05edfbcfdc1/be6e3c97605f2c3f49e9eb3e7773c0d22956f4a5f9352a23a62dc05edfbcfdc1-json.log'

KEY_EVENTS = [
    'generating proof',
    'created poet client',
    'Found proof for nonce',
    'stored poet proof',
    'calculating proof of work',
    'selected the best proof',
    'poet response received',
    'awaiting atx publication epoch',
    'atx published',
    'building new atx challenge',
    'atx challenge is ready',
    'verifying the initial post',
    'loaded the initial post from disk',
    'post setup completed',
    'got poet proof',
    'Proof is invalid: numunits too large',
    'challenge submitted to poet proving service',
    'proposal eligibilities for an epoch',
    'proposalBuilder started',
    'proposal created',
    'Failed to generate proof',
    "can't recover tortoise state"
]

POET_ENDPOINTS = [
    {'endpoint': 'proofs', 'exp': 'Getting PoET Proof'},
    {'endpoint': 'pow_params', 'exp': 'Getting PoET PoW Params'},
    {'endpoint': 'submit', 'exp': 'Submitting PoST Proof'},
    {'endpoint': 'info', 'exp': 'Getting PoET Info'}
]
def extract_json_from_string(input_string):
    # Define a regular expression pattern to match JSON
    json_pattern = r'({.*})'

    # Search for the pattern in the input string
    match = re.search(json_pattern, input_string)

    if match:
        # Extract and return the JSON object
        json_string = match.group(1)
        return json.loads(json_string)
    else:
        # Return None if no JSON object is found
        return None
    
def check_for_key_event(log):
    # print(log)
    event = None
    if KEY_EVENTS[0] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Node has begun generating proof.'
        }
    
    if KEY_EVENTS[1] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'PoET Client Created for {json_part["url"]} with max retries of {json_part["max retries"]} and a retry wait between {json_part["min retry wait"]} and {json_part["max retry wait"]}'
        }

    if KEY_EVENTS[2] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Node has Found Proof!'
        }

    if KEY_EVENTS[3] in log[2]:
        json_part = extract_json_from_string(log[2])

        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Successfully Stored PoET Proof for Epoch {json_part["round_id"]} with ID {json_part["poet_proof_id"]}'
        }

    if KEY_EVENTS[4] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Proofing has started!'
        }
        

    if KEY_EVENTS[5] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Select Best Proof from List of PoETs. Leaf Count: {json_part["leafCount"]}'
        }
        

    if KEY_EVENTS[6] in log[2]:
        json_part = extract_json_from_string(log[2])
        action = None
        for i in POET_ENDPOINTS:
            if i['endpoint'] in json_part["url"]:
                action = i['exp']

        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Received Status "{json_part["status"]}" Response While "{action}" from "{json_part["url"]}"'
        }

    if KEY_EVENTS[7] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Waiting to Publish ATX for Epoch {json_part["pub_epoch"]}'
        }
    
    if KEY_EVENTS[8] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'ATX Published by {json_part["node_id"]} in Epoch {json_part["epoch"]} with {json_part["num_units"]} Num Units for Reward Address {json_part["coinbase"]}'
        }

    if KEY_EVENTS[9] in log[2]:
        event = None

    if KEY_EVENTS[10] in log[2]:
        json_part = extract_json_from_string(log[2])
        
        if json_part["current_epoch"] == json_part["publish_epoch"]:
            message = f'ATX Challenge is Ready and Was Published in Epoch {json_part["publish_epoch"]}'
        else:
            message = f'ATX Challenge is Ready and Will be Published in Epoch {json_part["publish_epoch"]}'
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': message
        }

    if KEY_EVENTS[11] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Verifying Initial PoST'
        }

    if KEY_EVENTS[12] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Loaded the Initial PoST from Disk'
        }

    if KEY_EVENTS[13] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'PoST Setup Complete for PoST in Dir {json_part["data_dir"]} with {json_part["num_units"]} Num Units'
        }

    if KEY_EVENTS[14] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Got PoET Proof with Leaf Count of {json_part["leaf count"]}'
        }

    if KEY_EVENTS[15] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Num Units Mismatch! Try redownloading libpost.so from the release for your go-spacemesh version.'
        }

    if KEY_EVENTS[16] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Challenge Submitted to PoET Proving Service for Epoch {json_part["round"]} on PoET {json_part["poet_id"]}'
        }

    if KEY_EVENTS[17] in log[2]:
        json_part = extract_json_from_string(log[2])

        layers = [entry["layer"] for entry in json_part["eligible by layer"] for _ in range(entry["slots"])]

        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Got {json_part["eligible"]} Proposal Eligibilities for Epoch {json_part["epoch"]} with a Weight of {json_part["weight"]} Layers: {layers}'
        }

    if KEY_EVENTS[18] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Proposal Builder Started'
        }

    if KEY_EVENTS[19] in log[2]:
        json_part = extract_json_from_string(log[2])
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': f'Proposal Created for Layer {json_part["layer_id"]} in Epoch {json_part["epoch_id"]} with a latency of {json_part["latency"]["total"]}'
        }

    if KEY_EVENTS[20] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': 'Failed to Generate Proof!'
        }

    if KEY_EVENTS[21] in log[2]:
        event = {
            'timestamp': log[0],
            'level': log[1],
            'o_log': log[2],
            'parsed': "Can't recover tortoise state. Try replacing state.sql file as DB is likely corrupt."
        }
        #print(f'{event["timestamp"]}: {event["parsed"]}')

    return event

def parse_log(log):
    log_pattern = re.compile(r'(?P<timestamp>\S+)\s+(?P<level>\S+)\s+(?P<message>.+)')
    json_log = json.loads(log.strip())['log']
    match = log_pattern.match(json_log)

    if match:
        timestamp_str = match.group('timestamp')
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%b %d, %Y %I:%M %p")
        level = match.group('level')
        message = ' '.join(match.group('message').split())

        log_entry = [timestamp, level, message]
        return log_entry
    
    return None

def parse_new_logs():
    with subprocess.Popen(['tail', '-n', '0', '-F', PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    log = parse_log(line)
                    event = check_for_key_event(log)
                    if event:
                        print(event)


                time.sleep(0.1)
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C) to gracefully exit the script
            print("Exiting...")

def parse_logs():
    with open(PATH, 'r') as file:
        for line in file:
            log = parse_log(line)
            event = check_for_key_event(log)

            if event:
                event_text = f'{event["timestamp"]}: {event["parsed"]}'
                if event['level'] == 'INFO':
                    logging.info(event_text)
                elif event['level'] == 'ERROR' or event['level'] == 'FATAL':
                    logging.error(event_text)
                else:
                    logging.info(event_text)



if __name__ == "__main__":

    # Read existing logs
    print("Existing Logs:")
    parse_logs()

    # Watch for new logs
    print("\nWatching for New Logs:")
    #parse_new_logs()

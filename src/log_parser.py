import src.constants as constants
from src.utils import Utils
import json
import re
import traceback
from datetime import datetime
from src.logger import logger

class LOGPARSER:
    @staticmethod
    def get_event(log):
        print(log)

    def transform_log(log):
        try:
            log_pattern = re.compile(r'(?P<timestamp>\S+)\s+(?P<level>\S+)\s+(?P<message>.+)')

            match = log_pattern.match(log)

            if match:
                timestamp_str = match.group('timestamp')
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%b %d, %Y %I:%M %p")
                level = match.group('level')
                message = ' '.join(match.group('message').split())

                log_entry = [timestamp, level, message]
                return log_entry
            
        except ValueError as e:
            logger.error(f'Error handling log: {log}')
                        # Log the exception type and message
            logger.error(f"Exception type: {type(e).__name__}, Message: {str(e)}")

            # Log the traceback information
            traceback_info = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_info}")
            
        except Exception as e:
            logger.error(f'Error handling log: {log}')
                        # Log the exception type and message
            logger.error(f"Exception type: {type(e).__name__}, Message: {str(e)}")

            # Log the traceback information
            traceback_info = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_info}")

        return None
    
    @staticmethod
    def check_for_key_event(log, name):
        if not log:
            return None
        
        event = None
        if constants.KEY_EVENTS[0] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Node has begun generating proof.'
            }
        
        if constants.KEY_EVENTS[1] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'PoET Client Created for {json_part["url"]} with max retries of {json_part["max retries"]} and a retry wait between {json_part["min retry wait"]} and {json_part["max retry wait"]}'
            }

        if constants.KEY_EVENTS[2] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Node has Found Proof!'
            }

        if constants.KEY_EVENTS[3] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])

            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Successfully Stored PoET Proof for Epoch {json_part["round_id"]} with ID {json_part["poet_proof_id"]}'
            }

        if constants.KEY_EVENTS[4] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Proofing has started!'
            }
            

        if constants.KEY_EVENTS[5] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Select Best Proof from List of PoETs. Leaf Count: {json_part["leafCount"]}'
            }
            

        if constants.KEY_EVENTS[6] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            action = None
            for i in constants.POET_ENDPOINTS:
                if i['endpoint'] in json_part["url"]:
                    action = i['exp']

            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Received Status "{json_part["status"]}" Response While "{action}" from "{json_part["url"]}"'
            }

        if constants.KEY_EVENTS[7] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Waiting to Publish ATX for Epoch {json_part["pub_epoch"]}'
            }
        
        if constants.KEY_EVENTS[8] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'ATX Published by {json_part["node_id"]} in Epoch {json_part["epoch"]} with {json_part["num_units"]} Num Units for Reward Address {json_part["coinbase"]}'
            }

        if constants.KEY_EVENTS[9] in log[2]:
            event = None

        if constants.KEY_EVENTS[10] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            
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

        if constants.KEY_EVENTS[11] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Verifying Initial PoST'
            }

        if constants.KEY_EVENTS[12] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Loaded the Initial PoST from Disk'
            }

        if constants.KEY_EVENTS[13] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'PoST Setup Complete for PoST in Dir {json_part["data_dir"]} with {json_part["num_units"]} Num Units'
            }

        if constants.KEY_EVENTS[14] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Got PoET Proof with Leaf Count of {json_part["leaf count"]}'
            }

        if constants.KEY_EVENTS[15] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Num Units Mismatch! Try redownloading libpost.so from the release for your go-spacemesh version.'
            }

        if constants.KEY_EVENTS[16] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Challenge Submitted to PoET Proving Service for Epoch {json_part["round"]} on PoET {json_part["poet_id"]}'
            }

        if constants.KEY_EVENTS[17] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])

            layers = [entry["layer"] for entry in json_part["eligible by layer"] for _ in range(entry["slots"])]

            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Got {json_part["eligible"]} Proposal Eligibilities for Epoch {json_part["epoch"]} with a Weight of {json_part["weight"]} Layers: {layers}'
            }

        if constants.KEY_EVENTS[18] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Proposal Builder Started'
            }

        if constants.KEY_EVENTS[19] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f'Proposal Created for Layer {json_part["layer_id"]} in Epoch {json_part["epoch_id"]} with a latency of {json_part["latency"]["total"]}'
            }

        if constants.KEY_EVENTS[20] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': 'Failed to Generate Proof!'
            }

        if constants.KEY_EVENTS[21] in log[2]:
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': "Can't recover tortoise state. Try replacing state.sql file as DB is likely corrupt."
            }

        if constants.KEY_EVENTS[22] in log[2]:
            pattern = r"v\d+\.\d+\.\d+"
            match = re.search(pattern, log[2])
            if match:
                version = match.group()
            else:
                version = "Version Not Found"
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f"Spacemesh App Version {version}"
            }

        if constants.KEY_EVENTS[23] in log[2]:
            json_part = Utils.extract_json_from_string(log[2])
            event = {
                'timestamp': log[0],
                'level': log[1],
                'o_log': log[2],
                'parsed': f"Starting Spacemesh using data-dir {json_part.get('data-dir')} and post-dir {json_part.get('post-dir')}"
            }
            #print(f'{event["timestamp"]}: {event["parsed"]}')
        
        if event:
            event['name'] = name

        return event

import subprocess
import time
import json
import re
import argparse

import src.constants as constants
from urllib.parse import urlparse
from datetime import datetime
import traceback
from src.logger import logger
from src.utils import Utils

def parse_log(log):
    pass

def parse_default_log(log_entry):
    log_path = log_entry['log_path']

    with open(log_path, 'r') as file:
        for raw_log in file:
            try:
                parse_log(raw_log)

            except Exception as e:
                pass


def parse_docker_log(log_entry):
    logger.info(log_entry)

def parse_old_logs(config):
    for log_entry in config['logs']:

        if log_entry['log_type'] == 'default':
            parse_default_log(log_entry)
        elif log_entry['log_type'] == 'docker':
            parse_default_log(log_entry)
        else:
            logger.error(f"Unknown log type: {log_entry['log_type']}")

def run(config):
    parse_old_logs(config)

def main():
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    parser.add_argument("-c", "--config", help="Path to a config file", type=str)
    parser.add_argument("-l", "--logs", help="Path to logs", type=str, required=False)
    parser.add_argument("-t", "--type", help="Type of logs", type=str, required=False)
    parser.add_argument("-o", "--output", help="Path to Output Logs", type=str, required=False)

    args = parser.parse_args()

    if args.config:
        config = Utils.read_yaml_file(args.config)
    else:
        if not args.logs or not args.type:
            parser.error("-d (data directory) and -t (type of logs) are required if -c (config) is not provided.")
    
        config = {
            'logs': [
                {
                    'name': 'node01',
                    'log_path': args.logs,
                    'log_type': args.type
                }
            ]
        }

    run(config)


if __name__ == "__main__":
    main()











    

# def parse_log(log):
#     try:
#         log_pattern = re.compile(r'(?P<timestamp>\S+)\s+(?P<level>\S+)\s+(?P<message>.+)')
#         json_log = json.loads(log.strip())['log']
#         match = log_pattern.match(json_log)

#         if match:
#             timestamp_str = match.group('timestamp')
#             timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%b %d, %Y %I:%M %p")
#             level = match.group('level')
#             message = ' '.join(match.group('message').split())

#             log_entry = [timestamp, level, message]
#             return log_entry
        
#     except ValueError as e:
#         return None
        
#     except Exception as e:
#         logging.error(f'Error handling log: {log}')
#                     # Log the exception type and message
#         logging.error(f"Exception type: {type(e).__name__}, Message: {str(e)}")

#         # Log the traceback information
#         traceback_info = traceback.format_exc()
#         logging.error(f"Traceback:\n{traceback_info}")

#     return None

# def parse_new_logs():
#     with subprocess.Popen(['tail', '-n', '0', '-F', PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
#         try:
#             while True:
#                 line = process.stdout.readline()
#                 if line:
#                     log = parse_log(line)
#                     event = check_for_key_event(log)
#                     if event:
#                         print(event)


#                 time.sleep(0.1)
#         except KeyboardInterrupt:
#             # Handle keyboard interrupt (Ctrl+C) to gracefully exit the script
#             print("Exiting...")

# def parse_logs():
#     with open(PATH, 'r') as file:
#         for line in file:
#             try:

#                 log = parse_log(line)
#                 event = check_for_key_event(log)

#                 if event:
#                     event_text = f'{event["timestamp"]}: {event["parsed"]}'
#                     if event['level'] == 'INFO':
#                         logging.info(event_text)
#                     elif event['level'] == 'ERROR' or event['level'] == 'FATAL':
#                         logging.error(event_text)
#                     else:
#                         logging.info(event_text)

#             except Exception as e:
#                 logging.error(f'Error handling log: {log}')
#                             # Log the exception type and message
#                 logging.error(f"Exception type: {type(e).__name__}, Message: {str(e)}")

#                 # Log the traceback information
#                 traceback_info = traceback.format_exc()
#                 logging.error(f"Traceback:\n{traceback_info}")


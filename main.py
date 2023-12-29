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
from src.log_parser import LOGPARSER

def parse_log(log_entry):
    log_path, log_type, name = log_entry['log_path'], log_entry['log_type'], log_entry['name']
    
    events = []
    with open(log_path, 'r') as file:
        logs = []
        for raw_log in file:
            logs.append(raw_log)


        for log in logs:
            try:
                if log_type == 'Docker':
                    log = json.loads(log.strip())['log']

                t_log = LOGPARSER.transform_log(log)
                event = LOGPARSER.check_for_key_event(t_log, name)

                if event:
                    events.append(event)


            except Exception as e:
                logger.error(f'Error handling log: {log}')
                            # Log the exception type and message
                logger.error(f"Exception type: {type(e).__name__}, Message: {str(e)}")

                # Log the traceback information
                traceback_info = traceback.format_exc()
                logger.error(f"Traceback:\n{traceback_info}")

    return events


def parse_old_logs(config):
    old_logs = []
    for log_entry in config['logs']:
        old_log = parse_log(log_entry)
        old_logs.extend(old_log)

    return old_logs


def run(config):
    logger.info('Parsing Old Logs')
    old_logs = parse_old_logs(config)

    for log in old_logs:
        logger.info(f"{log['timestamp']} [{log['name']}]: {log['parsed']}")

    if config['output']:
        logger.info(old_logs[0])
        logger.info(f"Storing logs at {config['output']}")
        Utils.write_log(old_logs, config['output'])

def main():
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    parser.add_argument("-c", "--config", help="Path to a config file", type=str)
    parser.add_argument("-l", "--logs", help="Path to logs", type=str, required=False)
    parser.add_argument("-t", "--type", help="Type of logs", type=str, required=False)
    parser.add_argument("-o", "--output", help="Path to Output Logs", type=str, required=False)

    args = parser.parse_args()

    if args.config:
        config = Utils.read_yaml_file(args.config)
        logger.info(f"Imported Config: {config}")
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


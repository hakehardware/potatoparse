import subprocess
import time
import json
import re
import argparse
import os

import src.constants as constants
from urllib.parse import urlparse
from datetime import datetime
import traceback
from src.logger import logger
from src.utils import Utils
from src.log_parser import LOGPARSER
from time import sleep

def watch_logs(config):
    logger.info('Watching for new log files...')
    last_sizes = {file_path['log_path']: 0 for file_path in config['logs']}
    logs = []
    current_time = datetime.now().timestamp() * 1000

    try:
        count = 0
        while True:
            # Holds temporary logs for all nodes each iteration that then gets sorted.
            temp_logs = []

            # Iterate through each log file
            for log_entry in config['logs']:

                # Deconstruct the log_entry data
                log_path, log_type, name = log_entry['log_path'], log_entry['log_type'], log_entry['name']

                # Get the current size so we can compare with previous size.
                current_size = os.path.getsize(log_path)

                # Check that the size has grown
                if current_size > last_sizes[log_path]:

                    # Open the file
                    with open(log_path, 'r') as file:

                        # Move to the location of the new data
                        file.seek(last_sizes[log_path])

                        # For each new line, check for key events
                        for log in file:

                            try:

                                # If it's docker, we first need to get the actual log file from the JSON
                                if log_type == 'Docker':
                                    log = json.loads(log.strip())['log']

                                # Transform the log, then check it for 
                                t_log = LOGPARSER.transform_log(log)
                                event = LOGPARSER.check_for_key_event(t_log, name)

                                # If there was an event, append it to temp logs
                                if event:
                                    temp_logs.append(event)
                                    count = 0 # Reset the count to 0

                            except ValueError as e:
                                pass
            
                    last_sizes[log_path] = current_size
            
            # Add one to the count
            count = count + 1

            # Periodically print watching logs to screen
            if count > 300:
                logger.info('Watching logs...')
                count = 0

            temp_logs = sorted(temp_logs, key=lambda x: x['timestamp'])
            for log in temp_logs:
                logger.info(f'{log["timestamp"]} - [{log["name"]}]: {log["parsed"]}')
                if config.get('output', None):
                    Utils.write_key_event_to_csv(log, config['output'], current_time)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopped watching log files.")
        return logs

def run(config):
    logger.info('Parsing Old Logs')
    watch_logs(config)

    

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


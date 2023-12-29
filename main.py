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

def parse_log(log_entry):
    log_path, log_type, name = log_entry['log_path'], log_entry['log_type'], log_entry['name']
    
    events = []
    with open(log_path, 'r', encoding='utf-8') as file:

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

def watch_logs(config):
    logger.info('Watching for new log files...')
    last_sizes = {file_path['log_path']: 0 for file_path in config['logs']}
    logs = []

    try:
        count = 0
        while True:
            for log_entry in config['logs']:
                log_path, log_type, name = log_entry['log_path'], log_entry['log_type'], log_entry['name']

                current_size = os.path.getsize(log_path)
                if current_size > last_sizes[log_path]:
                    with open(log_path, 'r') as file:
                        file.seek(last_sizes[log_path])
                        for log in file:
                            try:
                                if log_type == 'Docker':
                                    log = json.loads(log.strip())['log']

                                t_log = LOGPARSER.transform_log(log)
                                event = LOGPARSER.check_for_key_event(t_log, name)
                                
                                if event:
                                    logger.info(f"{event['timestamp']} [{event['name']}]: {event['parsed']}")
                                    count = 0
                            except ValueError as e:
                                pass

                    last_sizes[log_path] = current_size
            count = count + 1

            if count > 10:
                logger.info('Watching logs...')
                count = 0

            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped watching log files.")
        return logs
    
    try:
        while True:
            for log in config['logs']:
                log_path = log['log_path']
                
                current_size = os.path.getsize(log_path)
                if current_size > last_sizes[log_path]:
                    with open(log_path, 'r') as file:
                        file.seek(last_sizes[log_path])
                        new_content = file.read()
                        for log in new_content:
                            logger.info(f"New Content: {new_content}")
                        # print(f"Updates in {log_path}:")
                        # print(file.read())
                    last_sizes[log_path] = current_size
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped watching log files.")



    # tail_processes = []
    # log_types = []
    # names = []

    #tail_process = subprocess.Popen(['tail', '-f', config['logs'][0]['log_path']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # try:
    #     while True:
    #         # Read a line from the tail process
    #         line = tail_process.stdout.readline()
    #         if not line:
    #             break  # Exit the loop when the tail process ends (e.g., when you stop the script)
    #         print(line.strip())  # Print the log entry

    # for log_entry in config['logs']:
    #     log_path, log_type, name = log_entry['log_path'], log_entry['log_type'], log_entry['name']
    #     log_types.append(log_type)
    #     logger.info(f"{log_path}")
    #     tail_process = subprocess.Popen(['tail', '-f', log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #     tail_processes.append(tail_process)

    # logger.info('Looping through subprocesses')
    # try:
    #     count = 0
    #     while True:
    #         for process, name, log_type in zip(tail_processes, names, log_types):
    #             # Read a line from the tail process
    #             log = process.stdout.readline()
    #             if not log:
    #                 break
    #             logger.info(log)

                #if log:
                    # if log_type == 'Docker':
                    #     log = json.loads(log.strip())['log']

                    # t_log = LOGPARSER.transform_log(log)
                    # event = LOGPARSER.check_for_key_event(t_log, name)

                    # if event:
                    #     logger.info(f"{log['timestamp']} [{name}]: {log['parsed']}")
                    #     count = 0

                    #logger.info(log)

            # sleep(0.1)

            # if count > 1000:
            #     logger.info('Watching for logs.')
            #     count = 0

            # count = count + 1

    # except KeyboardInterrupt:
    #     # Handle Ctrl+C to stop tailing the log files
    #     for process in tail_processes:
    #         process.terminate()

def parse_old_logs(config):
    old_logs = []
    for log_entry in config['logs']:
        old_log = parse_log(log_entry)
        old_logs.extend(old_log)

    return old_logs


def run(config):
    logger.info('Parsing Old Logs')
    # old_logs = parse_old_logs(config)
    # sorted_data = sorted(old_logs, key=lambda x: x['timestamp'])

    # logger.info(f"Got {len(sorted_data)} logs")
    # for log in sorted_data:
    #     logger.info(f"{log['timestamp']} [{log['name']}]: {log['parsed']}")

    # if config.get('output', None):
    #     logger.info(f"Storing logs at {config['output']}")
    #     Utils.write_log(sorted_data, config['output'])

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


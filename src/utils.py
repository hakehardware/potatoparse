import yaml
import os
import re
import json

from src.logger import logger

class Utils:
    @staticmethod
    def read_yaml_file(file_path):
        logger.info(f'Opening config from {file_path}')
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")

    @staticmethod
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
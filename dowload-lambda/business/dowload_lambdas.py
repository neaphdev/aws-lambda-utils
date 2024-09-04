import json
import logging
import time
from pathlib import Path

import boto3
import requests

CURRENT_FILE_PATH = Path(__file__).resolve()


def download_lambda_function(
    function_name: str,
    output_file: str,
    profile_name: str = "bdev",
) -> bool:
    try:
        # if downloads folder does not exist, create it

        # Create a session with the specified profile, if provided
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()

        # Initialize a session using Amazon Lambda in a specific region
        client = session.client(
            "lambda", region_name="us-east-1"
        )  # Ensure this is the same region as your Lambda function

        # Get the function's code
        response = client.get_function(FunctionName=function_name)

        # Get the URL for the function's code
        code_url = response["Code"]["Location"]

        # Get the absolute path of the current file

        # Define the output file path using pathlib
        output_file_path = (CURRENT_FILE_PATH.parent / "downloads" / f"{output_file}.zip").resolve()

        # Download the ZIP file from the URL
        with requests.get(code_url) as r:
            r.raise_for_status()
            with open(output_file_path, "wb") as f:
                f.write(r.content)

        logging.info(f"Lambda function {function_name} has been downloaded as {output_file_path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False


def dowload_lambdas_by_json_list_lambdas(json_file: str, profile_name: str = "bdev") -> bool:
    try:
        json_file_list = (CURRENT_FILE_PATH.parent / "downloads" / f"{json_file}").resolve()
        with open(json_file_list, "r") as f:
            lambdas = json.load(f)

        for lambda_function in lambdas:
            function_name = lambda_function["FunctionName"]

            success = download_lambda_function(
                function_name,
                function_name,
                profile_name,
            )
            time.sleep(0.1)
            if not success:
                print(f"Failed to download {function_name}")
            else:
                print(f"Downloaded {function_name}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


# Example usage
if __name__ == "__main__":

    function_name = "MyNodeJs20Function"
    output_file = f"downloads/{function_name}.zip"
    profile_name = None  # Replace with your AWS profile name
    # download_lambda_function(function_name, output_file, profile_name)
    file_name = "lambdas-20240904-1522"
    profile_name = "mid-nc-dev-developer"
    profile_name = "bdev"
    dowload_lambdas_by_json_list_lambdas(f"{file_name}.json", profile_name)

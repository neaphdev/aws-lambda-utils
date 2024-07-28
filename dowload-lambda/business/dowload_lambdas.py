import logging
from pathlib import Path

import boto3
import requests

current_file_path = Path(__file__).resolve()


def download_lambda_function(
    function_name: str,
    output_file: str,
    profile_name: str = None,
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
        output_file_path = (
            current_file_path.parent / "downloads" / f"{output_file}.zip"
        ).resolve()

        # Download the ZIP file from the URL
        with requests.get(code_url) as r:
            r.raise_for_status()
            with open(output_file_path, "wb") as f:
                f.write(r.content)

        logging.info(
            f"Lambda function {function_name} has been downloaded as {output_file_path}"
        )
        return True
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False


# Example usage
if __name__ == "__main__":
    function_name = "MyNodeJs20Function"
    output_file = f"downloads/{function_name}.zip"
    profile_name = None  # Replace with your AWS profile name
    download_lambda_function(function_name, output_file, profile_name)

# aws lambda list-functions --region <region-name> --output json > lambdas.json

# list all lambdas and save in json file
# aws lambda list-functions --region us-east-1 --output json > lambdas.json
import json
import logging
from pathlib import Path

import boto3
import pandas as pd

current_file_path = Path(__file__).resolve()


def list_functions(client):
    functions = []
    response = client.list_functions()

    while "NextMarker" in response:
        functions.extend(response["Functions"])
        response = client.list_functions(Marker=response["NextMarker"])

    functions.extend(response["Functions"])
    return functions


def list_lambdas(profile: str = "bdev"):
    try:
        # Create a session with the specified profile, if provided
        if profile:
            session = boto3.Session(profile_name=profile)
        else:
            session = boto3.Session()

        # Initialize a session using Amazon Lambda in a specific region
        client = session.client(
            "lambda", region_name="us-east-1"
        )  # Ensure this is the same region as your Lambda function

        # Get the function's code
        response = list_functions(client)

        # Get the URL for the function's code
        lambdas = response

        # Get the absolute path of the current file

        # Define the output file path using pathlib
        date = pd.Timestamp.today().strftime("%Y%m%d-%H%M")
        output_file_path = (
            current_file_path.parent / "downloads" / f"lambdas-{date}.json"
        ).resolve()

        # Download the ZIP file from the URL
        with open(output_file_path, "w") as f:
            json.dump(lambdas, f)

        logging.info(f"Lambda functions have been downloaded as {output_file_path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    profile = "mid-nc-dev-developer"
    profile = "bdev"
    logging.info(f"Listing lambdas with profile {profile} ....")
    list_lambdas(profile=profile)
    logging.info(f"Lambdas listed successfully")

import json
import logging
import subprocess
from pathlib import Path

import pandas as pd

current_file_path = Path(__file__).resolve()


def list_eventbridge_rules(profile: str = "bdev"):
    try:
        # Define the AWS CLI command
        command = [
            "aws",
            "events",
            "list-rules",
            "--event-bus-name",
            "default",
            "--region",
            "us-east-1",
            "--profile",
            profile,
            "--output",
            "json",
        ]

        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        rules = json.loads(result.stdout)

        # Get the absolute path of the current file
        date = pd.Timestamp.today().strftime("%Y%m%d-%H%M")
        output_file_path = (
            current_file_path.parent / "dowloads_list" / f"eventbridge-rules-{date}.json"
        ).resolve()

        # Save the rules to a JSON file
        with open(output_file_path, "w") as f:
            json.dump(rules, f)

        logging.info(f"EventBridge rules have been downloaded as {output_file_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while executing the AWS CLI command: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    profile = "bdev"
    logging.info(f"Listing EventBridge rules with profile {profile} ....")
    list_eventbridge_rules(profile=profile)
    logging.info(f"EventBridge rules listed successfully")

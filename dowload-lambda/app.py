import json
import logging
from pathlib import Path

import pandas as pd
from business.dowload_lambdas import download_lambda_function
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/download-lambdas", methods=["POST"])
def download_lambdas():
    try:
        if "file" not in request.files:
            raise RuntimeError("No file found")
        file = request.files["file"]
        # if user does not select file, browser also

        # submit an empty part without filename
        if file.filename == "":
            return json.dumps({"error": "No selected file"}), 400
        # Read file and convert it to pandas dataframe
        save_file_log = False
        df = None
        if file and save_file_log:
            df = pd.read_csv(file, header=None)
            df = df.fillna("")
            date_today_str = pd.Timestamp.today().strftime("%Y%m%d-%H%M")
            current_file_path = Path(__file__).resolve().parent
            name_date = f"business/downloads/DOWLOAD_LAMBDA_{date_today_str}.csv"
            output_file_path = (current_file_path / name_date).resolve()

        # download_lambda_functions
        dowload_status = []
        print("PANDAS ", df)
        for index, row in df.iterrows():
            print("ROW", row[0])
            function_name = row[0]
            success = download_lambda_function(function_name, function_name)
            dowload_status.append({"name": function_name, "success": success})

        logging.info(f"Lambda functions have been downloaded as {output_file_path}")
        print(dowload_status)
        df.to_csv(output_file_path, index=False)
        return json.dumps(dowload_status), 200
    except Exception as e:
        logging.exception("Error trying to download", e)
        return json.dumps({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

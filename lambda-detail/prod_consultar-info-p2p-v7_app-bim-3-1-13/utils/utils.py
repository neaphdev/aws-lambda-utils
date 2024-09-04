
import boto3
import json
import config as cfg


def invoke_lambda(arn_lambda, payload):
    try:
        invokeLam = boto3.client("lambda", region_name=cfg.region_arn)
        resp = invokeLam.invoke(
            FunctionName=arn_lambda, InvocationType="RequestResponse", Payload=json.dumps(payload))
        res_json = json.loads(resp['Payload'].read().decode("utf-8"))
        return res_json
    except Exception as e:
        print('Error',e)
        raise Exception("ERROR", e)
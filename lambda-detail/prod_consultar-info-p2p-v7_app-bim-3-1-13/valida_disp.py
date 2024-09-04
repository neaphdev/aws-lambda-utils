import json
import boto3
from config import arn_valida_disp

import pytz
tz = pytz.timezone('America/Lima')
import database.dynamodb_custom as dyn
from datetime import datetime,timedelta
import config as cfg

class ValidaDisp:

    def __init__(self):
        super().__init__()

    def valida_disp(self, traza, auth):
        try:
            invoke_lambda = boto3.client(
                "lambda", region_name="us-east-1")
            payload = {
                "traza_app": traza,
                "auth": auth
            }
            
            arn_lambda = arn_valida_disp
            resp = invoke_lambda.invoke(
                FunctionName=arn_lambda, InvocationType="RequestResponse", Payload=json.dumps(payload))
            print(resp)
            res_json = json.loads(resp['Payload'].read().decode("utf-8"))
            print('Response valida disp:', res_json)

            if res_json['code']==200:
                return True
            else:
                return False
        except Exception as e:
            print('Erroe valida_disp:', e)
            return False

    def session_validate(self, msisdn):
        dyn_obj = dyn.DynamoBD(table=cfg.table_db_session)
        result_select = dyn_obj.select(clave='idpdp', id=msisdn)
        print('result_select', result_select)
        ####FIN INSERT DYNAMO#####
        datetime_actual = datetime.now(tz)
        datetime_str =  result_select["datetime"]
        datetime_format = '%Y-%m-%dT%H:%M:%S'

        # Convertir la cadena a objeto datetime
        datetime_provided = datetime.strptime(datetime_str, datetime_format)
        # Calcular la diferencia	
        datetime_provided = tz.localize(datetime_provided)
        diferencia = datetime_actual - datetime_provided
        valid_time = timedelta(minutes=cfg.time_minutes_valid_session)
        if not result_select or diferencia > valid_time:
            return False
        return True
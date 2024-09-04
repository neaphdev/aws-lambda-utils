import sys
sys.path.insert(1,'libs')
import os
import boto3
import config_trazaapp as cfg
from datetime import datetime
#fecha/hora local
from datetime import datetime
import pytz
tz=pytz.timezone('America/Lima')
formatted_time = str(datetime.now(tz))

class Traza_appbim:
    def __init__(self,traza_app,context):
        self.traza_appbim=traza_app
        self.context=context
    def insert_traza_appbim(self):
        dynamodb = boto3.resource('dynamodb')
        try:
            table = dynamodb.Table(cfg.db_traza_app_bim)#name db from file cfg
            table.put_item(
            Item={
                "idrequestaws":self.context.aws_request_id,
                "traza_app":self.traza_appbim,
                "invoke_function":self.context.invoked_function_arn,
                "datetime":formatted_time,
            })
            return True
        except Exception as e:
            print(e)
            return False
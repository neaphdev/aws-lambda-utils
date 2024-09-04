import json
import os
import boto3
from xmljson import parker, Parker
import xml.etree.ElementTree as xml
from  errores_ewp import *
import config_ewp

from config_ewp import AuthGeneric

class EWP_APIS:

    def __init__(self):
        self.authorization_generic = AuthGeneric()
        self.use_getaccountholderinfo = os.environ.get("USE_GET_ACCOUNT_HOLDER_INFO")
        self.use_getaccounts = os.environ.get("USE_GET_ACCOUNTS")
        self.lambda_ewp_sender_awspdp = config_ewp.arn_lambda_api_sender_generico
        super().__init__()

    def __lambda_api_sender_awspdp(self, use_api_pdp) -> str:
        bol_debug_show = os.environ.get("BOL_DEBUG_API_SENDER")
        lambda_arn = config_ewp.arn_lambda_api + os.environ.get("API_SENDER_NAME")

        # Si el API EWP es 0 se usa Sender EWP si es 1 se usa API PDP
        if use_api_pdp == "0":
            lambda_arn = self.lambda_ewp_sender_awspdp

        if bol_debug_show == "1":
            print(f"API SENDER GENERICO: {lambda_arn}")

        return lambda_arn

        
    def xml_to_json(self, status_code,body):
        try:
            #print("PRUEBA")
            #status_code = 500
            #body = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><ns2:errorResponse xmlns:ns2="http://www.ericsson.com/lwac" errorcode="TRANSACTION_NOT_COMPLETED"><arguments name="status" value="FAILED"/></ns2:errorResponse>'
            if status_code == 200 and body:
                bf_str = Parker(xml_fromstring=False)
                xml_to_json = json.dumps(bf_str.data(xml.fromstring(body) ))
                xml_to_json = json.loads(xml_to_json)
                
                return {
                    "code":status_code,
                    "body":xml_to_json
                }
            else:
                body_return = xml_to_dict_error(body)
                str_error_code = body_return.get("errorcode", "")
                
                ###Validar si la operacion esta pendiente
                if str_error_code == "TRANSACTION_NOT_COMPLETED":
                    status = body_return["arguments"]["value"]
                    body_return["errorcode"] = "TRANSACTION_NOT_COMPLETED_FAILED"
                    if status == "PENDING":
                        body_return["errorcode"] = "TRANSACTION_NOT_COMPLETED_PENDING"
                print("body_return", body_return)
                return {
                    "code": status_code,
                    "body": body_return
                }
        except Exception as e:
            return {
                    "code": 500,
                    "body": xml_to_dict_error(body)
                }



    def getaccountholderinfo_generico(self, msisdn):
        try:
            invokeLam = boto3.client(
                "lambda", region_name=config_ewp.region_api_sender)
            payload = {
                "api_name": 'getaccountholderinfo',
                "auth": self.authorization_generic.get_auth_generic("getaccountholderinfo"),
                "message": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <ns2:getaccountholderinforequest xmlns:ns2="http://www.ericsson.com/em/emm/provisioning/v1_1">
                    <identity>ID:'''+msisdn+'''/MSISDN</identity>
                    </ns2:getaccountholderinforequest>'''
            }
            arn_lambda = self.__lambda_api_sender_awspdp(self.use_getaccountholderinfo)
            resp = invokeLam.invoke(
                FunctionName=arn_lambda, InvocationType="RequestResponse", Payload=json.dumps(payload))
            print(resp)
            res_json = json.loads(resp['Payload'].read().decode("utf-8"))
            print(res_json)
            print(res_json['body'])
            print(res_json['code'])
            data = self.xml_to_json(res_json['code'], res_json['body'])
            return data
        except Exception as e:
            print('Error',e)
            return{
                    "statusCode": 500,
                    "body": "INTERNAL_ERROR"
                }

    def getaccounts(self, msisdn):
        try:
            invokeLam = boto3.client("lambda", region_name=config_ewp.region_api_sender)
            payload = {
                "api_name": 'getaccounts',
                "auth": self.authorization_generic.get_auth_generic("getaccounts"),
                "message": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <ns2:getaccountsrequest xmlns:ns2="http://www.ericsson.com/em/emm/provisioning/v1_1">
                    <identity>ID:'''+msisdn+'''/MSISDN</identity>
                    </ns2:getaccountsrequest>'''
            }
            arn_lambda = self.__lambda_api_sender_awspdp(self.use_getaccounts)
            resp = invokeLam.invoke(
                FunctionName=arn_lambda, InvocationType="RequestResponse", Payload=json.dumps(payload))
            print(resp)
            res_json = json.loads(resp['Payload'].read().decode("utf-8"))
            print(res_json)
            print(res_json['body'])
            print(res_json['code'])
            return res_json
        except Exception as e:
            print('Error',e)
            return{
                    "statusCode": 500,
                    "body": "INTERNAL_ERROR"
                }
import xml.etree.ElementTree as xml
from xmljson import parker, Parker
import json

class Operacion(object):

    def __init__(self):
        super().__init__()

    def result_operacion(self,res_json):
        try:
            if str(res_json['code']) == '200':
                b = json.dumps(parker.data(xml.fromstring(res_json['body'])))
                print(b)
                b=json.loads(b)
                return b
            else:
                return {
                    "statusCode": 500,
                    "body": str(res_json['body'])
                }

        except Exception as e:
            print(e)
            return{
                "statusCode": 500,
                "body": "INTERNAL SERVER ERROR"
            }

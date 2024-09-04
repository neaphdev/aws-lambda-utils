import sys
sys.path.insert(1,'libs')
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime
import pytz
tz=pytz.timezone('America/Lima')

class DynamoBD:
    def __init__(self,table):
        self.table=table
        self.dynamodb = boto3.resource('dynamodb')

    def select(self,clave,id):
        try:
            query = self.dynamodb.Table(self.table)
            response = query.get_item(
                Key={
                    clave: id
                }
            )
            items = response['Item']
            return items

        except Exception as e:
            print('ERROR','ERROR SELECT DISP:',str(e))
            return []

    
    def insert(self,item):
        try:
            query = self.dynamodb.Table(self.table)#name db from file cfg
            item["datetime"]=self.get_datetime()
            query.put_item(
                Item=item
            )
            # Item={
            #     #"idawsrequest":self.context.aws_request_id,
            #     "idawsrequest":str(self.msisdn)+'_'+str(self.id_tel),
            #     "msisdn":self.msisdn,
            #     "id_tel":self.id_tel,
            #     "datetime":formatted_time
            # }
            return True
        except Exception as e:
            print('ERROR', "ERROR INSERT:",str(e))
            return False

    
    def delete(self,clave,id):
        try:
            table =self.dynamodb.Table(self.table)#name db from file cfg
            table.delete_item(
                Key={
                    clave:id
                })
            return True
        except Exception as e:
            print('Error al eliminar',str(e))
            return False

    def get_datetime(self):
        try:
            formatted_time = str(datetime.now(tz))
            return formatted_time
        except Exception as e:
            print('Error al generar fecha',str(e))
            return False

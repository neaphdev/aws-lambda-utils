import random
import os
from config_auth_generic import lista_usuarios

arn_lambda_api='arn:aws:lambda:us-east-1:807895504709:function:'
arn_lambda_api_sender_generico='arn:aws:lambda:us-east-1:807895504709:function:api_sender_PROD_awspdp'
arn_lambda_api_sender_user='arn:aws:lambda:us-east-1:807895504709:function:api_sender_PROD_xml_awspdp'
region_api_sender ='us-east-1'
auth_generico='Basic YXdzcGRwOmtPOSMxZkdUc0FBbyZYMT8j'

class AuthGeneric:

    def __init__(self):

        self.bol_debug_all = os.environ.get('BOL_DEBUG_ALL')

    def show_debug(self, key, opcion_seleccionada):
        if self.bol_debug_all == "1":

            bol_debug_show = os.environ.get(lista_usuarios[key]["key_environment_variable"])
            if bol_debug_show == "1":
                print("AUTH GENERIC", key, opcion_seleccionada)

    

    def get_auth_generic(self, key):
        opciones = lista_usuarios[key]["users"]

        opcion_seleccionada = random.choice(list(opciones.keys()))
        
        auth_generico=opciones[opcion_seleccionada]

        self.show_debug(key, opcion_seleccionada)
    
        return "Basic " + auth_generico
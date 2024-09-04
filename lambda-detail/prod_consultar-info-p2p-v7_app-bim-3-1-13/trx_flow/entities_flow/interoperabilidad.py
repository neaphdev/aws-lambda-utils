import base64_custom as b64
import config as cfg
import json
import uuid
import requests
from mysql import mysql_custom as my

import pytz
import datetime
import messagelevelenc as mle
import data_enc as data_enc_crypto
import os

import utils as u

tz = pytz.timezone('America/Lima')

class Interoperabilidad:

    def __init__(self, headers, destination_entity, origin_msisdn,
                destination_msisdn, firstname, surname, firstname_origin, surname_origin,max_amount_send_money):
 
        self.headers = headers
        self.destination_entity = destination_entity
        self.origin_msisdn = origin_msisdn
        self.destination_msisdn = destination_msisdn

        self.destination_first_name = firstname
        self.destination_last_name = surname
   
        self.destination_fullname = self.format_fullname(self.destination_first_name +' '+ self.destination_last_name)

        self.destination_first_name = ""
        self.destination_last_name = ""
        self.email  = "" 
        self.credential_payment_enc  = "" 
        self.expiration_cred_pay_date  = ""
        self.origin_first_name = firstname_origin
        self.origin_last_name = surname_origin
        self.max_amount_send_money = max_amount_send_money

        self.mysql = my.MySQLData()

    def validate_destination_entity(self):
        bol_destination_entity = cfg.entities_interoperabilidad.get(self.destination_entity, "")
        if not bol_destination_entity:
            raise Exception("DEFAULT")
        print("ENTIDAD: ", self.destination_entity)
        self.max_amount_send_money = bol_destination_entity["monto_max"]

    def validate_session(self):
        ###Implementar numeracion
        if self.headers:
            self.session_validate = b64.decode_b64(self.headers.get("session", ""))
            if not self.session_validate:
                print("SESSION no valida")
                raise Exception("DEFAULT")

            self.auth_user = self.headers.get('Authorization', "")  # get authorization
        self.session = self.session_validate
        
        params=(self.session_validate, self.origin_msisdn)
        print("SESSION", self.session_validate, self.origin_msisdn)
        resp = self.mysql.select_query(cfg.select_tabla_flujo, params)
        print(resp)
        if not resp:
            print("SESSION no valida")
            raise Exception("DEFAULT")
        ahora = datetime.datetime.now(tz)
        datetime_provided = tz.localize(resp[0]["created_at"])
        diferencia = ahora - datetime_provided
        valid_time = datetime.timedelta(minutes=cfg.time_minutes_valid_session_interop)

        if diferencia > valid_time:
            print("SESSION TIME NOT VALID")
            raise Exception("DEFAULT")
        
    def validar_numeracion(self):
        ahora = datetime.datetime.now(tz)
        print("AHORA", ahora)
        total_time_minutes = cfg.cfg_numeracion_interop["tiempo"]["dias"] * 24 * 60 + cfg.cfg_numeracion_interop["tiempo"]["horas"] * 60 + cfg.cfg_numeracion_interop["tiempo"]["minutos"]
        time_end = ahora + datetime.timedelta(minutes=total_time_minutes)
        time_init = ahora - datetime.timedelta(minutes=total_time_minutes)

        params=(self.origin_msisdn, time_init, time_end)
        print(params)
        resp = self.mysql.select_query(cfg.select_query_numeracion, params)
        print(resp)
        if not resp:
            raise Exception("DEFAULT")
        
        if resp[0]["cont"] > cfg.cfg_numeracion_interop["cantidad_intentos"]:
            print("SE EXCEDIO LA CANTIDAD DE INTENTOS")
            raise Exception("MANY_ATTEMPTS")
        
	
    def get_data_destination_user(self):
        self.call_api_resolve_yp()

	##Actualizar la tabla de flujo
    def update_table_flow(self):
        print("Actualizar la tabla de flujo de interoperabilidad")
        self.ahora = datetime.datetime.now(tz)


        params = (self.destination_first_name, self.destination_last_name, 
                    self.origin_first_name, self.origin_last_name,
                    self.destination_entity, self.ahora, self.id_yellow_pepper,
                    self.email, self.credential_payment_enc, self.expiration_cred_pay_date, 
                    self.session_validate)
        print(params)
        print(cfg.update_tabla_flujo)
        resp = self.mysql.insert_query(cfg.update_tabla_flujo, params)
        print(resp)
        
        if not resp:         
            print("Error inicializando la tabla al insertar")
            raise Exception("errorNotFound")

    def error_table_flow(self, statusdesc):
        print("Error tabla flujo")
        params = (statusdesc, self.session )
        print(params)
        print(cfg.update_tabla_flujo_error)
        resp = self.mysql.insert_query(cfg.update_tabla_flujo_error, params)
        print(resp)
        
        if not resp:         
            print("Error inicializando la tabla al insertar")
            raise Exception("errorNotFound")

   
    def call_api_resolve_yp(self):
        print("Invocar api resolve de YP")

        alias_type = "PHONE"
       
        payload = {
            "api_name": 'resolve',
            "lambda_name": os.environ['AWS_LAMBDA_FUNCTION_NAME'],
            "data":{
                "origin_msisdn": self.origin_msisdn,
                "alias_value": "+"+self.destination_msisdn,
                "alias_type": alias_type,
                "destination_entity": self.destination_entity,
            }
        }
        response, responseStatusCode =u.invoke_lambda(cfg.arn_lambda_yp, payload)

        print("RESPONSE DECRYPTED", responseStatusCode)
        

        self.id_yellow_pepper = response["xcorrelationid"]

        if responseStatusCode != 200:
            print("Error al consultar a YP")
            raise Exception("DEFAULT")

        profile = response.get("profile", "")
        contactinfo = profile.get("contactInfo", "")
        phone = ""
        if contactinfo:
            for i in  contactinfo:
                contactinfo_val = i 
                
                typecontact = contactinfo_val.get("type", "")
                if typecontact == "PHONE":
                    phone = contactinfo_val.get("value", "")
                if typecontact == "EMAIL":
                    self.email = contactinfo_val.get("value", "")

        paycred = response.get("paymentCredentials", "")
        bol_cred_pay = False
        for i in paycred:
            if i["type"] == "CARD":
                obj_CryptoUtil = data_enc_crypto.CryptoUtil()
                
                self.credential_payment_enc = obj_CryptoUtil.encript_word(i["accountNumber"])
                self.expiration_cred_pay_date = obj_CryptoUtil.encript_word(i["expirationDate"])
                bol_cred_pay = True
                break

        if not bol_cred_pay:
            print("NO SE ENCONTRO CREDENCIALES DE PAGO VALIDAS")
            raise Exception("DEFAULT")
        
        
        firstName = profile.get("firstName", "")
        lastName = profile.get("lastName", "")
        
        self.destination_first_name = firstName
        self.destination_last_name = lastName
        self.destination_fullname = self.format_fullname(self.destination_first_name + " " + self.destination_last_name)

        
    def format_fullname(self, fullname):
        fullname = fullname.replace(' / ', ' ')
        fullname = fullname.replace('/', ' ')
        fullname = fullname.title()
        return fullname
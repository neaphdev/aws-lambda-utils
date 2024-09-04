import base64_custom as b64
from entities_flow import bim
from entities_flow import interoperabilidad
import json
import config as cfg

class MandarPlata():

    def __init__(self, origin_msisdn, destination_msisdn, 
                       data_get_account_holder, firstname, surname, headers, destination_entity, max_amount_send_money,
                       firstname_origin, surname_origin):
        print("INICIO MANDAR PLATA")
        self.origin_msisdn = origin_msisdn
        self.destination_msisdn = destination_msisdn
        self.destination_entity = destination_entity
        self.firstname = firstname
        self.surname = surname
        self.fullname = ""
        self.comision = str(cfg.default_comision)
        self.headers = headers
        self.max_amount_send_money = max_amount_send_money
        self.data_get_account_holder = data_get_account_holder
        self.firstname_origin = firstname_origin
        self.surname_origin = surname_origin

    ###Validar saldo



    def get_aditional_params_mandar_plata(self, body):
        
        self.destination_entity=b64.decode_b64(str(body.get('entidad_destino')))
        print("entidad_destino",self.destination_entity)



    def validate_balance(self):
        rc      = self.ewp_obj.getbalance(self.destination_msisdn)
        print("RESP GET BALANCE", rc)
        
        if not rc["code"] == 200:
            raise Exception("DEFAULT")
        
        balance = float(rc["body"]["balance"]["amount"])  
        print("BALANCE", balance)
        print("Monto", self.amount)
        if balance == 0 or float(self.amount) > balance:
            raise Exception("NOT_FOUNDS")

    
    def get_info_entity(self):
        if self.destination_entity == "BIM":
            print("Usuario envia a BIM")
            obj_bim = bim.Bim(self.origin_msisdn, 
                                self.destination_msisdn, self.firstname, self.surname)

                
            self.destination_msisdn = obj_bim.destination_msisdn
            self.comision = obj_bim.comision
            self.destination_fullname = obj_bim.fullname
            
            return self.make_response(200, "COMPLETED", "")

        else:
            print("Es interoperabilidad")
            obj_interop = interoperabilidad.Interoperabilidad(self.headers, self.destination_entity, 
                                                            self.origin_msisdn, self.destination_msisdn, 
                                                            self.firstname, self.surname, self.firstname_origin, self.surname_origin, self.max_amount_send_money)
            obj_interop.validate_destination_entity()
            obj_interop.validate_session()
            try:
                obj_interop.validar_numeracion()
                obj_interop.get_data_destination_user()
                obj_interop.update_table_flow()
            except Exception as e:
                print("Error", e)
                obj_interop.error_table_flow(str(e))
                raise Exception(str(e))
            
            self.destination_fullname = obj_interop.destination_fullname
            self.max_amount_send_money = obj_interop.max_amount_send_money
            return self.make_response(200, "COMPLETED", "")

    
    def make_response(self, statusCode, status, message):

        body_resp = {}
        body_resp["status"] = b64.encode_b64(status)
        body_resp["message"] = b64.encode_b64(message)
        if statusCode == 200:

            body_resp["destination_fullname"] = b64.encode_b64(self.destination_fullname)
            body_resp["destination_entity"] = b64.encode_b64(self.destination_entity)
            body_resp["max_amout_send"] = b64.encode_b64(str(self.max_amount_send_money))
            body_resp["destination_msisdn"] = b64.encode_b64(self.destination_msisdn)
            #body_resp["comision"] = b64.encode_b64(self.comision )
        response = {}
        response["statusCode"] = statusCode
        response["body"] = json.dumps(body_resp)

        print('DEBUG', 'RESPONSE:['+str(response)+'].END REQUEST')
        return response
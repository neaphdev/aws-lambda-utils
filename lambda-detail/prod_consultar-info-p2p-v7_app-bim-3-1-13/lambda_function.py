import sys
sys.path.insert(1,'traza_app')
sys.path.insert(1,'ewp')
sys.path.insert(1,'base64_custom')
sys.path.insert(1,'app_controller')
sys.path.insert(1,'trx_flow')
sys.path.insert(1,'mysql')
sys.path.insert(1,'mle')
sys.path.insert(1,'utils')
sys.path.insert(1,'Authorization')
from authorization_ewp import *
import json
import base64_custom as b64
from traza_appbim import *
import ewp as ew

from operacion import *
import config as cfg
from valida_disp import ValidaDisp
import mandarplata
import errores as err
from errores_ewp import *


def lambda_handler(event, context):
    try:
        print('DEBUG', 'START REQUEST. INPUT:'+str(event['body']))

        # get input
        ewp = ew.EWP_APIS()
        op = Operacion()
        
        b = json.loads(event['body'])
        traza_app = str(b['traza_app'])
        origen=b64.decode_b64(str(b['origin_msisdn']))
        print("origen",origen)
        destino=b64.decode_b64(str(b['destination_msisdn']))
        print("destino",destino)
        destination_entity=b64.decode_b64(str(b.get('destination_entity')))
        print("entidad_destino", destination_entity)
        # INICIO TOKENIZACIÓN Y AUTH
        datos_header =event['headers']
        print("datos del header",datos_header )
        token = b64.decode_b64(datos_header["token"])
        pantalla =b64.decode_b64(datos_header["pantalla"])
        numero_msisdn = b64.decode_b64(datos_header["msisdn"])

        print("token",token)
        print("pantalla",pantalla)
        print("numero_msisdn",numero_msisdn)

        objeto_session= Authorization_ewp(numero_msisdn,token,pantalla)
        status,response_auth = objeto_session.obtener_authorization()
        if not status:
            return objeto_session.make_response()
        
        status_update_tiempo_caducidad = objeto_session.actualizar_fecha_caducidad()
        if not status_update_tiempo_caducidad:
            return objeto_session.make_response()
        
        # FIN TOKENIZACIÓN Y AUTH
        
        ################VALIDA DISP########################
        
        obj_valida_disp= ValidaDisp()
        auth_msisdn = "Basic "+b64.encode_b64(origen+":")
        is_valid=obj_valida_disp.valida_disp(traza=traza_app,auth=auth_msisdn)
        print('Validancion de dispositivo:',is_valid)
        if not is_valid:
            raise Exception("DISP_NOT_VALID")
        
        is_valid_session = obj_valida_disp.session_validate(origen)
        if not is_valid_session:
            return objeto_session.make_response()
        ################END VALIDA DISP########################

        # Insert Traza app bim
        # creamos el objeto para insertar la traza
        tap = Traza_appbim(traza_app, context)
        result = tap.insert_traza_appbim()
        print('INSERTANDO TRAZA APP. RESULTADO:', result)
        # status user
        #MANDAR_PLATA,PAGAR_PRESTAMO,PAGAR_COMPRA,PAGAR_SERVICIO
        ga = ""
        maximo_valor = ""
        firstname=''
        surname=''
        perfil=''

        ga_origin=ewp.getaccountholderinfo_generico(origen)
        body = ga_origin.get("body", "")
        firstname_origin=str(body['accountholderbasicinfo'].get('firstname', ""))
        if not firstname_origin:
            raise Exception("NOMBRES_NO_VALIDOS")
        surname_origin=str(body['accountholderbasicinfo'].get('surname', ""))
        if not surname_origin:
            raise Exception("NOMBRES_NO_VALIDOS")

        if destination_entity == "BIM":
            ga=ewp.getaccountholderinfo_generico(destino)
            #ga=account_destino_info_json
            print('INFO','GETACCOUNTHOLDER DESTINO:'+str(ga))

            #res_op_destino=op.result_operacion(ga)
            
            body = ga.get("body", "")
            if ga['code']==200:
                perfil=str(body['accountholderbasicinfo']['profilename'])
                print("perfil", perfil)
                status_user=str(body['accountholderbasicinfo']['accountholderstatus'])
                if str(status_user) =='REGISTERED':
                    print('INFO','USUARIO STATUS:'+str(status_user))
                    raise Exception("USER_REGISTERED")
                try:
                    firstname=str(body['accountholderbasicinfo']['firstname'])
                    print(firstname)
                    if firstname.find(' ') !=-1:
                        firstname=firstname[:firstname.find(' ')]
                except Exception as e:
                    print('first name',e)
                    firstname=''
                try:
                    surname=str(body['accountholderbasicinfo']['surname'])
                except Exception as e:
                    print('surname:',e)
                    surname=''
            else:
                print("USUARIO NO TIENE BIM")
                raise Exception("DEFAULT")
        

        account_xml=ewp.getaccounts(origen) #Asumiendo que origen es el que paga 
        account_json=op.result_operacion(account_xml) #Tranforma el xml
        account_profile=account_json['accountslist']['account']['profilename']
        print(account_profile)
        if str(account_profile).lower().find('general') != -1:
            type_account = 'general'
        else:
            type_account = 'simplificada'
        
        print('tipo cuenta origen',type_account)
    
        

        if "FCOMPARTAMOS" in account_profile:
            max_value=cfg.max_type_account_route["FCOMPARTAMOS"]
        else:
            max_value=cfg.max_type_account_route['.']
        
        maximo_valor = max_value[type_account]
       
        
        origin_msisdn = origen
    
        destination_msisdn = destino
    
        data_get_account_holder = ga
        headers = event.get("headers", "")
        headers["Authorization"] = response_auth

        obj_mandarplata = mandarplata.MandarPlata(origin_msisdn, destination_msisdn, \
                                                    data_get_account_holder, firstname, surname, headers, destination_entity, maximo_valor,
                                                    firstname_origin, surname_origin)
        print('limite maximo',maximo_valor)

        status_update, tokesession = objeto_session.actualizar_fecha_token()
        if not status_update:
            return objeto_session.make_response()
        ###Envia dinero
        resp_return = obj_mandarplata.get_info_entity()
        resp_return.update({'headers': {
            "Content-Type": "application/json",
            "token": b64.encode_b64(tokesession) # Agregar tu token como un encabezado personalizado
            },})
        return resp_return
    
    except Exception as e:
        print("Error", e)
        
        if (err.ewp_error_fix in str(e)):
    
            str_error = str(e).split("-")
            ewp_error = str_error[1]
            
            error_obj = err.map_errores.get("DEFAULT_EWP")
            error_obj["message"] = errores.get(ewp_error, "")

            if ewp_error in err.map_errores.keys():
                error_obj = err.map_errores.get(ewp_error, err.map_errores["DEFAULT"])
        else:
            error_obj = err.map_errores.get(str(e), err.map_errores["DEFAULT"])
        
        print("ERROR MAP", error_obj)
        
        res={}
        res["status"] = b64.encode_b64("FAILED")
        res["message"] = b64.encode_b64(error_obj["message"])
        res["cod_popup"] = b64.encode_b64(error_obj["cod_error_pop_up"])
        r={
            "statusCode": 500,
            "body": json.dumps(res)
        }
        print('DEBUG', 'RESPONSE:['+str(r)+'].END REQUEST')
        return r



max_type_account_route={ 'FCOMPARTAMOS':
                            {
                            'general':"20000.00",
                            'simplificada':"1537.00"
                            },
                        '.':
                            {
                            'general':"1537.00",
                            'simplificada':"1537.00"
                            },
                        }

max_amount_send_money = 999.00
default_comision = 0.00

arn_valida_disp = 'arn:aws:lambda:us-east-1:807895504709:function:prod_valida-disp-backend-v3'
tabla_flujo = "flujo_interoperabilidad"


status = ["PENDING", "COMPLETED", "FAILED"]
select_tabla_flujo = '''select * from {0} where session = %s 
                                    and origin_msisdn = %s and status != "{1}"  '''.format(tabla_flujo, status[1])

status_desc = "CONSULTAR_INFO"
update_tabla_flujo = '''update {0} set destination_first_name = %s, destination_last_name=%s, origin_first_name = %s,
                                 origin_last_name= %s,
                                 destination_wallet = %s, created_at = %s, 
                                 process_flow = "{1}", id_yellow_pepper=%s,
                                email =%s, credential_payment_enc=%s, expiration_cred_pay_date=%s
                                  where session = %s'''.format(tabla_flujo, status_desc)
update_tabla_flujo_error = '''update {0} set status = "{1}", status_description=%s where session = %s'''.format(tabla_flujo, status[2])

entities_interoperabilidad = {
    "BIM": {
        "name": "BIM",
        "monto_max": '999.00'
    },
    "YAPE": {
        "name": "YAPE",
        "monto_max": '999.00'
    },
    "PLIN": {
        "name": "PLIN",
        "monto_max": '999.00'
    }
}


cfg_numeracion_interop = {
    "cantidad_intentos": 10,
    "tiempo":{
        "dias": 0,
        "horas": 0,
        "minutos": 10
    }
}

process_type="ENVIO_DINERO_P2P"
select_query_numeracion = '''select count(*) cont from 
                {0} where origin_msisdn= %s
                    and process_type = "{1}" 
                    and created_at BETWEEN %s and %s'''.format(tabla_flujo, process_type) 

semilla_crypto_card = "57bdbe6aaa560ef2cecff5ef2753f1e3"

region_arn = "us-east-1"
arn_lambda_yp= "arn:aws:lambda:us-east-1:807895504709:function:prod_modulo-yellow-pepper"

table_db_session="session_appbim_prod"
time_minutes_valid_session = 9
time_minutes_valid_session_interop = 5
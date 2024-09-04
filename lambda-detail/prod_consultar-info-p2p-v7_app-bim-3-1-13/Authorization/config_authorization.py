from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('America/Lima')
select_flujo_by_token_at_00 = "(SELECT * FROM {} WHERE msisdn = %s and tokensession = %s ) UNION ALL (SELECT * FROM {} WHERE msisdn = %s and tokensession = %s)"

def get_current_date_table():
    current_date = datetime.now(tz)
    return "token_operacion_" + current_date.strftime('%Y%m%d')

def get_yesterday_date_table():
    yesterday = datetime.now(tz) - timedelta(days=1)
    return "token_operacion_" + yesterday.strftime('%Y%m%d')

DB = {
    "database": "bimtoken",
    "host": "db-bimtoken-prod.cy7neut4p7qs.us-east-1.rds.amazonaws.com",
    "user": "postgres",
    "password": "UJM7kta0RPUV4AF95u6g",
    "port":5432,
    "timeout":30
}


minutos_de_caducidad = 5
segundos_de_caducidad = 0

validar_primeros_minutos = 10

screen_all = "ALL"

def query_select(table):
    return " SELECT msisdn, idsession, tokensession, traza_app, screen, idewp ,auth,fecha_de_caducidad, minutos FROM " + table + " WHERE msisdn = %s and tokensession = %s"
def query_update(table):
    return " UPDATE " + table + " SET screen = %s, tokensession =%s, minutos=%s  WHERE msisdn = %s and tokensession = %s"
def query_update_tiempo_caducidad(table):
    return " UPDATE " + table + " SET fecha_de_caducidad = %s::TIMESTAMP WITHOUT TIME ZONE, minutos=%s  WHERE msisdn = %s and tokensession = %s"
def query_delete(previous_table):
    return " DELETE FROM " + previous_table + " WHERE msisdn = %s"
def query_insert(table):
    return "INSERT INTO " + table + " (msisdn, idsession, tokensession, traza_app, screen,idewp ,auth, fecha_de_caducidad,minutos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::TIMESTAMP WITHOUT TIME ZONE, %s)"

mensaje_logout = "Su sesión de usuario ha caducado"

screen_pantalla_actual = 'CONSULTAR-INFO-P2P'
screen_pantalla_formato = "MsNmPtT_129"
accepted_screens =["VALIDAR_USUARIO_P2P","CONSULTAR-INFO-P2P" ,"INICIO-FLUJO-P2P","COTIZACION-P2P"]

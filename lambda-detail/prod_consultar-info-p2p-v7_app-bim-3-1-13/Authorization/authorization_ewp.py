
import config_authorization as cfg_auth
from postgresql import PostgreSQLData
import exception_authorization as cfg_except
from datetime import datetime, timedelta
import pytz
from uuid import uuid4
from time import sleep
tz=pytz.timezone('America/Lima')
import base64

class Authorization_ewp:
    def __init__(self,msisdn,token,pantalla):
        self.msisdn=msisdn
        self.token = token
        self.postgres = PostgreSQLData(cfg_auth.DB)
        self.pantalla = pantalla
        self.validado = False
        self.datos = ""
        self.minutos = 0
        self.fecha_caducidad = ""

    def obtener_authorization(self):
        try:
            
            current_time = datetime.now(tz)
            #static_time = datetime(2024, 5, 2, 23, 59, 0, tzinfo=pytz.timezone('America/Lima'))
            #current_time = static_time
            print(f"Fecha y hora actual: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            if current_time.hour == 0 and (current_time.minute < cfg_auth.validar_primeros_minutos or (current_time.minute == cfg_auth.validar_primeros_minutos and current_time.second == 0)):
                query = cfg_auth.select_flujo_by_token_at_00.format(cfg_auth.get_yesterday_date_table(), cfg_auth.get_current_date_table())
                status,datos,afectados = self.postgres.select_query(query, (self.msisdn,self.token,self.msisdn,self.token))
                print("Se consulta la tabla antigua y actual por ser las primeras horas del dia")
            else:
                status,datos,afectados = self.postgres.select_query(cfg_auth.query_select(cfg_auth.get_current_date_table()), (self.msisdn,self.token))
            
            if status == False or int(afectados) == 0:
                raise Exception("REGISTRO_NO_ENCONTRADO")
            objeto = datos[0]
            print("---------------------")
            print("msisdn:", objeto.msisdn)
            print("idsession:", objeto.idsession)
            print("tokensession:", objeto.tokensession)
            print("traza_app:", objeto.traza_app)
            print("screen:", objeto.screen)
            print("auth:", objeto.auth)
            print("fecha_de_caducidad:", objeto.fecha_de_caducidad)
            print("minutos:", objeto.minutos)
            print("---------------------")
            self.datos = datos[0]
            self.minutos = objeto.minutos
            status_caducado = self.obtener_tiempo_transcurrido(objeto.fecha_de_caducidad)
            if not status_caducado:
                raise Exception("REGISTRO_CADUCADO")
            
            status_screen = self.validar_screen(objeto.screen)
            if not status_screen:
                raise Exception("ERROR_SCREEN")
            
            print("Screen y token validado")
            self.validado = True
            print("Cambiando stado",self.validado )
            return True, objeto.auth

        except Exception as e:
            error_msg = cfg_except.ERROR_LIST[str(e)] if str(e) in cfg_except.ERROR_LIST else cfg_except.CUSTOM_ERROR
            print("ERROR", "ERROR SELECT TOKEN:", error_msg)
            return False, "LOGOUT"
        
    def obtener_tiempo_transcurrido(self,tiempo_registrado):
        try:
            # Obtener la hora actual
            tiempo_actual = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            tiempo_actual_en_formato = datetime.strptime(tiempo_actual,"%Y-%m-%d %H:%M:%S")

            diferencia_tiempo = tiempo_actual_en_formato - tiempo_registrado
            diferencia_tiempo_segundos = diferencia_tiempo.total_seconds()

            if tiempo_actual_en_formato > tiempo_registrado:
                print("El registro caduco hace ", diferencia_tiempo_segundos, " Segundos")
                return False
            
            print("El registro va a caducar en ",abs(diferencia_tiempo_segundos), " Segundos")
            return True

        except Exception as e:
            print('ERROR', "ERROR AL OBTENER LA HORA DEL REGISTRO.:",str(e))
            return False
        
    def validar_screen(self,screen):
        print("la pantalla actual es : ", screen)
        if cfg_auth.accepted_screens[0] == cfg_auth.screen_all:
            return True
        elif screen in cfg_auth.accepted_screens:
            if self.pantalla == cfg_auth.screen_pantalla_formato:
                return True
        else:
            return False
        
    def actualizar_fecha_token(self):
            try:
                if self.validado == True:
                    #Nuevo token de session
                    nuevotoken = uuid4().hex
                    # Nuevo screen
                    print("Actualizando a actual screen:", cfg_auth.screen_pantalla_actual)
                    #Nuevo minuto de registro
                    #static_time = datetime(2024, 5, 3, 0, 0, 1, tzinfo=pytz.timezone('America/Lima'))
                    #hora_actual = static_time
                    hora_actual = datetime.now(tz)
                    minutos_actual = hora_actual.hour * 60 + hora_actual.minute + 1
                    data = (cfg_auth.screen_pantalla_actual,nuevotoken,minutos_actual,self.msisdn,self.token)
                    if hora_actual.hour == 0 and (hora_actual.minute < cfg_auth.validar_primeros_minutos or (hora_actual.minute == cfg_auth.validar_primeros_minutos and hora_actual.second == 0)):
                        if self.minutos > cfg_auth.validar_primeros_minutos:
                            status_update,afectados = self.eliminar_y_actualizar_nuevo_token(nuevotoken)
                            if not status_update:
                                raise Exception("ERROR_DELETE_AND_CREATE")
                        else:
                            status_update,afectados = self.postgres.update_query(cfg_auth.query_update(cfg_auth.get_current_date_table()), data)
                    else:   
                        status_update,afectados = self.postgres.update_query(cfg_auth.query_update(cfg_auth.get_current_date_table()), data)   
                    if status_update == False or int(afectados) == 0:
                        return False, ""
                    print("se actualizo el token y screen")
                    return True,nuevotoken
                else:
                    print("No se puede actualizar si el usuario no valido primero el token y la session")
                    raise Exception("Error de validación previa al update")
            except Exception as e:
                print('ERROR', "ERROR AL REALIZAR EL UPDATE DEL REGISTRO.:",str(e))
                return False,""
            
    def actualizar_fecha_caducidad(self):
            try:
                if self.validado == True:
                    #static_time = datetime(2024, 5, 2, 23, 59, 58, tzinfo=pytz.timezone('America/Lima'))
                    #hora_actual = static_time
                    hora_actual = datetime.now(tz)
                    nueva_fecha_caducidad = hora_actual + timedelta(minutes= cfg_auth.minutos_de_caducidad, seconds=cfg_auth.segundos_de_caducidad)
                    nueva_fecha_caducidad_sql = nueva_fecha_caducidad.strftime('%Y-%m-%d %H:%M:%S')

                    #Nuevo minuto de registro
                    minutos_actual = hora_actual.hour * 60 + hora_actual.minute + 1
                    data = (nueva_fecha_caducidad_sql,minutos_actual,self.msisdn,self.token)
                    if hora_actual.hour == 0 and (hora_actual.minute < cfg_auth.validar_primeros_minutos or (hora_actual.minute == cfg_auth.validar_primeros_minutos and hora_actual.second == 0)):
                        if self.minutos > cfg_auth.validar_primeros_minutos:
                            status_update,afectados = self.eliminar_y_actualizar_fecha_caducidad(nueva_fecha_caducidad_sql,minutos_actual)
                            if not status_update:
                                raise Exception("ERROR_DELETE_AND_CREATE")
                        else:
                            status_update,afectados = self.postgres.update_query(cfg_auth.query_update_tiempo_caducidad(cfg_auth.get_current_date_table()), data)
                    else:
                        status_update,afectados = self.postgres.update_query(cfg_auth.query_update_tiempo_caducidad(cfg_auth.get_current_date_table()), data)
                    if status_update == False or int(afectados) == 0:
                        return False, ""
                    self.fecha_caducidad = nueva_fecha_caducidad_sql
                    self.minutos = minutos_actual
                    print("se actualizo la fecha de caducidad")
                    return True
                else:
                    print("No se puede actualizar si el usuario no valido primero el token y la session")
                    raise Exception("Error de validación previa al update")
            except Exception as e:
                print('ERROR', "ERROR AL REALIZAR EL UPDATE DEL REGISTRO.:",str(e))
                return False

    def eliminar_y_actualizar_fecha_caducidad(self,nueva_fecha_caducidad_sql,minutos_actual):
        try:
            data_delete = (self.msisdn,)
            status,afectados = self.postgres.delete_query(cfg_auth.query_delete(cfg_auth.get_yesterday_date_table()), data_delete)
            print("Cantidad de registros eliminados:",afectados)
            if not status:
                return False, afectados
            data = (self.datos.msisdn, self.datos.idsession,self.datos.tokensession, self.datos.traza_app, self.datos.screen,self.datos.idewp ,self.datos.auth, nueva_fecha_caducidad_sql, minutos_actual)
            status,afectados = self.postgres.insert_query(cfg_auth.query_insert(cfg_auth.get_current_date_table()), data)
            print("Cantidad de registros insertados:",afectados)
            if not status:
                return False, afectados
            return True, afectados

        except Exception as e:
            print('ERROR', "ERROR INSERTAR, DELEATEAR REGISTRO:",str(e))
            return False, 0
        
    def eliminar_y_actualizar_nuevo_token(self,nuevo_token):
        try:
            data_delete = (self.msisdn,)
            status,afectados = self.postgres.delete_query(cfg_auth.query_delete(cfg_auth.get_yesterday_date_table()), data_delete)
            print("Cantidad de registros eliminados:",afectados)
            if not status:
                return False, afectados
            data = (self.datos.msisdn, self.datos.idsession, nuevo_token, self.datos.traza_app, cfg_auth.screen_pantalla_actual, self.datos.idewp, self.datos.auth, self.fecha_caducidad, self.minutos)
            status,afectados = self.postgres.insert_query(cfg_auth.query_insert(cfg_auth.get_current_date_table()), data)
            print("Cantidad de registros insertados:",afectados)
            if not status:
                return False, afectados
            return True, afectados

        except Exception as e:
            print('ERROR', "ERROR INSERTAR, DELEATEAR REGISTRO:",str(e))
            return False, 0
        
    def make_response(self):
        r={
            "statusCode": 500,
            "body": '''{
                "status": "'''+self.encode_b64("LOGOUT")+'''",
                "message": "'''+self.encode_b64(cfg_auth.mensaje_logout)+'''"
                }'''
            } 
        print('DEBUG','RESPONSE['+str(r)+'].END REQUEST')    
        return r

    def encode_b64(self,message):
        message_bytes = message.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        return base64_message

            




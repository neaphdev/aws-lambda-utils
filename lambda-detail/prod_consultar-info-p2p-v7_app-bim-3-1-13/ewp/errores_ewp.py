import xml.etree.ElementTree as ET


errores={
    "AUTHORIZATION_ACCOUNT_NOT_ALLOWED_TO_PERFORM_ACTION" :  "Lo sentimos, no puedes realizar esta operación",
    "FRI_INVALID" :  "Ingresa nuevamente tu número de celular",
    "INCORRECT_PIN" :  "Contraseña incorrecta, intenta nuevamente",
    "NOT_AUTHORIZED" :  "No puedes realizar esta operación",
    "NOT_ENOUGH_FUNDS" :  "No cuentas con saldo para realizar esta operación",
    "SESSION_INVALID" :  "Cerramos tu Bim por seguridad, ingresa nuevamente",
    "ACCOUNT_HOLDER_DOES_NOT_EXIST" :  "Número Bim incorrecto",
    "ACCOUNTHOLDER_ANY_ONE_MANDATORY_FIELD_REQUIRED" :  "Revisa los datos que ingresaste",
    "ACCOUNTHOLDER_WITH_MSISDN_ALREADY_EXISTS" :  "Ya existe un Bim registrado con ese número de celular",
    "ACCOUNTHOLDER_WITH_USERNAME_ALREADY_EXISTS" :  "Ya existe un Bim registrado con ese nombre de usuario",
    "AUTHORIZATION_FAILED" :  "Intentalo nuevamente",
    "COULD_NOT_PERFORM_OPERATION" :  "Intenta realizar la operación nuevamente",
    "FIELD_TOO_LONG" :  "Revisa los datos que ingresaste",
    "HOME_CHARGING_REGION_NOT_FOUND" :  "El operador móvil elegido no está disponible",
    "ID_LENGTH_OUT_OF_BOUNDS" :  "Revisa tu número de DNI",
    "IDENTIFICATION_ID_AND_TYPE_ALREADY_EXIST" :  "Tu DNI ya se encuentra registrado",
    "IDENTITY_INVALID" :  "Los datos de tu DNI son inválidos",
    "IDTYPE_NOT_SUPPORT" :  "Revisa los datos que ingresaste",
    "INVALID_FIELD_VALUE" :  "Revisa los datos que ingresaste",
    "MANDATORY_FIELD_MISSING" :  "Revisa los datos que ingresaste",
    "PROFILE_NOT_FOUND" :  "No te encuentras registrado en Bim",
    "PROFILE_TYPE_MISMATCH" :  "Slecciona nuevamente tu perfil",
    "REQUIRED_FIELD_MISSING" :  "Información no encontrada",
    "UNABLE_TO_CREATE_ACCOUNTHOLDER" :  "Intenta registrarte nuevamente",
    "ACCOUNTHOLDER_ACTIVATION_FAILED" :  "Intenta registrarte nuevamente",
    "AUTHORIZATION_NOT_REGISTERED_STATUS" :  "No te encuentras registrado en Bim",
    "BANKDOMAIN_NOT_FOUND" :  "El emisor seleccionado no está disponible",
    "CREDENTIAL_REPEATED_SECRET_DOES_NOT_MATCH" :  "Las contraseñas no son iguales",
    "CREDENTIAL_TYPE_NOT_FOUND" :  "No puedes ingresar con esos datos a Bim",
    "NONDIGIT_CHARACTERS_IN_PINCODE" :  "La contraseña solo puede contener números",
    "PINCODE_DENIED_BY_MATCHING_BIRTH_DATE" :  "La contraseña no puede coincidir con tu fecha de nacimiento",
    "PINCODE_DENIED_BY_MATCHING_IDENTIFICATION_NUMBER" :  "La contraseña no puede coincidir con tu DNI",
    "PINCODE_DENIED_BY_MATCHING_MSISDN" :  "La contraseña no puede coincidir con tu número de celular",
    "PINCODE_DENIED_BY_MATCHING_REGULAR_EXPRESSION" :  "La contraseña no es válida",
    "PINCODE_TOO_LONG" :  "La contraseña debe contener 4 dígitos",
    "PINCODE_TOO_SHORT" :  "La contraseña debe contener 4 dígitos",
    "TOO_MANY_CONSECUTIVE_DIGITS_IN_PINCODE" :  "La contraseña no puede contener númerosconsecutivos",
    "TOO_MANY_REPEATED_DIGITS_IN_PINCODE" :  "La contraseña no puede contener número repetidos",
    "ACCOUNT_NOT_FOUND" :  "Tu número de celular no se encuentra registrado en Bim",
    "ACCOUNTHOLDER_NOT_ACTIVE" :  "Tu usuario no se encuentra activo",
    "ACCOUNTHOLDER_NOT_FOUND" :  "No se encuentra registrado tu número de celular",
    "AMOUNT_INVALID" :  "El monto ingresado es incorrecto",
    "AUTHORIZATION_MAX_TRANSFER_AMOUNT" :  "Excedes el monto máximo de transacción",
    "AUTHORIZATION_MAX_TRANSFER_AMOUNT_FEE" :  "Excedes el monto máximo de transacción",
    "AUTHORIZATION_MAX_TRANSFER_TIMES" :  "Excedes el número de transacciones",
    "AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_RECEIVE" :  "Excedes el monto máximo de transacción",
    "AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_SEND" :  "Excedes el monto máximo de transacción",
    "AUTHORIZATION_MINIMUM_AMOUNT_ALLOWED_TO_SEND" :  "El dinero a envíar es menor al permitido",
    "AUTHORIZATION_MINIMUM_AMOUNT_ALLOWED_TO_SEND_ACCOUNT" :  "El dinero a envíar es menor al permitido",
    "AUTHORIZATION_MINIMUM_AMOUNT_ALLOWED_TO_SEND_ACCOUNT_REFERENCE" :  "El dinero a envíar es menor al permitido",
    "AUTHORIZATION_RECEIVER_ACCOUNT_NO_DEPOSIT" :  "No es posible enviar dinero a ese número celular",
    "AUTHORIZATION_RECEIVER_MAX_ALLOWED_BALANCE" :  "Llegaste a tu monto máximo. Comunícate con nostros al 080010838",
    "AUTHORIZATION_RECEIVING_ACCOUNT_NOT_ACTIVE" :  "El Bim que ingresaste no puede recibir dinero",
    "AUTHORIZATION_RECEIVING_ACCOUNT_UNAVAILABLE" :  "El Bim que ingresaste no puede recibir dinero",
    "CAN_NOT_RECEIVE_CASHIN" :  "El Bim que ingresaste no puede recibir dinero",
    "COULD_NOT_PERFORM_TRANSACTION" :  "Intenta nuevamente, no pudimos completar la operación",
    "INACTIVE_ACCOUNT" :  "El Bim que ingresaste no puede recibir dinero",
    "INVALID_RECEIVER" :  "El Bim que ingresaste no puede recibir dinero",
    "SOURCE_AND_TARGET_ARE_THE_SAME" :  "El número al cual quieres enviar plata, debe ser diferente al tuyo",
    "SOURCE_NOT_FOUND" :  "No encontramos tu número Bim",
    "TARGET_NOT_FOUND" :  "El número al que envías dinero no tiene Bim",
    "TRANSFER_TYPE_AND_ACCOUNT_DO_NOT_MATCH" :  "El Bim que ingresaste no puede recibir dinero",
    "AUTHORIZATION_MAXIMUM_AMOUNT_TO_APPROVE" :  "Ya no puedes realizar más operaciones. Superaste el monto límite de S/4,000",
    "AUTHORIZATION_SENDER_ACCOUNT_NO_WITHDRAWAL" :  "No es posible realizar este retiro",
    "AUTHORIZATION_SENDER_ACCOUNT_NOT_ACTIVE" :  "El número al cual quieres enviar plata, no tiene Bim",
    "AUTHORIZATION_SENDER_MIN_ALLOWED_BALANCE" :  "La cantidad mínima por transacción es 1 sol",
    "AUTHORIZATION_SENDING_ACCOUNT_UNAVAILABLE" :  "El número es incorrecto",
    "AUTHORIZATION_INVALID_DEBIT" :  "La operación no es válida",
    "CAN_NOT_RECEIVE_CASHOUT" :  "El Bim que ingresaste no puede recibir dinero",
    "TRANSACTION_NOT_COMPLETED" :  "Te llegará un mensaje para confirmar tu operación",
    "RESOURCE NOT FOUND" :  "El Bim que ingresaste no es válido",
    "AUTHORIZATION_MAX_TRANSFER_ACCOUNT_THROUGHPUT_SENDER" :  "Llegaste a tu monto máximo. Comunícate con nostros al 080010838",
    "AUTHORIZATION_MAX_TRANSFER_ACCOUNT_THROUGHPUT_RECEIVER" :  "Llegaste a tu monto máximo. Comunícate con nostros al 080010838",
    "ACCOUNT_HOLDER_ALREADY_INITIATE_DEBIT" :  "No es posible realizar esta operación",
    "CREDENTIAL_NOT_ACTIVE" :  "No tienes acceso  a esta operación",
    "CREDENTIALS_NOT_FOUND" :  "No tienes acceso  a esta operación",
    "PINCODE_ALREADY_USED_BEFORE" :  "La clave ingresada no puede ser igual a la anterior",
    "PINCODE_HAS_EXPIRED" :  "Debes actualizar tu contraseña",
    "OTP_INVALID" :  "Revisa los datos que ingresaste",
    "OTP_NOT_FOUND" :  "Tu contraseña es incorrecta. Intenta de nuevo",
    "VALIDATION_ERROR" :  "Revisa los datos que ingresaste",
    "INTERNAL_ERROR":'Lo sentimos, algo salió mal',
    "REGISTERED_BLOCKED":'El usuario esta bloqueado',
    "BLOCKED":'El usuario esta bloqueado',
    "USER_ALREADY_INVITED_BY_AH":"Ya enviaste una invitación a este usuario"
}

def parse_error_ewp(data_json):
    try:
        err = errores
        for key in err.keys():
            a = str(data_json)
            if a.find(str(key)) != -1:
                return str(err[key])
        return errores['INTERNAL_ERROR']
    except Exception as e:
        print('Error', e)
        return errores['INTERNAL_ERROR']

def xml_to_dict_error(data_xml):
    data_xml = ET.fromstring(data_xml)
    data = xml_to_dict(data_xml)
    return data

def xml_to_dict(data_xml):
    data = {}
    # Extract attributes
    data.update(data_xml.attrib)
    
    # Process child elements
    for child in data_xml:
        child_data = xml_to_dict(child)
        tag = child.tag
        
        # Check if the tag already exists in the dictionary
        if tag in data:
            # If it does, convert the existing value to a list
            if not isinstance(data[tag], list):
                data[tag] = [data[tag]]
            # Append the new value to the list
            data[tag].append(child_data)
        else:
            # If the tag is encountered for the first time, set its value in the dictionary
            data[tag] = child_data
    
    # Process the text content of the element if it exists
    if data_xml.text and data_xml.text.strip():
        data['_text'] = data_xml.text.strip()
    
    return data
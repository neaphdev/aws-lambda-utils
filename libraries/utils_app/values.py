from libraries.utils.log import LoggerUtils

log = LoggerUtils.setup_logger(__name__)


# decorator that print the time it takes to execute the function
def get_balance_soles_active(account_details: list) -> dict:
    """account_details debe ser accountDetails de la respuesta del Core"""
    for account in account_details:
        account_currency = account["currency"]
        account_status = account["accountStatus"]
        if account_currency == 101 and account_status == "Y":
            return account
    raise ValueError("No hay cuenta activa con moneda Soles")


def get_balance_soles_active(account_details: list) -> dict:
    """account_details debe ser accountDetails de la respuesta del Core"""
    for account in account_details:
        account_currency = account["currency"]
        account_status = account["accountStatus"]
        if account_currency == 101 and account_status == "Y":
            return account
    raise ValueError("No hay cuenta activa con moneda Soles")
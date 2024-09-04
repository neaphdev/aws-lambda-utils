from libraries.utils.log import LoggerUtils

log = LoggerUtils.setup_logger(__name__)


def log_lambda_event(log_event: bool):
    """This decorator is used to log the event according to the environment."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if log_event:
                log.info("Lambda Event: %s", args)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_alldict_without_auth(
    request_event: dict,
    offuscate_keys: list = ["Authorization", "auth", "authorization", "token_user"],
) -> dict:
    filtered_dict = {}
    for key, value in request_event.items():
        if key not in offuscate_keys:
            filtered_dict[key] = value
        else:
            filtered_dict[key] = "****"
    return filtered_dict


def get_alldict_without_auth_core(request_event: dict) -> dict:

    return {
        "api_name": request_event.get("api_name", ""),
        "Authorization": "****",
        "data": request_event.get("data", {}),
    }

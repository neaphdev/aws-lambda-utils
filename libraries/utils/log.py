import logging
from dataclasses import dataclass, field


@dataclass
class LoggerSettings:
    """
    Clase que se encarga de manejar la configuracion del logger
    """

    log_config: dict = field(default_factory=dict)
    LOG_FORMAT: str = "[%(levelname)5s] - [%(name)s:%(lineno)d] - %(message)s"
    DEBUG: bool = True
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

    @classmethod
    def set_basic_config(cls, config: dict) -> None:
        """Configura el logger con la configuracion basica"""
        cls.log_config: dict = config.get("LOG_CONFIG", {})
        cls.LOG_FORMAT = cls.log_config.get("LOG_FORMAT", cls.LOG_FORMAT)
        cls.DEBUG = bool(cls.log_config.get("DEBUG"))
        cls.LOG_LEVEL = logging.DEBUG if cls.log_config else logging.INFO


class LoggerUtils:
    """
    Clase que se encarga de manejar el logger de la aplicacion
    """

    @classmethod
    def setup_logger(cls, name_logger: str, log_setting: LoggerSettings = LoggerSettings()) -> logging.Logger:
        """
        configura un logger personalizado con un manejador de transmisión que
        envía registros a la salida estándar con un formato específico y un
        nivel de registro específico
        :param name_logger: Nombre del archivo donde se usa el LOG
        :param log_setting: Configuracion del Logger
        :return: Objeto Logger con la configuracion personalizada
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_setting.LOG_LEVEL)
        formatter = logging.Formatter(log_setting.LOG_FORMAT)
        stream_handler.setFormatter(formatter)

        log = logging.getLogger(name_logger)
        log.setLevel(log_setting.LOG_LEVEL)
        log.addHandler(stream_handler)
        log.propagate = False

        return log

    # ruff: noqa: ANN401

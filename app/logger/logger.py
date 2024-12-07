# logger.py

import logging

# Configuración básica del logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)  # Establecer el nivel de log deseado (DEBUG, INFO, WARNING, etc.)

# Crear un manejador de archivo
file_handler = logging.FileHandler("app_logs.log")  # El archivo donde se guardarán los logs
file_handler.setLevel(logging.DEBUG)  # Nivel de log para el archivo

# Crear un formateador
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(file_handler)
import logging

logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
error_file_handler = logging.FileHandler('/home/vincent/e-paper/lib/app_error.log')
error_file_handler.setLevel(logging.ERROR) 

console_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
error_file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_formatter)
error_file_handler.setFormatter(error_file_formatter)

logger.addHandler(console_handler)
logger.addHandler(error_file_handler)

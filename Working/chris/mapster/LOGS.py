import json, os, logging, logging.config

def init_logging(default_path):
    default_level=logging.INFO
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = json.load(f)
            info_log = 'logs/{}'.format(config['handlers']['info_file_handler']['filename'])
            error_log = 'logs/{}'.format(config['handlers']['error_file_handler']['filename'])
            config['handlers']['info_file_handler']['filename'] = info_log
            config['handlers']['error_file_handler']['filename'] = error_log
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


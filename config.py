import os
import json

config_path = 'config.json'

TELEGRAM_TOKEN = ''
target_channel_id = ''


def get_bot_id():
    return TELEGRAM_TOKEN.split(":")[0]


def load_config():
    global TELEGRAM_TOKEN, target_channel_id

    try:
        with open(config_path, 'r') as file:
            config = json.loads(file.read())

            TELEGRAM_TOKEN = config['token']
            target_channel_id = config['target_channel_id']

    except Exception as exception:
        # если файла нету, будет записываться пустая структура
        write_config()
        raise exception


def write_config():
    config = dict()
    config['token'] = TELEGRAM_TOKEN
    config['target_channel_id'] = target_channel_id

    with open(config_path, 'w') as file:
        file.write(json.dumps(config, indent=5, sort_keys=True))

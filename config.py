import os
import json

config_path = 'config.json'

TOKEN = ''
superadmin_username = ''
target_channel_id = ''
target_log_chat_ids = []
VK_TOKEN = ''
vk_group_id = ''


def get_bot_id():
    return TOKEN.split(":")[0]


def load_config():
    global TOKEN, superadmin_username, target_channel_id, target_log_chat_ids, VK_TOKEN, vk_group_id

    try:
        with open(config_path, 'r') as file:
            config = json.loads(file.read())

            TOKEN = config['token']
            superadmin_username = config['superadmin_username']
            target_channel_id = config['target_channel_id']
            target_log_chat_ids = config['target_log_chat_ids']
            VK_TOKEN = config['vk_token']
            vk_group_id = config['vk_group_id']

    except Exception as exception:
        # если файла нету, будет записываться пустая структура
        write_config()
        raise exception


def write_config():
    config = dict()
    config['token'] = TOKEN
    config['superadmin_username'] = superadmin_username
    config['target_channel_id'] = target_channel_id
    config['target_log_chat_ids'] = target_log_chat_ids
    config['vk_token'] = VK_TOKEN
    config['vk_group_id'] = vk_group_id

    with open(config_path, 'w') as file:
        file.write(json.dumps(config, indent=5, sort_keys=True))

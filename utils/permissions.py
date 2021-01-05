import config


def is_admin(username: str) -> bool:
    if username == config.superadmin_username:
        return True

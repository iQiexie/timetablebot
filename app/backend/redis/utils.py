from config import settings


def compose_key(*args):
    return settings.REDIS_SEP.join(args)

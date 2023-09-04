from multiprocessing import cpu_count

from uvicorn.workers import UvicornWorker


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "port": 8080,
        "reload": True,
        "factory": True,
        "host": "0.0.0.0",  # noqa: S104
        "proxy_headers": True,
    }


workers = cpu_count()

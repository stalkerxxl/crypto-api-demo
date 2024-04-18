import inspect
import logging
import os
import timeit
from functools import wraps
from logging.handlers import TimedRotatingFileHandler

from app.config import LOG_LEVEL, LOG_FOLDER, APP_DEBUG


def __sync_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if APP_DEBUG:
            start_time = timeit.default_timer()
            result = func(*args, **kwargs)
            end_time = timeit.default_timer()
            execution_time = end_time - start_time
            print(f"sync {func.__name__}() timer: {execution_time:.6f}s")
            return result
        else:
            return func(*args, **kwargs)

    return wrapper


def __async_timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if APP_DEBUG:
            start_time = timeit.default_timer()
            result = await func(*args, **kwargs)
            end_time = timeit.default_timer()
            execution_time = end_time - start_time
            print(f"async {func.__name__}() timer: {execution_time:.6f}s")
            return result
        else:
            return await func(*args, **kwargs)

    return wrapper


def timer(func):
    if inspect.iscoroutinefunction(func):
        return __async_timer(func)
    else:
        return __sync_timer(func)


def get_logger(name: str = 'main'):
    my_logger = logging.getLogger(name)
    my_logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def create_log_folder(folder=LOG_FOLDER):
        if not os.path.exists(folder):
            os.mkdir(folder)

    create_log_folder()

    fh = TimedRotatingFileHandler(
        filename=f'{LOG_FOLDER}/{name}.log',
        when='midnight',
        interval=1,
        encoding='utf-8'
    )
    fh.setFormatter(file_formatter)
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(file_formatter)
    ch.setLevel(logging.getLevelName(LOG_LEVEL))

    my_logger.addHandler(fh)
    my_logger.addHandler(ch)
    return my_logger

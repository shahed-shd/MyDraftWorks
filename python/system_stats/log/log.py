import logging
import queue
from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler

from .relative_pathname_setter_filter import RelativePathnameSetterFilter


class Log:
    """Wrapper for Logger to prepare the logger and has some additional features."""

    iso_datetime_format = '%Y-%m-%dT%H:%M:%S%z'
    sep = ' | '

    compact_format = sep.join(('%(asctime)s', '%(name)s', '%(levelname)8s', '%(message)s'))
    compact_formatter = logging.Formatter(compact_format, datefmt=iso_datetime_format)

    verbose_format = sep.join(('%(asctime)s', '%(name)s', '%(process)d', '%(thread)d', '%(threadName)s', '%(filename)s:%(lineno)d', '%(levelname)s', '%(message)s'))
    verbose_formatter = logging.Formatter(verbose_format, datefmt=iso_datetime_format)


    def __init__(self, *, logger_name, level=logging.DEBUG):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        self.__logger = logger


    @property
    def logger(self):
        return self.__logger


    def set_level(self, level):
        self.__logger.setLevel(level)


    def add_console_handler(self, *, level=logging.DEBUG, formatter=compact_formatter):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)


    def add_persistent_log_handler(self, *, level=logging.DEBUG, formatter=verbose_formatter, filename):
        handler = self._construct_persistent_handler(level=level, filename=filename)
        handler.setFormatter(formatter)

        queue_handler, queue_listener = self._integrate_queue(handler)

        self.__logger.addHandler(queue_handler)
        queue_listener.start()


    def add_persistent_log_handler_with_relative_pathname_formatter(self, *, level=logging.DEBUG, relative_path_start_dir, filename):
        handler = self._construct_persistent_handler(level=level, filename=filename)

        verbose_with_relative_pathname_format = self.verbose_format.replace('filename', 'relative_pathname')
        verbose_with_relative_pathname_formatter = logging.Formatter(verbose_with_relative_pathname_format, datefmt=self.iso_datetime_format)

        handler.setFormatter(verbose_with_relative_pathname_formatter)
        handler.addFilter(RelativePathnameSetterFilter(relative_path_start_dir=relative_path_start_dir, name=self.__logger.name))

        queue_handler, queue_listener = self._integrate_queue(handler)

        self.__logger.addHandler(queue_handler)
        queue_listener.start()


    @staticmethod
    def _construct_persistent_handler(level: int, filename: str) -> TimedRotatingFileHandler:
        handler = TimedRotatingFileHandler(filename=filename, when='midnight', backupCount=365, delay=True)
        handler.setLevel(level)
        return handler


    @staticmethod
    def _integrate_queue(handler: logging.Handler) -> tuple[QueueHandler, QueueListener]:
        que = queue.Queue(-1)
        queue_handler = QueueHandler(que)
        queue_listener = QueueListener(que, handler)

        return queue_handler, queue_listener


    def __repr__(self):
        level = logging.getLevelName(self.__logger.getEffectiveLevel())
        return f'{self.__class__.__name__}(logger_name={self.__logger.name}, level={level})'

import logging
import os


class RelativePathnameSetterFilter(logging.Filter):
    def __init__(self, relative_path_start_dir: str, name: str = ''):
        self.package_dir_name = relative_path_start_dir
        super().__init__(name=name)


    def filter(self, record: logging.LogRecord):
        pathname = record.pathname
        idx = pathname.find(os.sep + self.package_dir_name + os.sep)
        record.relative_pathname = pathname if idx == -1 else pathname[idx + 1:]
        return True

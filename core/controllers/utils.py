#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import logging


def download(url, file_path, file_name):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    jar_path = os.path.join(file_path, file_name)
    if not os.path.exists(jar_path):
        logging.info("{0} not exist. Try to download from {1}.".format(file_name, url))
        stat = os.system("curl -L -o {1} {0}".format(url, jar_path))
        if stat != 0:
            logging.error("Download failed.")
            return False, jar_path
    return True, jar_path


if __name__ == '__main__':
    pass

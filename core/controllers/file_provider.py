#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import os
import re

import apksec_exceptions


class FileProvider(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FileProvider, cls).__new__(cls, *args, **kwargs)
            cls._instance.files = {}
            cls._instance.unpackers = []
        return cls._instance

    def register_unpacker(self, unpacker_name):
        logging.info("Unpacker: {} registered.".format(unpacker_name))
        self.unpackers.append(unpacker_name)

    def get_files(self, unpacker, regex=None, magic=None):
        """

        :param unpacker: unpacker类，用来获取某个unpacker文件夹下的类型文件
        :param regex: 使用正则表达式搜索，带路径，建议使用原始字符串
        :param magic: 使用文件头的magic搜索，请使用字符串形式，如'\x03\x00\x08\x00'
        :return:
        """
        if unpacker not in self.unpackers:
            err_str = "Unpacker: '{}' not in registered unpackers.".format(unpacker)
            logging.error(err_str)
            raise apksec_exceptions.FileProviderException(err_str)

        # 缓存机制
        key = '{0}_{1}'.format(unpacker, regex if magic is None else magic)
        if key in self.files.keys():
            return self.files[key]

        res = []
        search_dir = unpacker.plugin_task_path
        if regex:
            pattern = re.compile(regex)
            for root, dirs, files in os.walk(search_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    if pattern.match(file_path):
                        res.append(file_path)
        elif magic:
            for root, dirs, files in os.walk(search_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    with open(file_path, 'r') as _file:
                        file_magic = _file.read(12)
                        if file_magic.startswith(magic):
                            res.append(file_path)

        self.files[key] = res
        return res

    def get_files_by_type(self, file_type):
        """
        选择一个恰当的unpacker并返回其结果
        :param file_type:
        :return:
        """
        unpackers = filter(lambda e: file_type in e.ability.keys(), self.unpackers)
        unpackers.sort(key=lambda e: -e.ability[file_type].value)

        for each_unpacker in unpackers:
            if len(each_unpacker.failed_files) == 0:
                return self.get_files(each_unpacker, regex='.*' + file_type.value)
        return self.get_files(unpackers[0], regex='.*' + file_type.value)


if __name__ == '__main__':
    fp = FileProvider()

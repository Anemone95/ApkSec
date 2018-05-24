#!/usr/bin/env python
# -*- coding=utf-8 -*-


class PluginException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


class FileProviderException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


class ApkCheckerException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


class UnpackerException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


class AuditorException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


class TaskInfoException(Exception):
    def __init__(self, error_str):
        Exception.__init__(self, error_str)


if __name__ == '__main__':
    pass

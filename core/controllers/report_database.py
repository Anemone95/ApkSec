#!/usr/bin/env python
# -*- coding=utf-8 -*-
from core.controllers.decorator import singleton


@singleton
class ReportDatabase(object):
    def __init__(self):
        self.database = []

    def filter(self, name=None, plugin_name=None):
        ret = self.database
        if name:
            ret = filter(lambda report: report.vulnerability.name == name, ret)
        if plugin_name:
            ret = filter(lambda report: report.plugin_name == plugin_name, ret)
        return ret

    def add(self, report):
        self.database.append(report)

    def list_database(self):
        return self.database


if __name__ == '__main__':
    t1 = ReportDatabase()
    t1.add("AAA")
    t2 = ReportDatabase()
    t2.add("BBB")

    print ReportDatabase().list_database()

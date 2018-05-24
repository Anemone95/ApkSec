#!/usr/bin/env python
# -*- coding=utf-8 -*-
# from core.controllers import plugin_category
import logging
import core.controllers.plugin_category as plugin_category
from core.controllers.vulnerability import Reference


class MobSF_SRC(plugin_category.Auditor):
    def register_vulns(self):
        self.register_vuln(name="test", i18n_name="test", description="Audit plugin example.", solution="",
                           risk_level=0)

    def start(self):
        pass
        # print self.file_provider.get_java_files()
        # java_files = self.file_provider.get_files("Jadx", regex=".*\.java")
        # logging.info("TestAuditor run.")
        # for each in java_files:
        #     self.report_vuln("test", Reference(location=each))


if __name__ == '__main__':
    pass

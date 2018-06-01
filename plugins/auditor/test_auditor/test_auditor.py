#!/usr/bin/env python
# -*- coding=utf-8 -*-
# from core.controllers import plugin_category
import core.controllers.plugin_category as plugin_category
from core.controllers.vulnerability import Reference
from core.controllers.const import RISK


class TestAuditor(plugin_category.Auditor):
    def register_vulns(self):
        self.register_vuln(name="test", i18n_name="test", category="ttt", description="Audit plugin example.",
                           solution="sss",
                           risk_level=RISK.INFO)

    def start(self):
        # self.report_vuln("test", Reference(location='aaa'))
        pass


if __name__ == '__main__':
    pass

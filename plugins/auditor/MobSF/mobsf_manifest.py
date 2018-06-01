#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
插件入口
"""
import json
import logging
from xml.dom import minidom

import os

import core.controllers.plugin_category as plugin_category
from core.controllers.const import TYPE
from core.controllers.vulnerability import Reference
from plugins.auditor.MobSF import mobsf_vulns_db
from plugins.auditor.MobSF.code_analysis import code_analysis
from plugins.auditor.MobSF.manifest_analysis import manifest_analysis, manifest_data


class MobSF_Manifest(plugin_category.Auditor):
    def register_vulns(self):
        for each_vuln in mobsf_vulns_db.vulns.keys():
            self.register_vuln(mobsf_vulns_db.vulns[each_vuln])

    def start(self):
        manifest_file = self.file_provider.get_files_by_type(TYPE.MANIFEST)[0]
        parsed_xml = minidom.parse(manifest_file)
        man_data_dic = manifest_data(parsed_xml)
        man_an_list = manifest_analysis(parsed_xml, man_data_dic)
        for each_vuln in man_an_list:
            if each_vuln["name"] in mobsf_vulns_db.vulns.keys():
                self.report_vuln(mobsf_vulns_db.vulns[each_vuln['name']], reference=Reference('androidmanifest.xml'))
        jfiles = self.file_provider.get_files_by_type(TYPE.JAVA)
        code_an_dic = code_analysis(jfiles, man_data_dic['perm'])
        for each_vuln_key in code_an_dic['findings']:
            if each_vuln_key in mobsf_vulns_db.vulns.keys():
                for each_path in code_an_dic['findings'][each_vuln_key]['path']:
                    self.report_vuln(mobsf_vulns_db.vulns[each_vuln_key],
                                     reference=Reference(
                                         os.path.relpath(each_path,
                                                         os.path.join(self.task_path, 'unpacker', 'JavaCollector'))))
            else:
                logging.debug("{vuln_name} not in database.".format(vuln_name=each_vuln_key))


if __name__ == '__main__':
    pass

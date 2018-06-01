# -*- coding: utf_8 -*-
"""Module holding the functions for code analysis."""

import shutil
import sys

import android_apis
import android_rules
from shared_func import *

SKIP_CLASSES = [
    r'android[\\\/]{1}support[\\\/]{1}', r'com[\\\/]{1}google[\\\/]{1}', r'android[\\\/]{1}content[\\\/]{1}',
    r'com[\\\/]{1}android[\\\/]{1}', r'com[\\\/]{1}facebook[\\\/]{1}', r'com[\\\/]{1}twitter[\\\/]{1}',
    r'twitter4j[\\\/]{1}', r'org[\\\/]{1}apache[\\\/]{1}', r'com[\\\/]{1}squareup[\\\/]{1}okhttp[\\\/]{1}',
    r'oauth[\\\/]{1}signpost[\\\/]{1}', r'org[\\\/]{1}chromium[\\\/]{1}'
]


def code_analysis(jfiles, perms):
    """Perform the code analysis."""
    try:
        logging.info("Static Android Code Analysis Started")
        api_rules = android_apis.APIS
        code_rules = android_rules.RULES
        code_findings = {}
        api_findings = {}
        email_n_file = []
        url_n_file = []
        url_list = []
        domains = {}

        # pylint: disable=unused-variable
        # Needed by os.walk
        for jfile_path in jfiles:
            dat = ''
            try:
                with io.open(
                        jfile_path,
                        mode='r',
                        encoding="utf8",
                        errors="ignore"
                ) as file_pointer:
                    dat = file_pointer.read()
            except IOError:
                sys.stderr.write(jfile_path)

            # Code Analysis
            relative_java_path = jfile_path
            code_rule_matcher(
                code_findings, perms.keys(), dat, relative_java_path, code_rules)
            # API Check
            api_rule_matcher(api_findings, perms.keys(),
                             dat, relative_java_path, api_rules)
            # Extract URLs and Emails
            urls, urls_nf, emails_nf = url_n_email_extract(dat, relative_java_path)
            url_list.extend(urls)
            url_n_file.extend(urls_nf)
            email_n_file.extend(emails_nf)
        code_an_dic = {
            'api': api_findings,
            'findings': code_findings,
            'urls': url_n_file,
            'emails': email_n_file,
        }
        return code_an_dic
    except:
        logging.error(traceback.format_exc())
        raise AuditorException("Performing Code Analysis Error")

#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
包含MobSF的代码检测逻辑，被code_analysis.py调用
"""
import logging
import os
import hashlib
import io
import re
import traceback

from core.controllers.apksec_exceptions import AuditorException


def PrintException(exc):
    logging.error(traceback.format_exc())
    raise AuditorException(exc)


def file_size(app_path):
    """Return the size of the file."""
    return round(float(os.path.getsize(app_path)) / (1024 * 1024), 2)


def hash_gen(app_path):
    """Generate and return sha1 and sha256 as a tupel."""
    try:
        logging.debug("Generating Hashes")
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()
        block_size = 65536
        with io.open(app_path, mode='rb') as afile:
            buf = afile.read(block_size)
            while buf:
                sha1.update(buf)
                sha256.update(buf)
                buf = afile.read(block_size)
        sha1val = sha1.hexdigest()
        sha256val = sha256.hexdigest()
        return sha1val, sha256val
    except:
        PrintException("[ERROR] Generating Hashes")


def get_list_match_items(ruleset):
    """Get List of Match item"""
    match_list = []
    i = 1
    identifier = ruleset["type"]
    if ruleset["match"] == 'string_and_or':
        identifier = 'string_or'
    elif ruleset["match"] == 'string_or_and':
        identifier = 'string_and'
    while identifier + str(i) in ruleset:
        match_list.append(ruleset[identifier + str(i)])
        i = i + 1
        if identifier + str(i) in ruleset == False:
            break
    return match_list


def add_findings(findings, desc, file_path, level):
    """Add Code Analysis Findings"""
    if desc in findings:
        tmp_list = findings[desc]["path"]
        if escape(file_path) not in tmp_list:
            tmp_list.append(escape(file_path))
            findings[desc]["path"] = tmp_list
    else:
        findings[desc] = {"path": [escape(file_path)], "level": level}


def code_rule_matcher(findings, perms, data, file_path, code_rules):
    """Android Static Analysis Rule Matcher"""
    try:
        for rule in code_rules:

            # CASE CHECK
            if rule["input_case"] == "lower":
                tmp_data = data.lower()
            elif rule["input_case"] == "upper":
                tmp_data = data.upper()
            elif rule["input_case"] == "exact":
                tmp_data = data

            # MATCH TYPE
            if rule["type"] == "regex":
                if rule["match"] == 'single_regex':
                    if re.findall(rule["regex1"], tmp_data):
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'regex_and':
                    and_match_rgx = True
                    match_list = get_list_match_items(rule)
                    for match in match_list:
                        if bool(re.findall(match, tmp_data)) is False:
                            and_match_rgx = False
                            break
                    if and_match_rgx:
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'regex_or':
                    match_list = get_list_match_items(rule)
                    for match in match_list:
                        if re.findall(match, tmp_data):
                            add_findings(findings, rule[
                                "desc"], file_path, rule["level"])
                            break
                elif rule["match"] == 'regex_and_perm':
                    if (rule["perm"] in perms) and (re.findall(rule["regex1"], tmp_data)):
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                else:
                    logging.error("[ERROR] Code Regex Rule Match Error: " + rule)

            elif rule["type"] == "string":
                if rule["match"] == 'single_string':
                    if rule["string1"] in tmp_data:
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'string_and':
                    and_match_str = True
                    match_list = get_list_match_items(rule)
                    for match in match_list:
                        if (match in tmp_data) is False:
                            and_match_str = False
                            break
                    if and_match_str:
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'string_or':
                    match_list = get_list_match_items(rule)
                    for match in match_list:
                        if match in tmp_data:
                            add_findings(findings, rule[
                                "desc"], file_path, rule["level"])
                            break
                elif rule["match"] == 'string_and_or':
                    match_list = get_list_match_items(rule)
                    string_or_stat = False
                    for match in match_list:
                        if match in tmp_data:
                            string_or_stat = True
                            break
                    if string_or_stat and (rule["string1"] in tmp_data):
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'string_or_and':
                    match_list = get_list_match_items(rule)
                    string_and_stat = True
                    for match in match_list:
                        if match in tmp_data is False:
                            string_and_stat = False
                            break
                    if string_and_stat or (rule["string1"] in tmp_data):
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'string_and_perm':
                    if (rule["perm"] in perms) and (rule["string1"] in tmp_data):
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                elif rule["match"] == 'string_or_and_perm':
                    match_list = get_list_match_items(rule)
                    string_or_ps = False
                    for match in match_list:
                        if match in tmp_data:
                            string_or_ps = True
                            break
                    if (rule["perm"] in perms) and string_or_ps:
                        add_findings(findings, rule[
                            "desc"], file_path, rule["level"])
                else:
                    logging.error("[ERROR] Code String Rule Match Error: " + rule)

            else:
                logging.error("[ERROR] Code String Rule Match Error: " + rule)
    except:
        PrintException("[ERROR] Error in Code Rule Processing")


def add_apis(api_findings, desc, file_path):
    """Add API Findings"""
    if desc in api_findings:
        tmp_list = api_findings[desc]["path"]
        if escape(file_path) not in tmp_list:
            tmp_list.append(escape(file_path))
            api_findings[desc]["path"] = tmp_list
    else:
        api_findings[desc] = {"path": [escape(file_path)]}


def api_rule_matcher(api_findings, perms, data, file_path, api_rules):
    """Android API Analysis Rule Matcher"""
    try:
        for api in api_rules:

            # CASE CHECK
            if api["input_case"] == "lower":
                tmp_data = data.lower()
            elif api["input_case"] == "upper":
                tmp_data = data.upper()
            elif api["input_case"] == "exact":
                tmp_data = data

            # MATCH TYPE
            if api["type"] == "regex":
                if api["match"] == 'single_regex':
                    if re.findall(api["regex1"], tmp_data):
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'regex_and':
                    and_match_rgx = True
                    match_list = get_list_match_items(api)
                    for match in match_list:
                        if bool(re.findall(match, tmp_data)) is False:
                            and_match_rgx = False
                            break
                    if and_match_rgx:
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'regex_or':
                    match_list = get_list_match_items(api)
                    for match in match_list:
                        if re.findall(match, tmp_data):
                            add_apis(api_findings, api["desc"], file_path)
                            break
                elif api["match"] == 'regex_and_perm':
                    if (api["perm"] in perms) and (re.findall(api["regex1"], tmp_data)):
                        add_apis(api_findings, api["desc"], file_path)
                else:
                    logging.error("[ERROR] API Regex Rule Match Error: " + api)

            elif api["type"] == "string":
                if api["match"] == 'single_string':
                    if api["string1"] in tmp_data:
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'string_and':
                    and_match_str = True
                    match_list = get_list_match_items(api)
                    for match in match_list:
                        if (match in tmp_data) is False:
                            and_match_str = False
                            break
                    if and_match_str:
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'string_or':
                    match_list = get_list_match_items(api)
                    for match in match_list:
                        if match in tmp_data:
                            add_apis(api_findings, api["desc"], file_path)
                            break
                elif api["match"] == 'string_and_or':
                    match_list = get_list_match_items(api)
                    string_or_stat = False
                    for match in match_list:
                        if match in tmp_data:
                            string_or_stat = True
                            break
                    if string_or_stat and (api["string1"] in tmp_data):
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'string_or_and':
                    match_list = get_list_match_items(api)
                    string_and_stat = True
                    for match in match_list:
                        if match in tmp_data is False:
                            string_and_stat = False
                            break
                    if string_and_stat or (api["string1"] in tmp_data):
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'string_and_perm':
                    if (api["perm"] in perms) and (api["string1"] in tmp_data):
                        add_apis(api_findings, api["desc"], file_path)
                elif api["match"] == 'string_or_and_perm':
                    match_list = get_list_match_items(api)
                    string_or_ps = False
                    for match in match_list:
                        if match in tmp_data:
                            string_or_ps = True
                            break
                    if (api["perm"] in perms) and string_or_ps:
                        add_apis(api_findings, api["desc"], file_path)
                else:
                    logging.error("[ERROR] API String Rule Match Error:" + api)
            else:
                logging.error("[ERROR] API Rule Error:" + api)
    except:
        PrintException("[ERROR] Error in API Rule Processing")


def url_n_email_extract(dat, relative_path):
    """Extract URLs and Emails from Source Code"""
    urls = []
    emails = []
    urllist = []
    url_n_file = []
    email_n_file = []
    # URLs Extraction My Custom regex
    pattern = re.compile(
        (
            ur'((?:https?://|s?ftps?://|file://|javascript:|data:|www\d{0,3}[.])'
            ur'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
        ),
        re.UNICODE
    )
    urllist = re.findall(pattern, dat.lower())
    uflag = 0
    for url in urllist:
        if url not in urls:
            urls.append(url)
            uflag = 1
    if uflag == 1:
        url_n_file.append(
            {"urls": urls, "path": escape(relative_path)})

    # Email Extraction Regex
    regex = re.compile(r'[\w.-]+@[\w-]+\.[\w.]+')
    eflag = 0
    for email in regex.findall(dat.lower()):
        if (email not in emails) and (not email.startswith('//')):
            emails.append(email)
            eflag = 1
    if eflag == 1:
        email_n_file.append(
            {"emails": emails, "path": escape(relative_path)})
    return urllist, url_n_file, email_n_file


def escape(_str):
    return _str

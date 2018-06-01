#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
将MobSF报出的漏洞类型转换为系统内部定义类型
"""

from core.controllers.vuln_db import *

vulns = {
    'a_debuggable': V_DEBUGGABLE,
    'a_allowbackup': V_BACKUP,
    'a_allowbackup_miss': V_BACKUP,
    'Files may contain hardcoded sensitive informations like usernames, passwords, keys etc.': V_INFO_LEAKAGE,
    'IP Address disclosure': V_INFO_LEAKAGE,
    'The App uses ECB mode in Cryptographic encryption algorithm. '
    'ECB mode is known to be weak as it results in the same ciphertext for identical blocks of plaintext.': V_ECB_MODE,
    'Insecure Implementation of SSL. '
    'Trusting all the certificates or accepting self signed certificates is a critical Security Hole. '
    'This application is vulnerable to MITM attacks': V_HOST_WEAK_VERIFY,
    'The file is World Readable. Any App can read from the file': V_FILE_READABLE,
    'The file is World Writable. Any App can write to the file': V_FILE_WRITEABLE,
    'The file is World Readable and Writable. Any App can read/write to the file': V_FILE_READABLE_AND_WRITEABLE,
    'Weak Hash algorithm used': V_WEAK_HASH,
    'The App uses an insecure Random Number Generator.': V_WEAK_RANDOM,
    'The App logs information. Sensitive information should never be logged.': V_LOG_LEAKAGE,
    'Insecure WebView Implementation. '
    'Execution of user controlled code in WebView is a critical Security Hole.': V_WEBVIEW_JS,
    'The App may use weak IVs like "0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00" '
    'or "0x01,0x02,0x03,0x04,0x05,0x06,0x07". '
    'Not using a random IV makes the resulting ciphertext much more predictable '
    'and susceptible to a dictionary attack.': V_INSECURE_IV,
    'Insecure WebView Implementation. WebView ignores SSL Certificate errors and accept any SSL Certificate. '
    'This application is vulnerable to MITM attacks': V_WEBVIEW_SSL,
}

if __name__ == '__main__':
    print len(vulns)

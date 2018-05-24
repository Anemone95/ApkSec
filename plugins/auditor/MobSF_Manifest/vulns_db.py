#!/usr/bin/env python
# -*- coding=utf-8 -*-
from core.controllers.const import RISK

vulns = {
    'a_debuggable': {
        'name': 'debuggable',
        'i18n_name': u'程序可被任意调试',
        'description': u'在manifest.xml中定义Debuggable项，如果该项被打开，app存在被恶意程序调试的风险，可能导致泄漏敏感信息泄漏等问题。',
        'solution': u'显示的设置manifest的debuggable标志为false',
        'risk_level': RISK.HIGH,
    }
}

if __name__ == '__main__':
    pass

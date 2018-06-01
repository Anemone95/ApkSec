#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
定义Manifest存在的问题
"""
import re

manifest_desc = {
    'a_debuggable': (
        'Debug Enabled For App <br>[android:debuggable=true]',
        'high',
        'Debugging was enabled on the app which makes it easier for reverse engineers to hook a '
        'debugger to it. This allows dumping a stack trace and accessing debugging helper classes.'
    ),
    'a_allowbackup': (
        'Application Data can be Backed up<br>[android:allowBackup=true]',
        'medium',
        'This flag allows anyone to backup your application data via adb. It allows users who have'
        ' enabled USB debugging to copy application data off of the device.'
    ),
    'a_allowbackup_miss': (
        'Application Data can be Backed up<br>[android:allowBackup] flag is missing.',
        'medium',
        'The flag [android:allowBackup] should be set to false. By default it is set to true and '
        'allows anyone to backup your application data via adb. It allows users who have enabled '
        'USB debugging to copy application data off of the device.'
    ),
    'a_testonly': (
        'Application is in Test Mode <br>[android:testOnly=true]',
        'high',
        ' It may expose functionality or data outside of itself that would cause a security hole.'
    ),
    'a_taskaffinity': (
        'TaskAffinity is set for Activity </br>(%s)',
        'high',
        'If taskAffinity is set, then other application could read the Intents sent to Activities'
        ' belonging to another task. Always use the default setting keeping the affinity as the '
        'package name in order to prevent sensitive information inside sent or received Intents '
        'from being read by another application.'
    ),
    'a_launchmode': (
        'Launch Mode of Activity (%s) is not standard.',
        'high',
        'An Activity should not be having the launch mode attribute set to "singleTask/singleInstance"'
        ' as it becomes root Activity and it is possible for other applications to read the contents'
        ' of the calling Intent. So it is required to use the "standard" launch mode attribute when'
        ' sensitive information is included in an Intent.'
    ),
    'a_prot_sign': (
        '<strong>%s</strong> (%s) is Protected by a permission.</br>%s<br>[android:exported=true]',
        'info',
        'A%s %s is found to be exported, but is protected by permission.'
    ),
    'a_prot_normal': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of '
        'the permission should be checked.</br>%s <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission. However,'
        ' the protection level of the permission is set to normal. This means that a malicious'
        ' application can request and obtain the permission and interact with the component.'
        ' If it was set to signature, only applications signed with the same certificate could'
        ' obtain the permission.'
    ),
    'a_prot_danger': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of '
        'the permission should be checked.</br>%s <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission. However,'
        ' the protection level of the permission is set to dangerous. This means that a'
        ' malicious application can request and obtain the permission and interact with the'
        ' component. If it was set to signature, only applications signed with the same'
        ' certificate could obtain the permission.'
    ),
    'a_prot_sign_sys': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of '
        'the permission should be checked.</br>%s <br>[android:exported=true]',
        'info',
        'A%s %s is found to be exported, but is protected by a permission. However, the'
        ' protection level of the permission is set to signatureOrSystem. It is recommended that'
        ' signature level is used instead. Signature level should suffice for most purposes, and'
        ' does not depend on where the applications are installed on the device.'
    ),
    'a_prot_unknown': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of '
        'the permission should be checked.</br>%s <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission which is not'
        ' defined in the analysed application. As a result, the protection level of the'
        ' permission should be checked where it is defined. If it is set to normal or'
        ' dangerous, a malicious application can request and obtain the permission and interact'
        ' with the component. If it is set to signature, only applications signed with the same'
        ' certificate can obtain the permission.'
    ),
    'a_prot_normal_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked.</br>%s'
        ' <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device.  It is protected by a permission at the application'
        ' level. However, the protection level of the permission is set to normal. This means that'
        ' a malicious application can request and obtain the permission and interact with the'
        ' component. If it was set to signature, only applications signed with the same certificate'
        ' could obtain the permission.'
    ),
    'a_prot_danger_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked.</br>%s'
        ' <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission at the'
        ' application level. However, the protection level of the permission is set to'
        ' dangerous. This means that a malicious application can request and obtain the'
        ' permission and interact with the component. If it was set to signature, only'
        ' applications signed with the same certificate could obtain the permission.'
    ),
    'a_prot_sign_appl': (
        '<strong>%s</strong> (%s)  Protected by a permission at the application level.</br>%s'
        '<br>[android:exported=true]',
        'info',
        'A%s %s is found to be exported, but is protected by a permission at the application level.'
    ),
    'a_prot_sign_sys_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level, but'
        ' the protection level of the permission should be checked.</br>%s'
        ' <br>[android:exported=true]',
        'info',
        'A%s %s is found to be exported, but is protected by a permission at the application'
        ' level. However, the protection level of the permission is set to signatureOrSystem.'
        ' It is recommended that signature level is used instead. Signature level should'
        ' suffice for most purposes, and does not depend on where the applications are'
        ' installed on the device.'
    ),
    'a_prot_unknown_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application, but the'
        ' protection level of the permission should be checked.</br>%s'
        ' <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission at the'
        ' application level which is not defined in the analysed application. As a result,'
        ' the protection level of the permission should be checked where it is defined.'
        ' If it is set to normal or dangerous, a malicious application can request and'
        ' obtain the permission and interact with the component. If it is set to signature,'
        ' only applications signed with the same certificate can obtain the permission.'
    ),
    'a_not_protected': (
        '<strong>%s</strong> (%s) is not Protected. <br>[android:exported=true]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device.'
    ),
    'a_not_protected_filter': (
        '<strong>%s</strong> (%s) is not Protected.<br>An intent-filter exists.',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. The presence of intent-filter indicates that the '
        '%s is explicitly exported.'
    ),
    'c_not_protected': (
        '<strong>%s</strong> (%s) is not Protected. <br>[[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is a Content Provider that targets an API'
        ' level under 17, which makes it exported by default, regardless of the API level of'
        ' the system that the application runs on.'
    ),
    'c_not_protected2': (
        '<strong>%s</strong> (%s) would not be Protected if the application ran on a device where'
        ' the the API level was less than 17. <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider(%s %s) would be exported if the application ran on a device where'
        ' the the API level was less than 17. In that situation, it would be shared with other'
        ' apps on the device therefore leaving it accessible to any other application on the'
        ' device.'
    ),
    'c_prot_normal': (
        '<strong>%s</strong> (%s) is Protected by a permission, but'
        ' the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission. However,'
        ' the protection level of the permission is set to normal. This means that a malicious'
        ' application can request and obtain the permission and interact with the component.'
        ' If it was set to signature, only applications signed with the same certificate could'
        ' obtain the permission.'
    ),
    'c_prot_danger': (
        '<strong>%s</strong> (%s) is Protected by a permission, but'
        ' the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission. However,'
        ' the protection level of the permission is set to dangerous. This means that a'
        ' malicious application can request and obtain the permission and interact with the'
        ' component. If it was set to signature, only applications signed with the same'
        ' certificate could obtain the permission.'
    ),
    'c_prot_sign': (
        '<strong>%s</strong> (%s) is Protected by a permission.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'info',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by permission.'
    ),
    'c_prot_sign_sys': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of'
        ' the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'info',
        'A%s %s is found to be exported, but is protected by a permission. However, the'
        ' protection level of the permission is set to signatureOrSystem. It is recommended that'
        ' signature level is used instead. Signature level should suffice for most purposes, and'
        ' does not depend on where the applications are installed on the device.'
    ),
    'c_prot_unknown': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of '
        'the permission should be checked.</br>%s <br>[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission which is not'
        ' defined in the analysed application. As a result, the protection level of the'
        ' permission should be checked where it is defined. If it is set to normal or'
        ' dangerous, a malicious application can request and obtain the permission and interact'
        ' with the component. If it is set to signature, only applications signed with the same'
        ' certificate can obtain the permission.'
    ),
    'c_prot_normal_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level, but'
        ' the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission at the'
        ' application level. However, the protection level of the permission is set to normal.'
        ' This means that a malicious application can request and obtain the permission'
        ' and interact with the component. If it was set to signature, only applications'
        ' signed with the same certificate could obtain the permission.'
    ),
    'c_prot_danger_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level, but'
        ' the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by a permission at the'
        ' application level. However, the protection level of the permission is set to dangerous.'
        ' This means that a malicious application can request and obtain the permission'
        ' and interact with the component. If it was set to signature, only applications'
        ' signed with the same certificate could obtain the permission.'
    ),
    'c_prot_sign_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'info',
        'A%s %s is found to be shared with other apps on the device therefore leaving it accessible'
        ' to any other application on the device. It is protected by permission at the'
        ' application level.'
    ),
    'c_prot_sign_sys_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion < 17]',
        'info',
        'A%s %s is found to be exported, but is protected by a permission at the application'
        ' level. However, the protection level of the permission is set to signatureOrSystem.'
        ' It is recommended that signature level is used instead. Signature level should'
        ' suffice for most purposes, and does not depend on where the applications are'
        ' installed on the device.'
    ),
    'c_prot_unknown_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at application level, but the'
        ' protection level of the permission should be checked.</br>%s <br>[Content Provider,'
        ' targetSdkVersion < 17]',
        'high',
        'A%s %s is found to be shared with other apps on the device therefore leaving it'
        ' accessible to any other application on the device. It is protected by a'
        ' permission at application level which is not defined in the analysed application.'
        ' As a result, the protection level of the permission should be checked where it'
        ' is defined. If it is set to normal or dangerous, a malicious application can'
        ' request and obtain the permission and interact with the component. If it is'
        ' set to signature, only applications signed with the same certificate can obtain'
        ' the permission.'
    ),
    'c_prot_normal_new': (
        '<strong>%s</strong> (%s) is Protected by a permission, but'
        ' the protection level of the permission should be checked if'
        ' the application runs on a device where the the API level is less than 17</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider (%s) would be exported if the application ran on a'
        ' device where the the API level was less than 17. In that situation, it'
        ' would still be protected by a permission. However, the protection level'
        ' of the permission is set to normal. This means that a malicious application'
        ' could request and obtain the permission and interact with the component. If'
        ' it was set to signature, only applications signed with the same certificate'
        ' could obtain the permission.'
    ),
    'c_prot_danger_new': (
        '<strong>%s</strong> (%s) is Protected by a permission, but'
        ' the protection level of the permission should be checked if'
        ' the application runs on a device where the the API level is less than 17.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider(%s) would be exported if the application ran on a device'
        ' where the the API level was less than 17. In that situation, it would still'
        ' be protected by a permission. However, the protection level of the permission'
        ' is set to dangerous. This means that a malicious application could request and'
        ' obtain the permission and interact with the component. If it was set to'
        ' signature, only applications signed with the same certificate could obtain'
        ' the permission.'
    ),
    'c_prot_sign_new': (
        '<strong>%s</strong> (%s) is Protected by a permission.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'info',
        'The Content Provider(%s) would be exported if the application ran on a'
        ' device where the the API level was less than 17. Nevertheless, it is'
        ' protected by a permission.'
    ),
    'c_prot_sign_sys_new': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of'
        ' the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'info',
        'The Content Provider(%s) would be exported if the application ran on a device where'
        ' the API level was less than 17. In that situation, it would still be protected by a'
        ' permission. However, the protection level of the permission is set to'
        ' signatureOrSystem. It is recommended that signature level is used instead.'
        ' Signature level should suffice for most purposes, and does not depend on where'
        ' the applications are installed on the device.'
    ),
    'c_prot_unknown_new': (
        '<strong>%s</strong> (%s) is Protected by a permission, but the protection level of'
        ' the permission should be checked  if the application runs on a device where the the'
        ' API level is less than 17.</br>%s <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider(%s) would be exported if the application ran on a device where'
        ' the the API level was less than 17. In that situation, it would still be protected'
        ' by a permission which is not defined in the analysed application. As a result, the'
        ' protection level of the permission should be checked where it is defined. If it is'
        ' set to normal or dangerous, a malicious application can request and obtain the'
        ' permission and interact with the component. If it is set to signature, only'
        ' applications signed with the same certificate can obtain the permission.'
    ),
    'c_prot_normal_new_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked if'
        ' the application runs on a device where the the API level is less than 17</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider (%s) would be exported if the application ran on a'
        ' device where the the API level was less than 17. In that situation, it'
        ' would still be protected by a permission. However, the protection level'
        ' of the permission is set to normal. This means that a malicious application'
        ' could request and obtain the permission and interact with the component. If'
        ' it was set to signature, only applications signed with the same certificate'
        ' could obtain the permission.'
    ),
    'c_prot_danger_new_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked if'
        ' the application runs on a device where the the API level is less than 17.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider(%s) would be exported if the application ran on a device'
        ' where the the API level was less than 17. In that situation, it would still'
        ' be protected by a permission. However, the protection level of the permission'
        ' is set to dangerous. This means that a malicious application could request and'
        ' obtain the permission and interact with the component. If it was set to'
        ' signature, only applications signed with the same certificate could obtain'
        ' the permission.'
    ),
    'c_prot_sign_new_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application'
        ' level.</br>%s<br>[Content Provider, targetSdkVersion >= 17]',
        'info',
        'The Content Provider(%s) would be exported if the application ran on a'
        ' device where the the API level was less than 17. Nevertheless, it is'
        ' protected by a permission.'
    ),
    'c_prot_sign_sys_new_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application'
        ' level, but the protection level of the permission should be checked.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'info',
        'The Content Provider(%s) would be exported if the application ran on a device where'
        ' the API level was less than 17. In that situation, it would still be protected by a'
        ' permission. However, the protection level of the permission is set to'
        ' signatureOrSystem. It is recommended that signature level is used instead.'
        ' Signature level should suffice for most purposes, and does not depend on where'
        ' the applications are installed on the device.'
    ),
    'c_prot_unknown_new_appl': (
        '<strong>%s</strong> (%s) is Protected by a permission at the application level,'
        ' but the protection level of the permission should be checked  if the application'
        ' runs on a device where the the API level is less than 17.</br>%s'
        ' <br>[Content Provider, targetSdkVersion >= 17]',
        'high',
        'The Content Provider(%s) would be exported if the application ran on a device where'
        ' the the API level was less than 17. In that situation, it would still be protected'
        ' by a permission which is not defined in the analysed application. As a result, the'
        ' protection level of the permission should be checked where it is defined. If it is'
        ' set to normal or dangerous, a malicious application can request and obtain the'
        ' permission and interact with the component. If it is set to signature, only'
        ' applications signed with the same certificate can obtain the permission.'
    ),
    'a_improper_provider': (
        'Improper Content Provider Permissions<br>[%s]',
        'high',
        'A content provider permission was set to allows access from any other app on the device. '
        'Content providers may contain sensitive information about an app and therefore should not'
        ' be shared.'
    ),
    'a_dailer_code': (
        'Dailer Code: %s Found <br>[android:scheme="android_secret_code"]',
        'high',
        'A secret code was found in the manifest. These codes, when entered into the dialer grant'
        ' access to hidden content that may contain sensitive information.'
    ),
    'a_sms_receiver_port': (
        'Data SMS Receiver Set on Port: %s Found<br>[android:port]',
        'high',
        'A binary SMS recevier is configured to listen on a port. Binary SMS messages sent to a '
        'device are processed by the application in whichever way the developer choses. The data'
        ' in this SMS should be properly validated by the application. Furthermore, the application'
        ' should assume that the SMS being received is from an untrusted source."'
    ),
    'a_high_intent_priority': (
        'High Intent Priority (%s)<br>[android:priority]',
        'medium',
        'By setting an intent priority higher than another intent, the app effectively overrides'
        ' other requests.'
    ),
    'a_high_action_priority': (
        'High Action Priority (%s)<br>[android:priority] ',
        'medium',
        'By setting an action priority higher than another action, the app effectively overrides'
        ' other requests.'
    ),
}


def get_all_risk():
    return set(map(lambda e: manifest_desc[e][1], manifest_desc.keys()))


def get_raw_types_by_title(query="High Action Priority (xxxaaa)<br>[android:priority]"):
    sorted_name = sorted(list(manifest_desc))
    for each in manifest_desc.keys():
        pattern = manifest_desc[each][0].replace("(", r"\(") \
            .replace(")", r"\)") \
            .replace("[", r"\[") \
            .replace("]", r"\]") \
            .replace("{", r"\{") \
            .replace("}", r"\}") \
            .replace("%s", r".*")
        pattern = re.compile(pattern)
        if pattern.search(query):
            return sorted_name.index(each), each, manifest_desc[each]


if __name__ == '__main__':
    for each in manifest_desc.values():
        print each[-1]

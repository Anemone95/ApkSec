#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import subprocess
import logging
import re

import core.controllers.plugin_category as plugin_category
import core.controllers.task_info as task_info
import core.controllers.apksec_exceptions as apksec_exceptions
import settings


class AAPT(plugin_category.ApkChecker):
    def start(self):
        _task_info = task_info.TaskInfo()
        if settings.OS == 'WindowsPE':
            bin_path = os.path.join('windows_64bit', 'aapt.exe')
        elif settings.OS == 'ELF':
            if settings.ARCH == '64bit':
                bin_path = os.path.join('linux_64bit', 'aapt')
            else:
                bin_path = os.path.join('linux_32bit', 'aapt')
        else:
            raise apksec_exceptions.PluginException('Unknown System')
        bin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'bin', bin_path)
        process = subprocess.Popen('{aapt} dump badging {apk_path}'.format(aapt=bin_path, apk_path=self.apk_path),
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        aapt_res, err = process.communicate()
        if len(err):
            logging.error('aapt error: {}'.format(err))
            return False
        aapt_res = aapt_res.replace('\n', '').replace('\r', '')

        regex_package_name = r"package: name='([a-z\.]*)'"
        match_res = re.match(regex_package_name, aapt_res)
        if match_res:
            _task_info.package_name = match_res.group(1)
        else:
            raise apksec_exceptions.ApkCheckerException("Unknown package name.")

        has_main = False
        if not has_main:
            regex_main_activity = r".*launchable\-activity: name='([a-zA-Z0-9\.]*)'"
            match_res = re.match(regex_main_activity, aapt_res)
            if match_res:
                _task_info.main_activity = match_res.group(1)
                has_main = True
        if not has_main:
            regex_main_activity = r".*android:name=.([a-zA-Z0-9\.]*).*<intent-filter>.*action\.MAIN.*</intent-filter>"
            match_res = re.match(regex_main_activity, aapt_res)
            if match_res:
                _task_info.main_activity = match_res.groups()[0]
                has_main = True
        if not has_main:
            raise apksec_exceptions.ApkCheckerException("Unknown main activity.")

        regex_target_sdk = r".*targetSdkVersion:'([1-9]\d*)'"
        match_res = re.match(regex_target_sdk, aapt_res)
        if match_res:
            _task_info.target_sdk = int(match_res.group(1))
        else:
            raise apksec_exceptions.ApkCheckerException("Unknown target sdk.")
        return True


if __name__ == '__main__':
    xml = '''
<application android:banner="@drawable/app_banner" android:debuggable="false" android:hardwareAccelerated="true" android:icon="@drawable/app_icon" android:isGame="true" android:label="@string/app_name">
<activity android:configChanges="fontScale|keyboard|keyboardHidden|locale|mcc|mnc|navigation|orientation|screenLayout|screenSize|smallestScreenSize|touchscreen|uiMode" android:label="@string/app_name" android:launchMode="singleTask" android:name="com.unity3d.player.UnityPlayerNativeActivity" android:screenOrientation="sensorLandscape">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
        <category android:name="android.intent.category.LEANBACK_LAUNCHER"/>
    </intent-filter>
    <meta-data android:name="unityplayer.UnityActivity" android:value="true"/>
    <meta-data android:name="unityplayer.ForwardNativeEventsToDalvik" android:value="true"/>
</activity>
<activity android:configChanges="keyboard|keyboardHidden|orientation" android:label="@string/app_name" android:name="com.unity3d.player.VideoPlayer"/>
<activity android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|screenSize|smallestScreenSize|uiMode" android:name="com.google.android.gms.ads.AdActivity"/>
    '''.replace('\n', '').replace('\r', '')
    regex_main_activity = r".*android:name=.([a-zA-Z0-9\.]*).*<intent-filter>.*action\.MAIN.*</intent-filter>"
    match_res = re.match(regex_main_activity, xml)
    print match_res.groups()[0]

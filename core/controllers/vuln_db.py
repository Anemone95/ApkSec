#!/usr/bin/env python
# -*- coding=utf-8 -*-
from core.controllers.const import RISK
from core.controllers.vulnerability import Vulnerability

V_DEBUGGABLE = Vulnerability(name='debuggable',
                             i18n_name=u'程序可被任意调试',
                             category=u'Manifest文件检测',
                             description=u'在manifest.xml中定义Debuggable项，如果该项被打开，app存在被恶意程序调试的风险，'
                                         u'可能导致泄漏敏感信息泄漏等问题。',
                             solution=u'显示的设置manifest的debuggable标志为false',
                             risk_level=RISK.HIGH)
V_BACKUP = Vulnerability(name='backup',
                         i18n_name=u'备份标识配置风险',
                         category=u'Manifest文件检测',
                         description=u'Android 2.1以上的系统可为App提供应用程序数据的备份和恢复功能，'
                                     u'该由AndroidMainfest.xml文件中的allowBackup属性值控制，其默认值为true。'
                                     u'当该属性没有显式设置为false时,攻击者可通过adb backup和adb restore对App的应用数据进行备份和恢复,'
                                     u'从而可能获取明文存储的用户敏感信息，如用户的密码、证件号、手机号、交易密码、身份令牌、服务器通信记录等。'
                                     u'利用此类信息攻击者可伪造用户身份，盗取用户账户资产，或者直接对服务器发起攻击。',
                         solution=u'在AndroidManifest.xml中设置android:allowBackup="false"',
                         risk_level=RISK.MEDIUM)
V_INFO_LEAKAGE = Vulnerability(name='info_leakage',
                               i18n_name=u'敏感信息泄露',
                               category=u'数据安全检测',
                               description=u'文件可能包含硬编码的敏感信息，如用户名，密码，IP地址等。',
                               solution=u'以下字段在编码和网络传输过程中建议加密处理：'
                                        u'密码、手机号、快捷支付手机号、Email、身份证、银行卡、CVV码、有效期、IP地址。',
                               risk_level=RISK.MEDIUM)
V_ECB_MODE = Vulnerability(name='ECB_mode',
                           i18n_name=u'不安全的加密模式',
                           category=u'弱加密风险',
                           description=u'在AES加密时，使用“ECB”的模式。ECB是将文件分块后对文件块做同一加密，'
                                       u'破解加密只需要针对一个文件块进行解密，降低了破解难度和文件安全性。',
                           solution=u'避免使用ECB模式，建议使用CBC。',
                           risk_level=RISK.LOW)
V_HOST_WEAK_VERIFY = Vulnerability(name='host_weak_verify',
                                   i18n_name=u'主机名弱校验漏洞检测',
                                   category=u'网络通信安全检测',
                                   description=u'自定义HostnameVerifier类，却不实现verify方法验证域名，导致中间人攻击漏洞。',
                                   solution=u'自定义HostnameVerifier类并实现verify方法验证域名。',
                                   risk_level=RISK.MEDIUM)
V_FILE_READABLE = Vulnerability(name='file_readable',
                                i18n_name=u'全局文件可读',
                                category=u'数据安全检测',
                                description=u'APP在创建内部存储文件时，将文件设置了全局的可读权限。攻击者恶意读取文件内容，获取敏感信息。',
                                solution=u'使用MODE_PRIVATE模式创建内部存储文件',
                                risk_level=RISK.MEDIUM)
V_FILE_WRITEABLE = Vulnerability(name='file_writeable',
                                 i18n_name=u'全局文件可写',
                                 category=u'数据安全检测',
                                 description=u'APP在创建内部存储文件时，将文件设置了全局的可写权限。攻击者恶意写文件内容，破坏APP的完整性。',
                                 solution=u'使用MODE_PRIVATE模式创建内部存储文件',
                                 risk_level=RISK.MEDIUM)
V_FILE_READABLE_AND_WRITEABLE = Vulnerability(name='file_readable_and_writeable',
                                              i18n_name=u'全局文件可读可写',
                                              category=u'数据安全检测',
                                              description=u'APP在创建内部存储文件时，将文件设置了全局的可读写权限。'
                                                          u'攻击者恶意写文件内容或者，破坏APP的完整性，或者是攻击者恶意读取文件内容，获取敏感信息。',
                                              solution=u'使用MODE_PRIVATE模式创建内部存储文件',
                                              risk_level=RISK.MEDIUM)
V_WEAK_HASH = Vulnerability(name='weak_hash',
                            i18n_name=u'Hash算法不安全',
                            category=u'弱加密风险',
                            description=u'使用不安全的Hash算法(MD4、MD5、RC2、RC4、SHA-1)加密信息，存在被破解的风险',
                            solution=u'使用SHA-256算法',
                            risk_level=RISK.MEDIUM)
V_WEAK_RANDOM = Vulnerability(name='weak_random',
                              i18n_name=u'随机数函数不安全',
                              category=u'弱加密风险',
                              description=u'使用不安全的伪随机数发生器(java.util.Random)，其生成的伪随机数可预测。',
                              solution=u'使用SecureRandom库生成伪随机数。',
                              risk_level=RISK.MEDIUM)
V_LOG_LEAKAGE = Vulnerability(name='log_leakage',
                              i18n_name=u'日志泄露隐私风险',
                              category=u'数据安全检测',
                              description=u'调试日志函数可能输出重要的日志文件，其中包含的信息可能导致客户端用户信息泄露，'
                                          u'暴露客户端代码逻辑等，为发起攻击提供便利，例如：Activity的组件名，是Activity劫持需要的信息；'
                                          u'通信交互的日志，会成为发动服务器攻击的依据；跟踪的变量值，可能泄露一些敏感数据，输入的账号、密码等。',
                              solution=u'关闭调试日志函数调用，或者确保日志的输出使用了正确的级别，涉及敏感数据的日志信息在发布版本中被关闭。',
                              risk_level=RISK.LOW)
V_WEBVIEW_JS = Vulnerability(name='webview_js',
                             i18n_name=u'Web组件远程代码执行漏洞',
                             category=u'WebView组件安全检测',
                             description=u'Webview是Android用于浏览网页的组件，'
                                         u'其包含的接口函数addJavascriptInterface可以将Java类或方法导出以供JavaScript调用，'
                                         u'实现网页JS与本地JAVA的交互。由于系统没有限制已注册JAVA类的方法调用，'
                                         u'因此未注册的其它任何JAVA类也可以被反射机制调用，'
                                         u'这样可能导致被篡改的URL中存在的恶意代码被执行，'
                                         u'用户手机被安装木马程序，发送扣费短信，通信录或者短信被窃取，'
                                         u'甚至手机被远程控制。',
                             solution=u'建议禁用危险接口addJavascriptInterface导出Java类及方法，并加强访问的url的域控制。',
                             risk_level=RISK.LOW)
V_INSECURE_IV = Vulnerability(name='insecure_iv',
                              i18n_name=u'IVParameterSpec不安全初始化向量检测',
                              category=u'弱加密风险',
                              description=u'使用IVParameterSpec函数，并且使用了固定的初始化向量，'
                                          u'那么密码文本可预测性高得多，容易受到字典攻击等。',
                              solution=u'禁止使用常量初始化矢量参数构建IvParameterSpec。',
                              risk_level=RISK.HIGH)
V_WEBVIEW_SSL = Vulnerability(name='webview_ssl',
                              i18n_name=u'WebView不校验证书漏洞检测',
                              category=u'WebView组件安全检测',
                              description=u'Android WebView组件加载网页发生证书认证错误时，'
                                          u'会调用WebViewClient类的onReceivedSslError方法，'
                                          u'如果该方法实现调用了handler.proceed()来忽略该证书错误，'
                                          u'则会受到中间人攻击的威胁，可能导致隐私泄露。',
                              solution=u'当发生证书认证错误时，采用默认的处理方法handler.cancel()，'
                                       u'停止加载问题页面当发生证书认证错误时，采用默认的处理方法handler.cancel()，停止加载问题页面。',
                              risk_level=RISK.MEDIUM)
V_ROOT_DETECT = Vulnerability(name='root_detect',
                              i18n_name=u'root代码检测',
                              category=u'敏感函数调用',
                              description=u'app可能不存在检测root环境的代码',
                              solution=u'',
                              risk_level=RISK.INFO)
if __name__ == '__main__':
    pass

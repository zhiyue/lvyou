# 接入Server酱Turbo

---
- **页面ID**: 633
- **作者ID**: 1
- **创建时间**: 2025-06-13 21:18:37
- **分类ID**: 197
---

　　「Server酱Turbo」，英文名「ServerChan」，是一款「手机」和「服务器」、「智能设备」之间的通信软件。绿邮开发板通过简单的配置，即可接入Server酱Turbo，无需二次开发。
　　Server酱Turbo官网：https://sct.ftqq.com/
　　
_
####Server酱的接入步骤：

　　（1）参照“快速入门”一节，先确保开发板正常连入WIFI，并可以登录到开发板后台页面。
　　
　　（2）在开发板后台页面中，点击进入“配置备份/恢复”页面，将以下的“配置信息”复制到“设备配置数据”的文本框中，然后点击“更新配置”按钮，**等待5秒后，重启开发板**。

**配置信息代码如下：**（复制以下黑框中的所有内容↓↓↓↓↓↓↓↓）

```json
{"wen":true,"wdb":99,"ecr":0,"lsben":true,"nsben":true,"srtmin":2,"ping":175,"ackMax":8000,"schr":4,"tz":8,"tca":15,"otat":3,"botm":[0,0],"amo":[1,1],"cim":[],"cims":[],"lss":[30,30],"sen":[false,false],"ord":[20,10],"str2":["SM","SM"],"sysArgs":null,"adName":"admin","uip":[{"url":"https://sctapi.ftqq.com/{{{sendkey}}}.send","method":1,"conType":0,"jcl":false,"reqFreq":false,"reqCnt":20,"reqOkLog":false,"reqErrLog":true,"allType":[100,101,102,204,205,209,501,603],"userArgs":{"0":{"un":"devName","uv":"{{devId}}","en":"0"},"1":{"un":"sendkey","uv":"","en":"0"},"2":{"un":"tail","uv":"★☆★☆短信小尾巴（不需要可以不填写）","us":"501","en":"0"}}}]}

~~--==~~--==
100
title=【设备上线提醒】{{{devName}}}&desp=设备已通过 WiFi 上线！{{LN}}{{LR}}→本机IP：{{ip}}{{LN}}{{LR}}→WiFi热点：{{ssid}}{{LN}}{{LR}}→信号强度：{{dbm}}%{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
603
title=【来电提醒】{{phNum}}&desp=→号码：{{phNum}}{{LN}}{{LR}}→时间：{{telStartTs|$ts2hhmmss(':')}} 至 {{telEndTs|$ts2hhmmss(':')}}{{LN}}{{LR}}↑↑来源：{{{devName}}}（卡{{slot}} {{msIsdn}}）{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
501
title=【新短信提醒】{{phNum}}&desp={{smsBd}}{{LN}}{{LR}}→短信号码：{{phNum}}{{LN}}{{LR}}→短信时间：{{smsTs|$ts2yyyymmddhhmmss('-',':')}}{{LN}}{{LR}}↑↑来源：{{{devName}}}（卡{{slot}} {{msIsdn}}）{{LN}}{{LR}}→时间：{{YMDHMS}}{{LN}}{{LR}}{{{tail}}}
~~--==~~--==
209
title=【设备提醒】{{phNum}}&desp=“卡{{slot}}”存在故障，请将卡放入手机检查原因！{{LN}}{{LR}}SIM卡信息：{{LN}}{{LR}}→iccid：{{iccId}}{{LN}}{{LR}}→imsi：{{imsi}}{{LN}}{{LR}}→卡号：{{msIsdn}}{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
205
title=【设备提醒】{{phNum}}&desp=“卡{{slot}}”已从设备中取出！{{LN}}{{LR}}SIM卡信息：{{LN}}{{LR}}→iccid：{{iccId}}{{LN}}{{LR}}→imsi：{{imsi}}{{LN}}{{LR}}→卡号：{{msIsdn}}{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
204
title=【设备提醒】{{phNum}}&desp=“卡{{slot}}”已就绪！{{LN}}{{LR}}SIM卡信息：{{LN}}{{LR}}→iccid：{{iccId}}{{LN}}{{LR}}→imsi：{{imsi}}{{LN}}{{LR}}→卡号：{{msIsdn}}{{LN}}{{LR}}→信号强度：{{dbm}}%{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
title=【设备上线提醒】{{{devName}}}&desp=设备已通过 卡2 上线！{{LN}}{{LR}}SIM卡信息：{{LN}}{{LR}}→iccid：{{iccId}}{{LN}}{{LR}}→imsi：{{imsi}}{{LN}}{{LR}}→卡号：{{msIsdn}}{{LN}}{{LR}}→信号强度：{{dbm}}%{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}
~~--==~~--==
101
title=【设备上线提醒】{{{devName}}}&desp=设备已通过 卡1 上线！{{LN}}{{LR}}SIM卡信息：{{LN}}{{LR}}→iccid：{{iccId}}{{LN}}{{LR}}→imsi：{{imsi}}{{LN}}{{LR}}→卡号：{{msIsdn}}{{LN}}{{LR}}→信号强度：{{dbm}}%{{LN}}{{LR}}↑↑来源：{{{devName}}}{{LN}}{{LR}}→时间：{{YMDHMS}}

```

**操作图示如下：**
![](images/ddd012ed_63be8adc3c6a0.jpg)

------------

> **注意：**
　　先将原有的“设备配置信息”全部清除，然后，再复制上面的配置信息，粘贴到“设备配置数据”的文本框中。

　　
　　（3）登录 Server酱 网站（新用户可能需要先完成注册），Server酱 登录地址为：https://sct.ftqq.com/login
　　
　　（4）Server酱 网站成功后，点击“KEY&API”功能获取`sendKey`。

**操作图示如下：**

![](images/247911d2_63beae94ddbdf.png)
　
 
　　（5）登录开发板后台页面，进入“用户参数管理”页面，将之前获取的 sendkey 填写到指定位置，然后点击“保存页面配置”按钮。

**操作图示如下：**
![](images/2ce8b246_63beaf2d32e92.png)


　　
　　（6）重启开发板，重启完成之后，开发板中的手机卡的短信以及未接来电提醒，会自动在您微信的 Server酱 的公众号中显示。
  
**操作图示如下：**
![](images/c65b5933_63beaf805541f.png)


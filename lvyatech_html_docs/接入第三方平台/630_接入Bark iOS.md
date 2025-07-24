# 接入Bark iOS

---
- **页面ID**: 630
- **作者ID**: 1
- **创建时间**: 2025-05-31 18:05:05
- **分类ID**: 197
---

　　Bark iOS是一款苹果手机 （iOS）专用的APP，特点是免费、轻量，经过简单调用接口，即可给自己的iPhone发送推送信息，在苹果手机上有着绝佳的使用体验。（苹果手机用户，推荐使用！）
　　
_
####Bark iOS的接入步骤：

　　（1）参照“快速入门”一节，先确保开发板正常连入WIFI，并可以登录到开发板后台页面。
　　
　　（2）在开发板后台页面中，点击进入“配置备份/恢复”页面，将以下的“配置信息”复制到“设备配置数据”的文本框中，然后点击“更新配置”按钮，**等待5秒后，重启开发板**。

**配置信息代码如下：**（复制以下黑框中的所有内容↓↓↓↓↓↓↓↓）

```json
{"wen":true,"wdb":99,"ecr":0,"lsben":true,"nsben":true,"srtmin":2,"ping":110,"ackMax":8000,"schr":4,"tz":8,"tca":15,"otat":3,"botm":[0,0],"amo":[1,1],"cim":[],"cims":[],"lss":[30,30],"sen":[false,false],"ord":[20,10],"str2":["SM","SM"],"sysArgs":{"devSmsTs":{"en":"0"}},"adName":"admin","uip":[{"url":"http://api.day.app/push","method":1,"conType":1,"jcl":true,"reqFreq":false,"reqCnt":20,"reqOkLog":false,"reqErrLog":true,"allType":[100,101,102,204,205,209,501,603],"userArgs":{"0":{"un":"title","uv":"【绿芽推送】"},"1":{"un":"device_key","uv":"\"\""},"2":{"un":"device_key_more"},"3":{"un":"group","uv":"绿芽"},"4":{"un":"isArchive","uv":"1"},"5":{"un":"level","uv":"active"},"8":{"un":"devName","uv":"{{devId}}"},"9":{"un":"tail","uv":"★☆短信小尾巴（不需要可不填）"}}}]}

~~--==~~--==
204
{
"title":"{{{title}}}",
"subtitle":"【设备状态提醒】",
"body":"卡{{slot}}”已就绪！{{LN}}{{LN}}SIM卡信息：{{LN}}→iccid：{{iccId}}{{LN}}→imsi：{{imsi}}{{LN}}→卡号：{{msIsdn}}{{LN}}→信号强度：{{dbm}}%{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
102
{
"title":"{{{title}}}",
"subtitle":"【设备上线提醒】",
"body":"设备已通过 卡2 上线！{{LN}}{{LN}}SIM卡信息：{{LN}}→iccid：{{iccId}}{{LN}}→imsi：{{imsi}}{{LN}}→卡号：{{msIsdn}}{{LN}}→信号强度：{{dbm}}%{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
101
{
"title":"{{{title}}}",
"subtitle":"【设备上线提醒】",
"body":"设备已通过 卡1 上线！{{LN}}{{LN}}SIM卡信息：{{LN}}→iccid：{{iccId}}{{LN}}→imsi：{{imsi}}{{LN}}→卡号：{{msIsdn}}{{LN}}→信号强度：{{dbm}}%{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
100
{
"title":"{{{title}}}",
"subtitle":"【设备上线提醒】",
"body":"设备已通过 WiFi 上线！{{LN}}{{LN}}→本机IP：{{ip}}{{LN}}→WiFi热点：{{ssid}}{{LN}}→信号强度：{{dbm}}%{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
205
{
"title":"{{{title}}}",
"subtitle":"【设备状态提醒】",
"body":"卡{{slot}}”已从设备中取出！{{LN}}{{LN}}SIM卡信息：{{LN}}→iccid：{{iccId}}{{LN}}→imsi：{{imsi}}{{LN}}→卡号：{{msIsdn}}{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
603
{
"title":"{{{title}}}",
"subtitle":"【来电提醒】",
"body":"设备有一个未接来电。{{LN}}→号码：{{phNum}}{{LN}}→时间：{{telStartTs|$ts2hhmmss(':')}} 至 {{telEndTs|$ts2hhmmss(':')}}{{LN}}{{LN}}↑↑来源：{{{devName}}}（卡{{slot}} {{msIsdn}}）{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
209
{
"title":"{{{title}}}",
"subtitle":"【设备状态提醒】",
"body":"卡{{slot}}”存在故障，请将卡放入手机检查原因！{{LN}}{{LN}}SIM卡信息：{{LN}}→iccid：{{iccId}}{{LN}}→imsi：{{imsi}}{{LN}}→卡号：{{msIsdn}}{{LN}}{{LN}}↑↑来源：{{{devName}}}{{LN}}→时间：{{YMDHMS}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
~~--==~~--==
501
{
"title":"{{{title}}}",
"subtitle":"新短信提醒",
"body":"{{smsBd}}{{LN}}→短信号码：{{phNum}}{{LN}}→短信时间：{{smsTs|$ts2yyyymmddhhmmss('-',':')}}{{LN}}↑↑来源：{{{devName}}}（卡{{slot}} {{msIsdn}}）{{LN}}→时间：{{YMDHMS}}{{LN}}{{{tail}}}",
"device_key":{{{device_key}}},
"device_keys":[ {{{device_key}}} {{{device_key_more|$nothingIfNotBlank(',')}}} {{{device_key_more}}}],
"level":"{{{level}}}",
"group":"{{{group}}}",
"isArchive":"{{{isArchive}}}"
}
```

**操作图示如下：**
![](images/ddd012ed_63be8adc3c6a0.jpg)

------------

> **注意：**
　　先将原有的“设备配置信息”全部清除，然后，再复制上面的配置信息，粘贴到“设备配置数据”的文本框中。

　　
　　（3）打开您苹果手机上的app store，搜索并安装好Bark iOS。
  **操作图示如下：**

![](images/954ae784_63bf85e81e942.png)
　　
　　（4）Bark iOS安装成功后，点击运行。在Bark iOS的主界面中，点击下图所示的“复制”图标，获取到bark iOS提供的http地址。
  　　
**注意！Bark iOS首次运行时可能会弹出以下界面，请按图示操作即可：**.

![](images/34e1a6d6_63bf8c206e227.png)
　　
**复制http地址的操作图示如下：**

![](images/338beafd_63bf863518a18.png)
　
 
　　（5）登录开发板后台页面，进入“用户参数管理”页面，将之前复制的 http地址 仅保留KEY的部分，填写到参数“device_key”后面的“值”的文本框中，然后点击“保存页面配置”按钮。
  
> **注意：**
>　　Bark iOS点击“复制”按钮后，复制的数据可能为以下格式：
>　　　　https://api.day.app/qY3jxAJfxnABCDALSiekZ/这里改成你自己的推送内容
>　　只保留 qY3jxAJfxnABCDALSiekZ 这一段（两个/符号中间的字符），其它不要复制。

**操作图示如下：**
![](images/887a57bc_683ad08f86739.png)
> **再次注意：**
　　填写 qY3jxAJfxnABCDALSiekZ 时，两侧需要增加“半角的双引号”。
  
  
  当您需要将短信同时转发给多个Bark iOS客户端时，除了第一个 Bark iOS 的KEY之外， 其它Bark客户端的KEY，需要填写到“device_key_more”的值中，示例如下：
  ![](images/a3e5e4d2_683ad1945d32a.png)
　　
  > **注意：**
  这个例子时，同时将短信转发给3个Bark客户端，除了第1个客户端的KEY必需写在“device_key”中之外，其它2个客户端的KEY，需要填写到“device_key_more”中。
  同样的，每一个KEY都需要写“双引号”（半角），多个KEY之间用“半角逗号”分隔。


　　
　　（6）重启开发板，重启完成之后，开发板中的手机卡的短信以及未接来电提醒，会自动在您Bark中显示。
  
**操作图示如下：**
![](images/9c62f157_63bf919a67eb7.png)


　　
　　（7）为了便于您的使用，在我们示范的配置文件中，已经对部分事件进行了对接（见下图）。如果您不需要其中的某些事件，您可以手动将对应的事件勾选取消掉，然后点击保存就可以了。
  如果您需要对接新的事件，您需要参照开发文档独自完成对接。
![](images/86f1fe1b_683ad3b217c1f.png)


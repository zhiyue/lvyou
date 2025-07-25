# sendsms - 外发短信

---
- **页面ID**: 581
- **作者ID**: 1
- **创建时间**: 2025-05-15 19:28:20
- **分类ID**: 185
---

###“命令：sendsms - 控制SIM卡外发短信”使用说明
####命令的作用
　　使用 sendsms 命令，可以控制开发板的某个卡槽中的SIM卡，向外发送短信。
  
　　如果您的接口需要获取**短信发外成功报告**，那么您需要在控制命令中增加tid参数，并为其添加一个唯一ID（一般推荐使用timestamp即可）。
　　当短信外发成功后，您的接口将接收到开发板推送的501消息。501消息中tid参数，与您在控制命令中提供的tid参数一致。

```plantuml
@startuml
用户接口 -> 开发板:　控制命令:sendsms (tid=123456)
用户接口 <-- 开发板 : 　　推送消息:501 (tid=123456)
@enduml
```
　　
　　sendsms控制消息中，tid参数不可以省略。
  
####命令的格式（示例）
```
http://192.168.7.170/ctrl?token=3f4bffa77257d243875d0a5a80635934&cmd=sendsms&tid=1647344840&p1=2&p2=10001&p3=查话费
```
####命令的格式（TCP方式示例）
```
{"cmd":"sendsms", "p1":2, "p2":"10001", "p3":"查话费", "tid":"1647344840"}\x11\x12
```
####命令参数说明
 | 参数名  | 参数值（示例）  |参数类型|说明|
| ------------ |:------------ |-----|--|
|token |3f4bffa77257d243875d0a5a80635934 |字符型|管理员Token|
|cmd  | sendsms |字符型|控制命令名称|
|p1 |2 |数值型|外发短信的卡槽号|
|p2 |10001 |字符型|短信号码|
|p3 |查话费 |字符型|短信内容|
|tid   | 任意值 |字符型|不可省略。控制命令的唯一标识，用于接收501消息（短信外发成功报告）|
####命令反馈结果
成功时返回：
```
{
  "code": 0
}
```

失败时返回：
```
{
  "code": 101,
  "msg": "Invalid arguments."
}
```

####命令反馈结果说明
无




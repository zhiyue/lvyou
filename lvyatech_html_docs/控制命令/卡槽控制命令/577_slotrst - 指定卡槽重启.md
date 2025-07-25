# slotrst - 指定卡槽重启

---
- **页面ID**: 577
- **作者ID**: 1
- **创建时间**: 2025-05-15 19:29:16
- **分类ID**: 183
---

###“命令：slotrst - 指定卡槽重启”使用说明
####命令的作用
　　使用 slotrst 命令，可以让开发板上的某个卡槽重新启动。重新启动过程，一般需要60秒左右的时间。命令发出后，相当于用户手动将开发板上的SIM卡弹出后，又重新插入SIM卡。
  
　　正常情况下，您接口会在卡槽重启的过程中，陆续接收到开发板推送的202、203、204推送消息。
####命令的格式（示例）
```
http://192.168.7.170/ctrl?token=3f4bffa77257d243875d0a5a80635934&cmd=slotrst&p1=1
```
####命令的格式（TCP方式示例）
```
{"cmd":"slotrst", "p1":"1", "tid":"1234"}\x11\x12
```
####命令参数说明
 | 参数名  | 参数值（示例）  |参数类型|说明|
| ------------ |:------------ |-----|--|
|token |3f4bffa77257d243875d0a5a80635934 |字符型|管理员Token|
|cmd  | slotrst |字符型|控制命令名称|
|p1 |1 |数值型|卡槽号。1表示卡槽1；2表示卡槽2|
|tid (可选)  | 任意值 |字符型|仅TCP接口方式可用。如省略，则命令执行后，不反馈命令执行结果。|
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





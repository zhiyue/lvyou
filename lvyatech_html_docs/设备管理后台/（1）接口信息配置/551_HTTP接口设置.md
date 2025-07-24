# HTTP接口设置

---
- **页面ID**: 551
- **作者ID**: 1
- **创建时间**: 2025-05-15 18:00:40
- **分类ID**: 174
---

　　当您的接口使用的是HTTP接口时，通过“**HTTP接口设置**”功能可以对HTTP协议的细节，完成进一步的设置。
  

####HTTP接口设置界面：
![](images/36e8519f_63cdce5639a0d.png)

　　
　　（1）**HTTP请求方式：**用于设置开发板向接口发送HTTP请求时，可以通过 GET 或是 POST 两种方式提交数据。一般来说，在正式的使用环境中，我们**推荐您使用POST**，而GET方式由于受到参数长度的限制，不适合发送数据量较多的数据。GET方式一般用于初步的开发调试中使用。
　　
　　（2）**Content-Type：**Content-Type可以设置HTTP提交数据的方式，有两种选择分别是：FORM 或 JSON。

　　如果您选择了FORM，则开发板向您的接口提交数据时，模拟的是HTTP FORM表单，您的接口一侧收到数据后，可以通过 request 对象获取开发板提交过来的数据，比如在Java中，您可以使用 request.getParameter("参数名") 的方式，获取到数据。
  
　　如果您选择了JSON，则开发板向您的接口提交数据时，您的接口一侧可以通过读取 request 流的方式，获取到一个包括所有数据的完整的JSON串。比如在Java中，示例代码如下：
  ```java
  String contentType = request.getHeader("Content-Type");
  if (contentType.contains("application/json")) {
  	BufferedReader br = null;
  	try {
		  br = new BufferedReader(new InputStreamReader(request.getInputStream(), "UTF-8"));
		  StringBuilder sb = new StringBuilder();
		  String s;
		  while ((s = r.readLine()) != null) {
			  sb.append(s);
		  }
		  String jsonStr = sb.toString();
		  System.out.println("Json数据是：" + jsonStr);
	  } finally {
	  	if (br != null)  r.close();
	  }
  } 
  ```
  
　　注意：如果您选择了 GET + JSON，那么您在接口一侧需要使用 request.getParameter("p") 来获取到GET中的数据。这里的“**p**”，是开发板在GET方式中提交数据时的“固定参数名”。所有数据组装成JSON串后，会放在“p”参数中向您的接口中提交。以100消息为例，“p”参数获取到的参数内容，格式如下：
```json
{ "devId": "498060912345", "type": 100, "ip": "192.168.7.170", "ssid": "mywifi", "dbm": 61, "netCh": 0 } 
```
　　
　　无论如何，GET + JSON 的方式，一般只应用于内部调试阶段，正式环境中都不推荐使用这种组合。
  
　　**Content-Type**，无论您选择 FORM 或是 JSON ，在技术本身的优缺点层面上并没有差异。您可以根据您自己的需要自行选择。
  
　　（3）**请求频率：**一般来说，设置为“无限制”即可。在对接某些第三方平台时（比如对接webhook机器人），有些第三方平台，会限制HTTP请求的频率。比如，钉钉和企业微信，都要求机器人webhook地址的请求频率，不能超过每分钟20次，否则会触发惩罚机制。在这种情况下，您可以将此选项设置为：限制并每分钟不超过20次，即可。
  
　　（4）**HTTP附加头：**一般来说，这个选项用不到。在某些特殊的情况，比如您的接口中开启了HTTP基本身份验证（Basic auth），此时如果用户通过浏览器直接访问接口时，浏览器会弹出“请输入访问的用户名、密码”的提示框，而您希望开发板向接口上报数据不受这个限制，此时，您就可以将HTTP认证信息，附加到HTTP头信息中，类似以下格式：
```
"Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ="
```
　　具体关于HTTP头信息的用法，您可以根据自己的需要自行设计。


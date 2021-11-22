# Fake_METER_Implementation

PS：工具运行的非常慢，可能是复现的时候好多细节论文中没有提到，这篇论文本来开源了的，但是后来又闭源了。。。没有任何代码可以参考。而且我感觉论文课题组跑工具的时候是在GPU上跑的，即使如此，官方实现的METER修复脚本的平均时长也达到了194分钟，而且最离谱的是，对于代码量大的APP和测试序列较长的脚本，最高修复时间居然达到了811分钟，而且这很可能是在GPU上跑的结果。。。在测试复现的工具时，电脑挂了好几天，因为时间和性能的限制，选择构造了**测试动作较少**的部分APP及对应的测试脚本。

**相关演示在视频中，由于跑的时间太长而且使用相关付费技术（如OCR）时需要注册Azure账号或百度账号，令牌环周期性失效，因此在其他电脑上会出现可执行但结果失败的情况，因为关键的OCR解析部分没法跨主机用（为了防止信息泄漏，我已经在相关文件中把我的百度账号相关密码删了）。除非其他使用者再注册百度相关产品（步骤下文中会讲到），否则目前还没有想好解决方法，就先看我的视频、文档和PPT介绍吧。后续再想办法解决其他主机上运行失败的情况。**



## 工具执行流程

### I. 环境要求

- Appium：开源的、适合于原生或混合移动应用的自动化测试平台，应用WebDriver
- Appium Python Client library：用于支持使用 python 编写的测试脚本运行
- Android SDK：可以选用AS自带的或用国内的Android Dev Tools，因为网络原因我选择了后者
- Ubuntu 20.04 或其他Linux环境
- Android Emulator (Android 7 以上)，由于我没有安卓手机，所以用模拟器；如果有安卓手机用真机连接电脑应该也可以

> #### 环境补充：安卓模拟器 CPU 架构冲突问题
>
> 在运行AVD时，有一个很头疼的问题：使用 Intel x86 架构启动和运行都很快，但是目前市面上大多数 apk 采用的是 arm 架构指令集，就会导致在使用 adb install \<apk> 时安装不了，显示兼容问题，对此，采取如下解决方法：（主要参考<a href=https://blog.imlk.top/posts/wechat-in-avd-7-1-x86/>这篇博文</a>）
>
> :star: 主要思路：
>
> 1. 安装 arm 的 AVD：不可取，AVD 启动 arm 架构的虚拟机非常慢，在测试时我等了将近一小时机器才开机，但开机后根本没法操作，卡成 ppt
> 2. 应用英特尔开发的 ARM-Translation，可以把apk里边的arm用的so库在运行时动态转换为x86指令，所有x86的安卓设备里都内置它，可行
>
> :star: 操作流程：
>
> 1. 改`build.prop`里的`ro.product.cpu.abilist`和`ro.product.cpu.abilist32`为`x86,armeabi-v7a,armeabi`，这一步的目的主要是骗过包安装器，可以安装上相应应用
> 2. 改`default.prop`里的`ro.dalvik.vm.native.bridge=0`为`ro.dalvik.vm.native.bridge=libhoudini.so`，开启系统内的NativeBridge。要注意的是，`default.prop`不在`system.img`里面，在`ramdisk.img`里面，`ramdisk.img`是只读的，只在启动的时候读一次到内存里。所以对`default.prop`的修改重启后会丢失，唯一的办法是手动编辑一个`ramdisk.img`，然后用emulator的`-ramdisk`选项指定修改后的`ramdisk.img`文件。
>    - 编辑方法：
>      - 从SDK目录里找到ramdisk.img，备份一份到自己的avd目录里，
>      - 用gunzip解压它，再用cpio解包到一个目录里
>      - 在这目录里找到`default.prop`进行修改
>      - 注意回package的时候，不要用cpio打包，用`mkbootfs ./之前解包到的目录 | gzip > ramdisk-new.img`制作修改后的镜像（可以从这下载<a href=https://github.com/shenyuanv/mkboot-tools>mkbootfs</a> ）
>      - 最后的`ramdisk-new.img`就是修改过的`ramdisk.img`了，在启动avd时用emulator的`-ramdisk`选项指定它即可。
> 3. Enable native bridge，将 persist.sys.nativebridge 从0改为1，在 build.prop 里加上一句 persist.sys.nativebridge=1
> 4. <a href=https://gist.github.com/41a5d8ba498ceecca28e9d1069a32ede>下载一个脚本</a> `enable_nativebridge`，将其放在 avd 里的 `/system/bin/` 下
> 5. `houdini.sfs` 是 squashfs 格式的一个景象，脚本里将其挂载到 /system/lib/arm 里了

### II. 执行 Appium 服务

- 从官网下载 Appium 后，得到的是 `Appium-Server-GUI-linux-1.22.0.AppImage` 的 AppImage 文件，从属性中将其设置为可执行后，双击即可执行
- 执行后，只需要默认开启一个服务即可（Host: 0.0.0.0  Port: 4723）
- 注：测试脚本中的端口号要与 Port 值相应，即默认为 4723

### III. 运行安卓模拟器

- 按前文所述方法解决兼容性问题后，运行安卓虚拟机
- 在终端上可以通过 `adb devices` 命令查看设备情况，确保虚拟机已正常运行

### IV. 注册百度OCR接口服务

- 问题：论文中使用的微软OCR接口MSCVA，需要申请Azure账号，申请过程中需要VISA信用卡，而我没有VISA信用卡，因此Azure账号无法申请，无法使用微软API

- 解决方案：使用国内OCR接口——百度文字识别接口，它申请难度相对较小。虽然有谷歌的tesseract-ocr，但谷歌的OCR模型识别能力较弱，如果做一些需求量不大的任务，可以考虑百度OCR接口

- 操作流程

  - 首先在<a href=https://ai.baidu.com/tech/ocr>百度AI开放平台</a>上进行账号注册和实名认证。

  - 在控制台“文字识别”模块购买“通用文字识别（标准含位置版）”，注意之所以买含位置版，是因为算法需要使用到识别到的文字位置和CV识别到的轮廓的位置进行比较，若轮廓位置与文字位置相近，说明该轮廓对应于一个文本元素，否则对应于一个图形元素。

  - 在<a href=https://console.bce.baidu.com/ai>控制台</a>页面创建一个新应用，应用名称任意，在文字识别功能中勾选“通用文字识别（标准含位置版）”，文字识别报名选择不需要，应用归属选择个人，简要描述应用后创建之。

  - 创建应用后，在应用列表查看已创建的应用，记录下AppID，API Key和Secret Key三个值

    > 注：由于不同账号的原因，且访问令牌本身一段时间后会过期，可执行文件在OCR识别这一步经检测只能运行在本机，其他机器上可能不能正常运行，目前还没有找到好的解决方法，因此先在视频中展示功能，后续完善此项目时再考虑解决问题。

  - 获取访问令牌：

    ```python
    import requests
    
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的API Key】&client_secret=【官网获取的Secret Key】'
        
    response = requests.get(host)
    if response:
        print(response.json())
    ```

    在 python 中运行此脚本，在输出的json串中找到 'access_token' 字段，此即本账号对应的访问令牌

  - 调用接口：

    - 调用方法：HTTP-RESTful，POST
    - 请求URL：https://aip.baidubce.com/rest/2.0/ocr/v1/general
    - URL参数：access_token，从上一步获取
    - Header：Content-Type : 'application/x-www-form-urlencoded'
    - Body：放置请求参数，参数详情：

> | 参数                  | 是否必选                 | 类型   | 可选值范围                                  | 说明                                                         |
> | --------------------- | ------------------------ | ------ | ------------------------------------------- | ------------------------------------------------------------ |
> | image                 | 和 url/pdf_file 三选一   | string | -                                           | 图像数据，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过4M，最短边至少15px，最长边最大4096px，支持jpg/jpeg/png/bmp格式 **优先级**：image > url > pdf_file，当image字段存在时，url、pdf_file字段失效 |
> | url                   | 和 image/pdf_file 三选一 | string | -                                           | 图片完整url，url长度不超过1024字节，url对应的图片base64编码后大小不超过4M，最短边至少15px，最长边最大4096px，支持jpg/jpeg/png/bmp格式 **优先级**：image > url > pdf_file，当image字段存在时，url字段失效 **请注意关闭URL防盗链** |
> | pdf_file              | 和 image/url 三选一      | string | -                                           | PDF文件，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过4M，最短边至少15px，最长边最大4096px **优先级**：image > url > pdf_file，当image、url字段存在时，pdf_file字段失效 |
> | pdf_file_num          | 否                       | string | -                                           | 需要识别的PDF文件的对应页码，当 pdf_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页 |
> | recognize_granularity | 否                       | string | big/small                                   | 是否定位单字符位置，big：不定位单字符位置，默认值；small：定位单字符位置 |
> | language_type         | 否                       | string | CHN_ENG ENG JAP KOR FRE SPA POR GER ITA RUS | 识别语言类型，默认为CHN_ENG 可选值包括： - CHN_ENG：中英文混合 - ENG：英文 - JAP：日语 - KOR：韩语 - FRE：法语 - SPA：西班牙语 - POR：葡萄牙语 - GER：德语 - ITA：意大利语 - RUS：俄语 |
> | detect_direction      | 否                       | string | true/false                                  | 是否检测图像朝向，默认不检测，即：false。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括: - true：检测朝向； - false：不检测朝向。 |
> | detect_language       | 否                       | string | true/false                                  | 是否检测语言，默认不检测。当前支持（中文、英语、日语、韩语） |
> | paragraph             | 否                       | string | true/false                                  | 是否输出段落信息                                             |
> | vertexes_location     | 否                       | string | true/false                                  | 是否返回文字外接多边形顶点位置，不支持单字位置。默认为false  |
> | probability           | 否                       | string | true/false                                  | 是否返回识别结果中每一行的置信度                             |

- 调用示例：

  请求限制：请求图片需经过base64编码及urlencode后传入

  base64编码通过base64.b64encode(f.read())实现

  - 如果不使用相关工具，可以首先得到图片二进制，去掉编码头后再进行urlencode
  - 如果使用Postman，Python等工具，请求库会自动urlencode，无需自行处理

  ```python
  # encoding:utf-8
  
  import requests
  import base64
  
  request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
  # 二进制方式打开图片文件
  f = open('[本地文件]', 'rb')
  img = base64.b64encode(f.read())
  
  params = {"image":img}
  access_token = '[调用鉴权接口获取的token]'
  request_url = request_url + "?access_token=" + access_token
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  response = requests.post(request_url, data=params, headers=headers)
  if response:
      print (response.json())
  ```

  如果请求成功，将打印出识别结果的json串，此串中含有每个识别文本的内容及'location'信息，这正是我们需要的

### V. 运行程序

- 创建根目录，例如 `/usr/share/meter`，然后 `git clone` 仓库到该根目录下

- 确保测试脚本文件夹 `ApkTestScript` 位于根目录下

- **方法一**：选择一个APP，在根目录下运行如下指令：

  `src/main -a <app_name> -c <script_name> -r <root_path> -o <base_version_apk_path> -n <updated_version_apk_path> -v <based_android_version> -w <updated_android_version> -p <app_package> -t <app_activity>`

  - 例: `src/main -a 'MyTherapy' -c 'MyTherapy 1' -r /home/edenman/桌面/tool-implementation/FAKE_METER-Implementation/ -o /home/edenman/桌面/tool-implementation/FAKE_METER-Implementation/apk/eu.smartpatient.mytherapy-3.31.1-APK4FUN.com.apk -n /home/edenman/桌面/tool-implementation/FAKE_METER-Implementation/apk/eu.smartpatient.mytherapy-3.33-APK4Fun.com.apk -v 7.0 -w 10.0 -p 'eu.smartpatient.mytherapy' -t '.onboarding.WelcomeActivity'`

  - 解释：-a 表示选择的应用名为 MyTherapy，-c 表示脚本名是 MyTherapy 1.py，-r 表示根目录位置，-o 表示原版本 apk 所在位置，-n 表示新版本 apk 所在位置，-v 表示原版本 apk 所安装在设备的安卓版本，这里为7.0，-w 表示新版本apk所安装在设备的安卓版本，-p 表示 app 包名，-t 表示 app 活动名

  - 补充：-p 及 -t 后的参数可以在对应的测试脚本中的注释里找到，如: `MyTherapy 1.py`

    ```python
    # -*- coding:utf8 -*-
    
    import time
    from appium import webdriver
    from selenium.webdriver.common.by import By
    
    desired_caps = {'platformName': 'Android', 'platformVersion': '10.0', 'deviceName': 'emulator-5554', 'appPackage': 'eu.smartpatient.mytherapy', 'appActivity': '.onboarding.WelcomeActivity', 'newCommandTimeout': '1000', 'noReset': True}
    
    driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
    time.sleep(20)
    
    # 
    # reminder time
    el = driver.find_elements(By.CLASS_NAME, "android.widget.Button")[4]
    el.click()
    
    driver.quit()
    
    
    '''
    {
      "platformName": "Android",
      "platformVersion": "10",
      "deviceName": "emulator-5554",
      "noReset": true,
      "appPackage": "eu.smartpatient.mytherapy",
      "appActivity": ".onboarding.WelcomeActivity"
    }
    '''
    ```

    最后的注释中，已经标明了安卓版本，应用包和应用活动等信息，直接复制即可。

- **方法二**：使用 GUI 界面（实际是对方法一的一个封装）

  （待补充）



### VI. 目录结构

```
.
├── apk
│   ├── APK List.md				选取的安卓应用列表及相关说明
│   └── assets
├── ApkTestScript				对应应用的测试脚本（py文件）
│   ├── dianping 1.py
│   └── ......
├── docs						相关文档目录
│   ├── 工具理解.pdf	         工具理解文档
│   ├── README.md			    工具运行流程及相关注解
│   ├── 工具理解.pptx			 工具理解PPT，展示了技术要点和相关问题
│   └── ......
├── final						存储工具运行的结果
│   ├── dianping 1				对应脚本的修复结果
│   └── ......					对应应用的脚本序列执行截图等
├── video						存储讲解视频
│   └── final.mp4
├── README.md					项目简介
└── src							关键模块源文件及可执行文件
```


#### OCR

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
> |                       |                          |        |                                             |                                                              |
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


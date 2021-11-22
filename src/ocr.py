import json

import requests
import base64


def get_text_ocr(filePath):
    TOKEN = '24.1b84780b7c6ca739e3ce7f4ba316336e.2592000.1640141874.282335-25207025'
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general'

    f = open(filePath, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    request_url = request_url + '?access_token=' + TOKEN

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        r = json.loads(response.text)
        return r.get('words_result')

    return 'error'


# if __name__ == '__main__':
#     words = get_text_ocr('01.png')
#     pass

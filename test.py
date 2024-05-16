import os
import re

import ssh_util


def replace_clear(text: str, arr: list):
    if not arr:
        return
    for arr_ in arr:
        text = text.replace(arr_, '')
    return text


def list_name(first: str, arr: list):
    for a in arr:
        if a.__contains__(first):
            return a


def get_source_account_name(ocr_text):
    for text in ocr_text:
        for a in ['Source Account Name:','Debit Account:']:
            if text.__contains__(a):
                return text.replace(a, '')


for file_name in os.popen('ls *.jpg /Users/mac01/Downloads/流水').read().split('\n'):
# img = '2024-05-1123.02.13S.jpg'
#     file_name = '2024-05-1123.02.23S.jpg'
    cmd = f'docker run -v /root/liushui/{file_name}:/tmp/img.jpg jitesoft/tesseract-ocr /tmp/img.jpg stdout'
    # print(cmd)
    ocr_text = ssh_util.exec(cmd)
    print('\n\n' + file_name)
    arr = ocr_text.split('\n')
    if re.findall('\d{30}', ''.join(ocr_text)):
        # print(re.findall('\d{30}', ''.join(ocr_text)))
        pass
    else:
        # print(get_source_account_name(arr))
        print(arr)
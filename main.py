import json
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def bark(device_key, title, content, bark_icon):
    if not device_key:
        return 2

    url = "https://api.day.app/push"
    headers = {
        "content-type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "title": title,
        "body": content,
        "device_key": device_key
    }

    if not bark_icon:
        bark_icon = ''
    if len(bark_icon) > 0:
        url += '?icon=' + bark_icon
        print('拼接icon')
    else:
        print('不拼接icon')

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp_json = resp.json()
    if resp_json["code"] == 200:
        print(f"[Bark]Send message to Bark successfully.")
    if resp_json["code"] != 200:
        print(f"[Bark][Send Message Response]{resp.text}")
        return -1
    return 0


def getqa(soup, month, day):
    message_all = []

    count = 0

    todayNo1 = month + '.' + day
    todayNo2 = month + '月' + day + '日'

    ps = soup.find_all('p')
    for p_ele in ps:
        if count >= 20:
            break

        if (p_ele.text.startswith(todayNo1)):
            message_all.append(p_ele.text + '\n')
            print(p_ele.text)
            answer = p_ele.find_next_sibling('p')
            if answer:
                message_all.append(answer.text + '\n')
                print(answer.text)
        else:
            if (p_ele.text.startswith(todayNo2)):
                message_all.append(p_ele.text + '\n')
                print(p_ele.text)
                answer = p_ele.find_next_sibling('p')
                if answer:
                    message_all.append(answer.text + '\n')
                    print(answer.text)

        count += 1
    return message_all

def getContent(url, month, day):
    # get请求获取内容
    response = requests.get(url)

    # 编码
    response.encoding = response.apparent_encoding

    # 取text属性
    html_content = response.text

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    message_all = getqa(soup, month, day)

    return message_all

def main():
    now = datetime.now()

    month = now.strftime("%m")
    day = now.strftime('%d')

    if month[0] == '0':
        month = month[1:]
    if day[0] == '0':
        day = day[1:]

    url = 'https://m.duotegame.com/mgl/35822.html'
    url1 = 'https://www.youxi369.com/gonglue/49969.html'

    message_all = getContent(url1, month, day)
    if not message_all:
        message_all = getContent(url1, month, day)

    bark_deviceKey = os.environ.get('BARK_DEVICEKEY')
    title = '蚂蚁庄园今日答案'
    message = ''
    bark_icon = os.environ.get('BARK_ICON')

    if not message_all:
        message = '未能查询到当日答案'
    else:
        message_all = '\n'.join(message_all)
        message_all = re.sub('\n+', '\n', message_all).rstrip('\n')
        message = message_all

    bark(bark_deviceKey, title, message, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()

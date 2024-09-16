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


def getQA_DuoTe_35822(soup, year, month, day):
    message_all = []

    count = 0

    todayno1 = month + '.' + day
    todayno2 = month + '月' + day + '日'

    ps = soup.find_all('p')
    for p_ele in ps:
        if count >= 20:
            break

        if p_ele.text.startswith(todayno1):
            message_all.append(p_ele.text + '\n')
            print(p_ele.text)
            answer = p_ele.find_next_sibling('p')
            if answer:
                message_all.append(answer.text + '\n')
                print(answer.text)
        else:
            if p_ele.text.startswith(todayno2):
                message_all.append(p_ele.text + '\n')
                print(p_ele.text)
                answer = p_ele.find_next_sibling('p')
                if answer:
                    message_all.append(answer.text + '\n')
                    print(answer.text)

        count += 1
    return message_all


def getQA_YouXi369_49969(soup, year, month, day):
    message_all = []

    count = 0

    todayno1 = month + '.' + day
    todayno2 = month + '月' + day + '日'

    ps = soup.find_all('p')
    for p_ele in ps:
        if count >= 20:
            break

        if p_ele.text.startswith(todayno1):
            message_all.append(p_ele.text + '\n')
            print(p_ele.text)
        else:
            if p_ele.text.startswith(todayno2):
                message_all.append(p_ele.text + '\n')
                print(p_ele.text)

        count += 1
    return message_all


def getQA_ALi213_371835(soup, year, month, day):
    message_all = []

    count = 0

    todayno1 = '【' + month + '.' + day + '】'

    ps = soup.find_all('p')
    for p_ele in ps:
        if count >= 20:
            break

        if todayno1 in p_ele.text:
            message_all.append(todayno1 + '\n')
            print(todayno1)
            answer1 = p_ele.find_next_sibling('p')
            if answer1:
                message_all.append(answer1.text + '\n')
                print(answer1.text)
                answer2 = answer1.find_next_sibling('p')
                if answer2:
                    message_all.append(answer2.text + '\n')
                    print(answer2.text)

        count += 1
    return message_all


def getQA_M_ALi213_371835(soup, year, month, day):
    message_all = []

    count = 0

    todayno1 = '【' + month + '.' + day + '】'

    ps = soup.find_all('p')
    for p_ele in ps:
        if count >= 20:
            break

        if todayno1 in p_ele.text:
            message_all.append(todayno1 + '\n')
            print(todayno1)
            answer1 = p_ele.find_next_sibling('p')
            if answer1:
                message_all.append(answer1.text + '\n')
                print(answer1.text)
                answer2 = answer1.find_next_sibling('p')
                if answer2:
                    message_all.append(answer2.text + '\n')
                    print(answer2.text)

        count += 1
    return message_all


def getQA_xuexili_jinridaan(soup, year, month, day):
    message_all = []

    count = 0

    todayno1 = year + '年' + month + '月' + day + '日'

    ps = soup.find_all('td')
    for p_ele in ps:
        if count >= 20:
            break

        if todayno1 in p_ele.text:
            answer1 = p_ele.find_next_sibling('td')
            if answer1:
                message_all.append(answer1.text.replace('\n', ''))
                print(answer1.text)
                answer2 = answer1.find_next_sibling('td')
                if answer2:
                    message_all.append(answer2.text.replace('\n', ''))
                    print(answer2.text)

        count += 1

    if message_all:
        message_all.insert(0, todayno1)

    return message_all


def getSoup(url):
    # 设置超时时间为10秒
    timeout = 20

    try:
        # 先打印url
        print(url)

        # get请求获取内容
        response = requests.get(url, timeout=timeout)

        # 编码
        response.encoding = response.apparent_encoding

        # 取text属性
        html_content = response.text

        print(html_content)

        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        return soup
    except requests.exceptions.Timeout:
        print('请求超时')
        soup = BeautifulSoup('', 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(e)
        soup = BeautifulSoup('', 'html.parser')
        return soup


def main():
    now = datetime.now()

    year = now.strftime('%Y')
    month = now.strftime("%m")
    day = now.strftime('%d')

    if month[0] == '0':
        month = month[1:]
    if day[0] == '0':
        day = day[1:]

    url1 = 'https://m.duotegame.com/mgl/35822.html'
    url2 = 'https://www.youxi369.com/gonglue/49969.html'
    url3 = 'https://app.ali213.net/mip/gl/371835.html'
    url4 = 'https://m.ali213.net/news/gl1910/371835.html'
    url5 = 'http://www.xuexili.com/mayizhuangyuan/jinridaan.html'

    soup = None
    message_all = []

    # soup = getSoup(url5)
    # message_all = getQA_xuexili_jinridaan(soup, year, month, day)
    # print(message_all)

    if not message_all:
        soup = getSoup(url1)
        message_all = getQA_DuoTe_35822(soup, year, month, day)
    if not message_all:
        soup = getSoup(url2)
        message_all = getQA_YouXi369_49969(soup, year, month, day)
    if not message_all:
        soup = getSoup(url3)
        message_all = getQA_ALi213_371835(soup, year, month, day)
    if not message_all:
        soup = getSoup(url4)
        message_all = getQA_M_ALi213_371835(soup, year, month, day)
    if not message_all:
        soup = getSoup(url5)
        message_all = getQA_xuexili_jinridaan(soup, year, month, day)

    bark_devicekey = os.environ.get('BARK_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')
    title = '蚂蚁庄园今日答案'
    message = ''

    if not message_all:
        message = '未能查询到当日答案'
    else:
        message_all = '\n'.join(message_all)
        message_all = re.sub('\n+', '\n', message_all).rstrip('\n')
        message = message_all

    bark(bark_devicekey, title, message, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()

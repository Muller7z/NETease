
import requests
from lxml import html
import jsonpath

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding": "deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "keep-alive",
"Cookie":"",
"Host": "music.163.com",
"Referer": "http://music.163.com/",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}


def get_song_info(sid,ip):
    url = 'http://music.163.com/song?id=%s'% sid
    r = requests.get(url,headers=headers,proxies=ip).text
    # print(r)
    e = html.fromstring(r)
    key_word = e.xpath('//meta[@name="keywords"]/@content')[0].split("，")
    # 下面进行格式化的输出内容
    new = []
    if len(key_word) == 2:
        new.append(key_word[0])
        new.append("")
        new.append(key_word[1])
        return new
    if len(key_word) == 3:
        return key_word
    else:
        for each in key_word:
            if each not in new:
                new.append(each)
        n = new[0:2]
        a = ",".join(new[2:])
        n.append(a)
        return n


def get_comment(sid,ip):
    # 抓热门评论
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_%s" % sid
    r = requests.post(url=url,headers=headers,proxies=ip)
    # print(r.text)
    comment = jsonpath.jsonpath(r.json(), "$..content")
    new = []
    for each in comment:
        if each not in new:
            new.append(each)
    return new


def get_lyric(sid,ip):
    # 免验证api , 抓取歌词
    lyric_url = "http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1" % sid
    r = requests.get(lyric_url,headers=headers,proxies=ip)
    # print(r.text)
    lyric =  jsonpath.jsonpath(r.json(), "$..lyric")[0].split("\n")
    # print(lyric)
    # 下面进行歌词的格式化处理，最后输出一个字符串
    new = []
    for each in lyric:
        if len(each[11:]) != 0:
            new.append(each[11:])
    # print(new)
    return ",".join(new)


def get_song_list_from_order(oid):
    url = "http://music.163.com/playlist?id=%s"%oid
    r = requests.get(url,headers=headers).text
    # print(r)
    e = html.fromstring(r)
    # song_name = e.xpath('//ul[@class="f-hide"]/li/a/text()')
    song_id = e.xpath('//ul[@class="f-hide"]/li/a/@href')
    # print(len(song_id))
    # print(song_id)
    # print(song_name)
    sid_list = []
    for i in song_id:
        index = i.index('=')
        id = i[index+1:]
        sid_list.append(id)
    print("抓取到的歌曲ID：")
    print(sid_list)
    # print(len(sid_list))
    return sid_list


def get_some_order(url):
    r = requests.get(url,headers=headers).text
    # print(r)
    e = html.fromstring(r)
    order_id = e.xpath('//p[@class="dec"]/a/@href')
    # print(order_id)
    oid_list = []
    for i in order_id:
        index = i.index('=')
        id = i[index + 1:]
        oid_list.append(id)
    # print(oid_list)
    print("获取到%s个歌单"%len(oid_list))
    return oid_list


if __name__ == '__main__':
    sid = "188989"
    ip = {'port': '22703', 'ip': '183.149.248.176'}
    print(get_comment(sid,ip))
    print(get_lyric(sid,ip))
    print(get_song_info(sid,ip))

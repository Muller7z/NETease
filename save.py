
import time
import xlsxwriter
import json

from spider import *


def proxies():
    # 获取代理ip
    key_1 = "http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=92d3669416c04879a1057087bf203a25&count=1&expiryDate=5&format=1"
    key_2 = "http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=6180a562757748a99346cca5b9964983&count=1&expiryDate=5&format=1"
    key = key_2
    try:
        r = requests.get(key)
        j = r.json()
        if j["code"] == "0":
            return j["msg"]
        else:
            time.sleep(6)
            r = requests.get(key)
            j = r.json()
            return j["msg"]
    except Exception as e:
        print(e)


def save_by_order(oid):
    song_list = get_song_list_from_order(oid)
    worksheet = workbook.add_worksheet(oid)
    x = 0
    worksheet.write(0, x+0, "序号")
    worksheet.write(0, x+1, '歌名')
    worksheet.write(0, x+2, '所属专辑')
    worksheet.write(0, x+3, '歌手')
    worksheet.write(0, x+4, '歌词')
    worksheet.write(0, x+5, '评论')
    # 获取一个代理ip
    ip = proxies()[0]
    for i in range(len(song_list)):

        try:
            print(song_list[i])
            info = get_song_info(song_list[i],ip)
            comment = get_comment(song_list[i],ip)
            lyric = get_lyric(song_list[i],ip)
            new = []
            new.append(str(i+1))
            new.extend(info)
            new.append(lyric)
            new.extend(comment)
            # print(new)
            row = i+1
            for c in range(len(new)):
                worksheet.write(row,c,new[c])
                print(row,c,new[c])

        except Exception as e:
            print(e)
            print("111111")


if __name__ == '__main__':

    with open("config.json","r")as f:
        j = json.load(f)
        print("将要抓取的页面链接 在：config.json中，要抓取其他页面，更新json文件后即可")
        page_name = input("please inter the page number(check it in config.json):")
        url = j[page_name]
    workbook = xlsxwriter.Workbook(page_name + '.xlsx')
    order_id = get_some_order(url)
    for oid in order_id:
        save_by_order(oid)
        time.sleep(10)
    workbook.close()
    print(page_name+"完成！")

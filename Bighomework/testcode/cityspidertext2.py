import urllib.request
import lxml.html
import os
from selenium import webdriver
import re
import json

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131',
    'Cookie':'track_id=117315748041039872; uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; user_city_id=264; ganji_uuid=7256664090169495681743; lg=1; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; guaZiUserInfo=8MS%2By%2BXmcWZGeNXclR86f; userid=745622618; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; antipas=97SvnO322wk56J674305672X7661i; clueSourceCode=%2A%2300; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599142245,1599177060; sessionid=04bc845e-d5b3-4452-8cb8-50d3a1f1d670; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_so.com%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22117315748041039872%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22ca_city%22%3A%22zhanjiang%22%2C%22sessionid%22%3A%2204bc845e-d5b3-4452-8cb8-50d3a1f1d670%22%7D; close_finance_popup=2020-09-04; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A28269999895%7D; cityDomain=zhanjiang; preTime=%7B%22last%22%3A1599181771%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1599181773'
}


def loadin_city_json(data):
    # 保存到文件中
    city_json_path = "./jsonfile/"
    if not os.path.exists(city_json_path):
        os.makedirs(city_json_path)
        print("已成功创建目录%s" % city_json_path)
    else:
        print("目录%s已存在" % city_json_path)
    city_jsonfile_name = city_json_path + "carcity.json"
    with open(city_jsonfile_name, "w") as cityfile:
        cityfile.write(data)
        cityfile.close()
    print("数据已写入%s中" % city_jsonfile_name)


def city_spider():
    # 获取网页数据
    url = "https://www.guazi.com/huzhou/buy/"
    chrome_path = r"D:\shixun\chromedriver.exe"
    brower = webdriver.Chrome(chrome_path)
    brower.get(url)
    city_html = brower.page_source
    # print("网页内容", city_html)

    metree = lxml.html.etree
    city_parser = metree.HTML(city_html)

    # 获取城市数据
    city_list_script = city_parser.xpath("//script")[6]
    city_list_script_text = city_list_script.xpath("./text()")[0]

    # 正则表达式抓取城市json数据
    city_left_pattern = re.compile("{\"A\":.*;")
    city_left_list_str = city_left_pattern.findall(city_list_script_text)[0]
    city_right_pattern = re.compile("{\"N\":.*;")
    city_right_list_str = city_right_pattern.findall(city_list_script_text)[0]
    # print(city_left_list_str)
    # print(city_right_list_str)
    # 将两段数据拼接起来,转换为json格式
    # city_left_list_json = str({"A":[{"id":102089,"domain":"anji","name":"\\u5b89\\u5409","firstC":"A","active":false}]};)
    allcity_list_str =  city_left_list_str[:-2] + "," + city_right_list_str[1:-1]
    print(allcity_list_str)

    brower.quit()
    return allcity_list_str


def main():
    # 爬取城市信息,并返回
    cities_list_str = city_spider()
    # 保存json数据
    loadin_city_json(cities_list_str)


if __name__ == '__main__':
    main()

import urllib.request
import lxml.html
import os
import json
import time
from selenium import webdriver
from random import randint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131', 'cookie': 'track_id=117315748041039872; uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; lg=1; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; antipas=34t01l9jP520j641624l16gF96; close_finance_popup=2020-09-06; clueSourceCode=%2A%2300; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599205178,1599354880,1599360694,1599363348; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; sessionid=b179a35a-b758-494f-8e15-d7a3c07aa704; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_so.com%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22117315748041039872%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22ca_city%22%3A%22zhanjiang%22%2C%22sessionid%22%3A%22b179a35a-b758-494f-8e15-d7a3c07aa704%22%7D; user_city_id=102089; preTime=%7B%22last%22%3A1599369974%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1599369976; lng_lat=110.34328_21.26866; gps_type=1; cityDomain=anji'}
visit_deny_time = randint(1, 5)   # 随机延迟时间


def get_cities_data():
    # 读入json文件，获取城市数据
    json_file = "./jsonfile/citylist.json"
    with open(json_file, "r") as jf:
        city_data = jf.read()
        jf.close()
        city_list = json.loads(city_data)
    # print(city_list)
    return city_list


def download_img(path, addre):
    request_one_car = urllib.request.Request(addre, headers=headers)
    response_one_car = urllib.request.urlopen(request_one_car)
    # time.sleep(2)
    if response_one_car.getcode() == 200:
        car_shop_html = response_one_car.read()
        with open(path, 'wb') as pic:
            pic.write(car_shop_html)
            pic.close()


def get_car_data(city_datas, begin_page, end_page):
    chrome_path = r"D:\shixun\chromedriver.exe"
    carlist_path = "./cavfile/"
    if not os.path.exists(carlist_path):
        os.makedirs(carlist_path)
    carlist_csv = open(carlist_path + 'carlist.csv', 'a', encoding='utf-8')
    # 遍历城市信息
    print(city_datas)
    for alphabet in "BCDEFGHIJKLMNOPQRSTUVWXYZ":
        # print(city_datas[alphabet])
        city_list = city_datas[alphabet]
        # 遍历城市拼音为该字母开头的所有城市
        for city_element in city_list:
            # 获取城市域名和名称
            city_domain = city_element["domain"]
            city_name = city_element["name"]
            city_id = city_element["id"]
            print("城市:%s  %s" % (city_domain, city_name))
            # 爬取该城市每一页的内容
            global_page_num = 0
            for page_num in range(begin_page, end_page + 1):
                global_page_num = page_num
                csv_title = "城市%s,第%d页,汽车名字,图片链接" % (city_name, page_num)
                carlist_csv.write(csv_title + "\n")
                # 发送请求，获取数据
                # https://www.guazi.com/zhanjiang/buy/o50/#bread
                car_shop_addre = "https://www.guazi.com/" + city_domain + "/buy/o" + str(page_num) + "/#bread"
                print("开始爬取数据", car_shop_addre, city_domain, city_id)

                # 访问页面，开始爬取信息
                # brower = webdriver.Chrome(chrome_path)
                # brower.get(car_shop_addre)

                request_car = urllib.request.Request(car_shop_addre, headers=headers)
                response_car = urllib.request.urlopen(request_car)

                # 停留三秒
                time.sleep(3 + visit_deny_time)
                # brower.maximize_window()
                # 两种方法，一种是urllib,一种是selenium
                # car_shop_html_content = brower.page_source
                car_shop_html_content = response_car.read().decode("utf-8")
                if 1:
                    print("正在--%s-->城市--第%d页-->爬取:" % (city_name, page_num))
                    # 获取 etree 对象、获取解析器对象、开始解析,获取汽车数据
                    metree = lxml.html.etree
                    car_html = metree.HTML(car_shop_html_content)
                    carlist_data = car_html.xpath("//ul[@class='carlist clearfix js-top']/li")

                    # 遍历汽车数据
                    car_index = 1
                    for one_car in carlist_data:
                        # 获取汽车名称和链接
                        car_name = one_car.xpath("./a/@title")[0]
                        car_img_src = one_car.xpath("./a/img/@src")[0]
                        # print(car_name,car_img_src)
                        onecar_str = '%s,%s,%s' % (city_name, car_name, car_img_src)
                        carlist_csv.write(onecar_str + '\n')

                        # 下载图片到本地
                        car_img_path = "./carImgs/" + "%s/第%d页/" % (city_name, page_num)
                        if not os.path.exists(car_img_path):
                            os.makedirs(car_img_path)
                        # path = car_img_path + str(car_index) + car_name + ".jpg"
                        path = car_img_path + car_name + ".jpg"
                        print(path)
                        # 开始下载图片，并保存到本地
                        download_img(path, car_img_src)

                        car_index += 1
                    print("爬取完成！！", car_shop_addre)
                else:
                    print("访问失败")
                    break
                # brower.quit()
                print("--%s--第%d页-->爬取数据完毕!!" % (city_name, global_page_num))

        break
    carlist_csv.close()
    '''
    # 爬取该城市每一页的内容
    for page_num in range(begin_page, end_page + 1):
        csv_title = '城市,第%d页,汽车名字,图片链接'%page_num
        carlist_csv.write(csv_title + '\n')
        # 发送请求，获取数据
        # https://www.guazi.com/zhanjiang/buy/o50/#bread
        car_shop_addre = "https://www.guazi.com/zhanjiang/buy/o" + str(page_num) + "/#bread"
        request_car = urllib.request.Request(car_shop_addre, headers=headers)
        response_car = urllib.request.urlopen(request_car)
        if response_car.getcode() == 200:
            car_shop_html = response_car.read().decode("utf-8")
            print("正在爬取:",car_shop_addre)
            # 获取 etree 对象、获取解析器对象、开始解析,获取汽车数据
            metree = lxml.html.etree
            car_html = metree.HTML(car_shop_html)
            carlist_data = car_html.xpath("//ul[@class='carlist clearfix js-top']/li")

            # 遍历汽车数据
            for one_car in carlist_data:
                car_name = one_car.xpath("./a/@title")[0]
                car_img_src = one_car.xpath("./a/img/@src")[0]
                # print(car_name,car_img_src)
                onecar_str = '{},{}'.format(car_name, car_img_src)
                carlist_csv.write(onecar_str + '\n')

                # 下载图片到本地
                car_img_path = "./carImgs/" + "第%d页/"%page_num
                if not os.path.exists(car_img_path):
                    os.makedirs(car_img_path)
                path = car_img_path + car_name + ".jpg"
                print(path)
                # 开始下载图片，并保存到本地
                download_img(path, car_img_src)
            print("爬取完成！！", car_shop_addre)
        else:
            break
    carlist_csv.close()
    print("执行完毕!!")
    '''


def main():
    # 输入爬取的页数
    try:
        # bengin_page, end_page = eval(input("请输入开始爬取的页码:")), eval(input("请输入结束爬取的页码:"))
        bengin_page, end_page = 1, 1
        # 获取所有城市
        city_data_dict = get_cities_data()
        # 获取数据信息
        get_car_data(city_data_dict, bengin_page, end_page)
    except:
        pass


if __name__ == '__main__':
    main()

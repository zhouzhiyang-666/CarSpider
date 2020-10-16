import urllib.request
import herogetAgent
import requests
import proxytool
import lxml.html
import json
import os
from datetime import datetime

def read_json_to_get_data():
    #转换数据类型
    json_data=json.load(open("./jsonfile/carcity.json","r",encoding="utf-8"))
    # print(type(json_data))
    area_name_list=[]
    area_domin_list=[]
    area=[]
    item = {}
    #遍历，分别找出各个字母开头的城市，遍历A->Z,
    for item_data_element in json_data:

        first_word=json_data[item_data_element]
        # print(first_word)
        #遍历，依次从A-z找到‘domin’‘name’
        for word_element in first_word:
            # print(word_element)
            area_name=word_element["name"]
            # item["city_name"]=area_name
            area_domin=word_element["domain"]
            # item[""]
            area_name_list.append(area_name)
            area_domin_list.append(area_domin)
    # print(area_name_list,area_domin_list)
    return area_name_list,area_domin_list


def get_car_index_data(name_data,domin_data):
    """获取1-5页数据，车名，详情链接"""
    # 爬取地址：https://www.guazi.com/zhanjiang/buy/o1/#bread；https://www.guazi.com/zhanjiang/buy/o2/#bread
    car = []
    for name in [name_data[0]]:
        one_city_alldetails_url = []
        car_data_dict = {}
        print("现在爬取的城市是%s" % name)
        print(datetime.now())
        for item in range(1, 51):
            # print(name)
            num = name_data.index(name)
            # car_dir1 = {}
            html_index_url = "https://www.guazi.com/"+domin_data[num]+"/buy/o" + str(item) + "/#bread"
            print(html_index_url)

            # 封装头部和cookie，调用代理池模块
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131",
                "Cookie": "uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; antipas=34Izf01q9X52064162416H96V; lg=1; track_id=123786017047695360; clueSourceCode=%2A%2300; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599385407,1599809664,1599814069,1600834454; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; sessionid=42141127-8810-4cb3-8fcc-a1f94b27ec52; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_so.com%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22123786017047695360%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22sessionid%22%3A%2242141127-8810-4cb3-8fcc-a1f94b27ec52%22%2C%22ca_city%22%3A%22zhanjiang%22%7D; lng_lat=110.34459_21.26748; gps_type=1; close_finance_popup=2020-09-23; cityDomain=zhanjiang; user_city_id=264; preTime=%7B%22last%22%3A1600834471%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1600834473"
            }
            request_obj = requests.get(html_index_url,
                                       headers=headers,
                                       proxies=proxytool.get_proxies())
            # 获取数据 ----列表类型
            car_content = request_obj.content.decode("utf-8")
            print("正在爬取第%d页" % item)
            # 找到节点，使用lxml获取部分数据内容
            parser = lxml.html.etree.HTML(car_content)
            index_jd = parser.xpath("//ul[@class='carlist clearfix js-top']/li")
            # print(index_jd)
            # 遍历获取信息（车名和详情链接）
            for car_element in index_jd:
                # car_name = car_element.xpath("./a/@title")[0]
                car_detail_url = "https://www.guazi.com" + car_element.xpath("./a/@href")[0]
                # print(len(car_detail_url))
                one_city_alldetails_url.append(car_detail_url)
                # print(car_detail_url_list)
        car_data_dict["city_name"] = name
        car_data_dict["detail_url"] = one_city_alldetails_url
        # print(car_data_dict)
        car.append(car_data_dict)
        # print(car)
        make_car_data_json(car)
        print(datetime.now())


def make_car_data_json(data):
    """制作json文件，[{车名，详情链接}]"""
    file_path="./jsonfile/cardetailfile"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    #转换格式。python数据类型-->json格式
    car_data_json = json.dumps(data, ensure_ascii=False, indent=2)
    #打开文件
    car_data_file = open(file_path+"/domain3.json", "w", encoding="utf-8")
    #写入内容
    car_data_file.write(car_data_json)
    #关闭文件
    car_data_file.close()
    print("数据保存成功")


def main():
    car_index_area_name,car_index_ares_domin=read_json_to_get_data()
    car_data=get_car_index_data(car_index_area_name,car_index_ares_domin)



if __name__ == '__main__':
    main()
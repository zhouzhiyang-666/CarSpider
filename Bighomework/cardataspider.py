import requests
import herogetAgent
import proxytool
import lxml.html
import json


def catch_index():
    car_data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131"}
    cookie = {
        "Cookie": "uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; antipas=34Izf01q9X52064162416H96V; lg=1; track_id=123786017047695360; clueSourceCode=%2A%2300; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599385407,1599809664,1599814069,1600834454; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; sessionid=42141127-8810-4cb3-8fcc-a1f94b27ec52; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_so.com%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22123786017047695360%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22sessionid%22%3A%2242141127-8810-4cb3-8fcc-a1f94b27ec52%22%2C%22ca_city%22%3A%22zhanjiang%22%7D; lng_lat=110.34459_21.26748; gps_type=1; close_finance_popup=2020-09-23; cityDomain=zhanjiang; user_city_id=264; preTime=%7B%22last%22%3A1600835987%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1600835989"
    }
    headers.update(cookie)
    all_data_list = []

    city_file = open("./carjsonfile/domain.json", "r", encoding="utf-8")
    city_data = json.load(city_file)
    for item in city_data:
        # print(item['city_name'])
        city_name = item['city_name']
        # city_list.append(item['city_name'])
        detail_list = item['detail_url']
        print("正在爬取城市--%s--的数据" % city_name)
        all_car_list = []

        for temp in detail_list:
            print("正在抓取第--(%s)--个汽车详情数据！！%s" % (detail_list.index(temp),temp))
            car_data = {}
            response = requests.get(temp,
                                    headers=headers,
                                    proxies=proxytool.get_proxies()
                                    )
            res = response.text
            # print(res)

            parser = lxml.html.etree.HTML(res)

            # 车名
            car_name_list = parser.xpath("//h2[@id='base']/span/text()")
            # print(car_name_list)
            for car_name in car_name_list:
                car_name = car_name.strip()
                car_name = car_name[0:-5]
                car_data["carname"] = car_name

            # 基本参数
            base_data_key = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[1]/tr/td[@class='td1']/text()")
            base_data_value = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[1]/tr/td[@class='td2']/text()")
            base_data = dict(zip(base_data_key, base_data_value))
            # print(base_data)
            car_data["基本参数"] = base_data
            # print(base_dict)

            # 发动机参数
            engine_data_key = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[2]/tr/td[@class='td1']/text()")
            engine_data_value = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[3]/tr/td[@class='td2']/text()")
            engine_data = dict(zip(engine_data_key, engine_data_value))
            # print(base_data)
            car_data["发动机参数"] = engine_data
            # print(engine_dict)

            # 底盘及制动
            chassis_data_key = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[2]/tr/td[@class='td1']/text()")
            chassis_data_value = parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[3]/tr/td[@class='td2']/text()")
            chassis_data = dict(zip(chassis_data_key, chassis_data_value))
            # print(base_data)
            car_data["底盘及制动"] = chassis_data

            # print("正在爬取汽车--%s--的数据" % car_name)
            all_car_list.append(car_data)
            #
            # # for item in city_list:
            # #     all_data_dict={item:all_car_list}
        all_data_dict={}
        all_data_dict['city_name']=city_name
        all_data_dict['car_list']=all_car_list
        all_data_list.append(all_data_dict)
        save_data(all_data_list)
        print("---------爬完！！！")
        # print(all_data_list)


def save_data(datas):
    with open("./carjsonfile/car_data3.json","w",encoding="utf-8") as car_file:
        data=json.dumps(datas, ensure_ascii=False,indent=2)
        car_file.write(data)


def main():
    data=catch_index()


if __name__ == '__main__':
    main()

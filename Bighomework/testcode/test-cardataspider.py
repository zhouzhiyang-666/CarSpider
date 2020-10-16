import requests
import herogetAgent
import proxytool
import lxml.html
import json
from queue import Queue
from threading import Thread
import time


class CarDetailSipder(object):
    def __init__(self):
        self.headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131"}
        self.cookie = {
            "Cookie": "uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; cityDomain=zhanjiang; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599363348,1599385407,1599809664,1599814069; antipas=34Izf01q9X52064162416H96V; user_city_id=264; lg=1; close_finance_popup=2020-09-21; clueSourceCode=%2A%2300; sessionid=54056c1a-5cdc-4432-89b2-8abdd84c3a57; lng_lat=110.34459_21.26748; gps_type=1; track_id=123770519561375744; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e7%25bd%2591%22%7D; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22pcbiaoti%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e7%25bd%2591%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22123770519561375744%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22sessionid%22%3A%2254056c1a-5cdc-4432-89b2-8abdd84c3a57%22%2C%22ca_city%22%3A%22zhanjiang%22%7D; preTime=%7B%22last%22%3A1600664394%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D"}
        self.headers.update(self.cookie)
        # 存放详情地址队列
        self.car_detail_url_queue = Queue()
        # 存放配置信息队列
        self.car_detail_queue = Queue()
        self.car_data = {}
        self.all_car_list = []
        self.all_data_list = []
        self.tag = "安吉"

    def read_car_detail_url(self):
        city_file = open("../jsonfile/domain.json", "r", encoding="utf-8")
        city_data = json.load(city_file)
        for city_element in city_data:
            # print(item['city_name'])
            city_name = city_element['city_name']
            # city_list.append(item['city_name'])
            detail_list = city_element['detail_url']
            # print("正在读取%s的数据" % city_name)
            for temp in detail_list:
                self.car_detail_url_queue.put([city_name, temp])
            # time.sleep(3)
            # print("------（%s）-----的数据已读取完成！！！" % city_name)
        print("城市信息已全部入队！！！")

    def catch_index(self):
        while True:
            detail = self.car_detail_url_queue.get()
            city_name, detail_url = detail[0], detail[1]
            # print(city_name, detail_url)
            # 跳出循环条件
            # print(car_data)
            if city_name != self.tag:
                self.all_data_dict = {}
                self.all_data_dict['city_name'] = self.tag
                self.all_data_dict['car_list'] = self.all_car_list
                self.all_data_list.append(self.all_data_dict)
                self.car_detail_queue.put(self.all_data_list)
                print("--(%s)--爬取完成!!!" % self.tag)
                print(self.all_data_list)
                self.all_car_list = []
                self.all_data_list = []
                self.tag = city_name
                # print(all_data_list)

            response = requests.get(detail_url,
                                    headers=self.headers,
                                    proxies=proxytool.get_proxies()
                                    )
            detail_text = response.text
            detail_parser = lxml.html.etree.HTML(detail_text)

            # 车名
            car_name_list = detail_parser.xpath("//h2[@id='base']/span/text()")
            self.car_data = {}
            for car_name in car_name_list:
                car_name = car_name.strip()
                car_name = car_name[0:-5]
                self.car_data["carname"] = car_name

            # 基本参数
            base_data_key = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[1]/tr/td[@class='td1']/text()")
            base_data_value = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[1]/tr/td[@class='td2']/text()")
            base_data = dict(zip(base_data_key, base_data_value))
            # print(base_data)
            self.car_data["基本参数"] = base_data
            # print(base_dict)

            # 发动机参数
            engine_data_key = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[2]/tr/td[@class='td1']/text()")
            engine_data_value = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[3]/tr/td[@class='td2']/text()")
            engine_data = dict(zip(engine_data_key, engine_data_value))
            # print(base_data)
            self.car_data["发动机参数"] = engine_data
            # print(engine_dict)

            # 底盘及制动
            chassis_data_key = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[2]/tr/td[@class='td1']/text()")
            chassis_data_value = detail_parser.xpath(
                "//div[@class='detailcontent clearfix js-detailcontent active']/table[3]/tr/td[@class='td2']/text()")
            chassis_data = dict(zip(chassis_data_key, chassis_data_value))
            # print(base_data)
            self.car_data["底盘及制动"] = chassis_data
            # print(chassis_dict)
            # print("正在爬取%s的数据" % car_name)
            self.all_car_list.append(self.car_data)
            self.car_detail_url_queue.task_done()

    def save_data(self):
        while True:
            data = self.car_detail_queue.get()
            # print(data)
            city_name = data[0]['city_name']
            path = "./" + city_name + ".json"
            json.dump(data,
                      open(path, "w", encoding="utf-8"),
                      ensure_ascii=False,
                      indent=2)
            self.car_detail_queue.task_done()
            # print("--(%s)--" % data[0])

    def start(self):
        start = time.time()
        # 存放线程列表
        thread_list = []
        # 读取汽车详情页线程
        read_url_thread = Thread(target=self.read_car_detail_url)
        thread_list.append(read_url_thread)
        # 存取汽车数据线程
        get_detail_thread = Thread(target=self.catch_index)
        thread_list.append(get_detail_thread)
        # 写入数据线程
        laodin_detail_thread = Thread(target=self.save_data)
        thread_list.append(laodin_detail_thread)
        # 启动线程
        for thread_temp in thread_list:
            # 方法二,线程设定为守护线程
            # thread_temp.setDaemon(True)    # 多个线程互抢内存资源情况
            thread_temp.start()

        # 启动队列
        for temp_queue in [self.car_detail_url_queue, self.car_detail_queue]:
            temp_queue.join()


def main():
    car_detail_spider = CarDetailSipder()
    car_detail_spider.start()


if __name__ == '__main__':
    main()

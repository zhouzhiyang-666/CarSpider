import requests
import lxml.html
import json
import time
from random import randint
import herogetAgent
import os
requests.packages.urllib3.disable_warnings()


class IpProxySpider(object):
    def __init__(self):
        self.ip_url = "https://www.kuaidaili.com/free/inha/{}/"
        self.ip_list = []
        # self.http_proxy = {"HTTP":"https://163.125.223.3"}

    def catch_ip_proxy(self, begin, end):
        for index in range(begin, end + 1):
            ip_url = self.ip_url.format(index)
            ip_response = requests.get(ip_url,
                                       headers=herogetAgent.get_header(),
                                       verify=False)
            # 延时3-6s
            time.sleep(1 + randint(1, 3))
            ip_url_html = ip_response.content.decode("utf-8")
            ip_parser = lxml.html.etree.HTML(ip_url_html)
            web_tr = ip_parser.xpath("//div[@id='list']/table/tbody//tr")
            for tr_element in web_tr:
                proxy = {}
                ip = tr_element.xpath("./td[1]/text()")[0]
                port = tr_element.xpath("./td[2]/text()")[0]
                type_1 = tr_element.xpath("./td[4]/text()")[0]
                #  HTTP,HTTPS的情况，取HTTP
                if "," in type_1:
                    type_1 = ",".split(type_1)[0]

                # print(ip_info)
                # {'IP': '60.168.80.138', 'PORT': '1133', 'TYPE': 'HTTP'}
                # http://60.168.80.138:1133
                proxy[type_1] = type_1.lower() + "://" + ip + ":" + port
                self.ip_list.append(proxy)
            # 把数据写进去
            self.loadin_json(self.ip_list, index)
            print("爬取第%d页完成!!" % index)

    def loadin_json(self, data, page):
        print("正在写入第%d页代理数据" % page)
        json_path = "./jsonfile/"
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        json.dump(data,
                  open(json_path + "proxyipdata3.json", "w"),
                  indent=2)

    def start(self):
        # 爬取第几页
        begin_page, end_page = int(input("请输入开始页码:")), int(input("请输入结束页码:"))
        self.catch_ip_proxy(begin_page, end_page)
        # proxy_ip_list = self.ip_list


if __name__ == '__main__':
    spider = IpProxySpider()
    spider.start()

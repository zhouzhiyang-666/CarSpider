import requests
import proxytool
import lxml.html
import json


class CarDetailSpider(object):
    def __init__(self):
        # 存取所有汽车详情数据,   存取汽车名称+详情信息
        self.car_details = []
        # 地址模板
        self.car_url = "https://www.guazi.com/zhanjiang/buy/o{}/#bread"

    def get_car_datas(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131',
            'Cookie': 'uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; lg=1; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599354880,1599360694,1599363348,1599385407; track_id=120084697640050688; antipas=9S7ntk32256O6743056727661V; cityDomain=zhanjiang; clueSourceCode=%2A%2300; user_city_id=264; sessionid=95d4e8e2-d48c-493c-c979-ab62a43e8229; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22pcbiaoti%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22120084697640050688%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22ca_city%22%3A%22zhanjiang%22%2C%22sessionid%22%3A%2295d4e8e2-d48c-493c-c979-ab62a43e8229%22%7D; lng_lat=110.3486_21.26925; gps_type=1; close_finance_popup=2020-09-11; preTime=%7B%22last%22%3A1599785918%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A32343558084%7D'}
        # https://www.guazi.com/zhanjiang/buy/o2/#bread

        # 爬取第1-10页面数据
        for page_num in range(1, 11):
            one_url = self.car_url.format(page_num)
            car_response = requests.get(one_url, headers=headers, proxies=proxytool.get_proxies())
            # print(car_response.text)
            # 获取页面源码
            car_html_content = car_response.text
            car_parser = lxml.html.etree.HTML(car_html_content)
            li_list = car_parser.xpath("//ul[@class='carlist clearfix js-top']/li")

            for li_element in li_list:
                car_temp = {}
                # 获取汽车名字和详情地址
                car_name = li_element.xpath("./a/@title")[0]
                car_detail_url = "https://www.guazi.com" + li_element.xpath("./a/@href")[0]
                # print("汽车名称:%s--汽车详情页:%s" % (car_name, car_detail_url))
                car_temp["car_name"] = car_name
                car_temp["car_detail_url"] = car_detail_url
                self.car_details.append(car_temp)
            # 提示信息
            print("---->第%d页数据爬取完成-----" % page_num)

    def loadin_json(self, data):
        file_path = "./jsonfile/cardetails.json"
        json.dump(data,
                  open(file_path, "w", encoding="utf-8"),
                  ensure_ascii=False,
                  indent=2)
        print("------数据已写入完成!!------")

    def start(self):
        # 获取页面数据信息
        self.get_car_datas()
        # 存入json文件
        self.loadin_json(self.car_details)


def main():
    car_detail_spiser = CarDetailSpider()
    car_detail_spiser.start()


if __name__ == '__main__':
    main()

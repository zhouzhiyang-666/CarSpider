import urllib.request
import herogetAgent
import requests
import proxytool
import lxml.html
import json
import os

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
    for name in name_data:
        one_city_alldetails_url = []
        car_data_dict = {}
        print("现在爬取的城市是%s" % name)
        for item in range(1, 3):
            # print(name)
            num = name_data.index(name)
            # car_dir1 = {}
            html_index_url = "https://www.guazi.com/"+domin_data[num]+"/buy/o" + str(item) + "/#bread"

            # 封装头部和cookie，调用代理池模块
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
                "Cookie": "uuid=4dd9a195-6042-4007-8d12-af15404ca469; ganji_uuid=7986487939725663517305; lg=1; close_finance_popup=2020-09-11; __utmganji_v20110909=11fdc737-74a7-4670-fbee-e2e09cbb01bf; antipas=cwc8o048p6c218044062wJ55SBG; user_city_id=102089; clueSourceCode=%2A%2300; preTime=%7B%22last%22%3A1599828755%2C%22this%22%3A1599785184%2C%22pre%22%3A1599785184%7D; sessionid=3b98f574-c957-4b4c-eb04-24ff9e26e049; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599811279,1599811592,1599828474,1599828756; cityDomain=su; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%224dd9a195-6042-4007-8d12-af15404ca469%22%2C%22ca_city%22%3A%22zhanjiang%22%2C%22sessionid%22%3A%223b98f574-c957-4b4c-eb04-24ff9e26e049%22%7D; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A75189083761%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1599828814"}
            request_obj = requests.get(html_index_url,
                                       headers=herogetAgent.get_header(),
                                       proxies=proxytool.get_proxies())
            # 获取数据 ----列表类型
            car_content = request_obj.content.decode("utf-8")
            # print(car_content)
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



def make_car_data_json(data):
    """制作json文件，[{车名，详情链接}]"""
    file_path="./jsonfile/cardetailfile"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    #转换格式。python数据类型-->json格式
    car_data_json = json.dumps(data, ensure_ascii=False, indent=2)
    #打开文件
    car_data_file = open(file_path+"/domain.json", "w", encoding="utf-8")
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
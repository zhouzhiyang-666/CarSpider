import json
from random import randint


def read_proxy_json_file():
    ip_proxies_file = "../jsonfile/proxiespool.json"
    # 导入json数据
    ip_proxy_data = json.load(open(ip_proxies_file, "r"))
    return ip_proxy_data


def get_proxies():
    # 获取代理池数据
    ip_proxy_datas = read_proxy_json_file()
    ip_index = randint(0, len(ip_proxy_datas)-1)
    # print("代理地址为：", ip_proxy_datas[ip_index])
    return ip_proxy_datas[ip_index]


if __name__ == '__main__':
    ip_proxy = get_proxies()

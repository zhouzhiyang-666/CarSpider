import json
import requests
import herogetAgent
requests.packages.urllib3.disable_warnings()


def main():
    # 访问百度验证
    baidu = "https://www.sohu.com/"
    use_ip_proxy = []
    ip_proxy_path = "./jsonfile/proxyipdata3.json"
    # 加载数据
    ip_proxy_datas = json.load(open(ip_proxy_path,"r"))

    # print(ip_proxy_datas)

    # 遍历代理地址
    try:
        for ip_element in ip_proxy_datas:
            # 验证,访问,设置访问超时
            # print(http_element)

            # print("开始验证 %s" % ip_element)
            ip_response = requests.get(baidu,
                                       headers=herogetAgent.get_header(),
                                       proxies=ip_element,
                                       verify=False
                                       )

            # time.sleep(2 + randint(1,4))
            # print(ip_response.status_code)
            if ip_response.status_code == 200:
                print("--%s->ip地址请求成功" % ip_element)
                use_ip_proxy.append(ip_element)
                json.dump(use_ip_proxy,
                          open("./jsonfile/proxiespool2.json", "w"),
                          indent=2)
            else:
                # print("--%s->ip地址请求失败" % http_element)
                continue
        print("----------------------------->验证完成!!")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

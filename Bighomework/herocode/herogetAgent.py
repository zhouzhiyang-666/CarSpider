import random
# 动态获取agent
user_agent = [
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"},
{"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"},
{"User-Agent": "Opera/8.0 (Windows NT 5.1; U; en)"},
{"User-Agent": "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"},
{"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"},
{"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"},
{"User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
{"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"},
{"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"},
{"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360SE/12.1.2812.0"},
{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}
]


def get_header():
    index = random.randint(0, len(user_agent)-1)
    # print(user_agent[index])
    # headers = user_agent[index]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.8131"}
    cookie = {"Cookie": "uuid=d12bc33e-3ee0-4558-8d6f-2892ce738313; ganji_uuid=7256664090169495681743; GZ_TOKEN=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; CHDSSO=8998YpdvkymfX5MfmIFOzSved8oVAnyLhW%2FJG16lFKyu2K8smXex69YLZpudxA3V3gYT%2FF%2FD7wMVbT2xOo24I6frhSVsY%2B7Hgsqvt8khT7qIHeP1GdITlLVpehbyiURjNZpkPh4eAwa%2FUXK2TA; cityDomain=zhanjiang; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1599363348,1599385407,1599809664,1599814069; antipas=34Izf01q9X52064162416H96V; user_city_id=264; lg=1; close_finance_popup=2020-09-21; clueSourceCode=%2A%2300; sessionid=54056c1a-5cdc-4432-89b2-8abdd84c3a57; lng_lat=110.34459_21.26748; gps_type=1; track_id=123770519561375744; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e7%25bd%2591%22%7D; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22pcbiaoti%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e7%25bd%2591%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%22123770519561375744%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d12bc33e-3ee0-4558-8d6f-2892ce738313%22%2C%22sessionid%22%3A%2254056c1a-5cdc-4432-89b2-8abdd84c3a57%22%2C%22ca_city%22%3A%22zhanjiang%22%7D; preTime=%7B%22last%22%3A1600664394%2C%22this%22%3A1599125454%2C%22pre%22%3A1599125454%7D"}
    headers.update(cookie)
    return headers


if __name__ == '__main__':
    get_header()

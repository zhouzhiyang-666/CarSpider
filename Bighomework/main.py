from testcode import climbcartest2, cityspidertext2


def main():
    # 获取页面数据存入json中
    climbcartest2.main()
    # 爬取城市信息,写入json文件
    cityspidertext2.main()
    # 爬取所有城市汽车详情页
    # 对详情页请求数据，获取汽车配置信息


if __name__ == '__main__':
    main()


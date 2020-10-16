import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.sans-serif'] = 'SimHei'


class AnalyseCar(object):
    def __init__(self):
        pass

    def read_car_datas(self):
        car_detail_file = "./carjsonfile/car_data2.json"
        car_detail_list = json.load(open(car_detail_file, "r", encoding="utf-8"))
        # print(car_detail_list)
        return car_detail_list

    def draw_plot(self, details):
        car_data = []
        while True:
            # need_city = input("请输入要分析的城市中文名:")
            need_city = "安吉"
            for element in details:
                if element["city_name"] == need_city:
                    car_data = element["car_list"]
                    break
                else:
                    continue
            if car_data == []:
                print("没有该城市数据，请重新输入!!!")
            else:
                break
        # print(car_data)
        if car_data != []:
            firm_data = []
            firm_num = []
            for temp in car_data:
                # 厂商
                one_firm = temp["基本参数"].get("厂商", "暂无数据")
                # print(one_firm)
                firm_data.append(one_firm)
            firm_set = set(firm_data)
            unique_firm = list(firm_set)
            for firm_temp in unique_firm:
                number = firm_data.count(firm_temp)
                firm_num.append(number)

            plt.figure(figsize=(16, 10), dpi=100)
            plt.title("城市名称：(%s)--汽车数据厂商分析" % need_city)
            plt.xlabel("厂商名称")
            plt.ylabel("厂商数目")
            plt.ylim(0, 10)
            plt.plot(unique_firm, firm_num, linewidth=1.0, color="b", label="厂商")
            plt.yticks([i for i in range(0, max(firm_num) + 5)])
            plt.xticks(rotation=90)  # 这里是调节横坐标的倾斜度，rotation是度数
            # 绘制点
            draw_list = []
            index = 0
            while index < len(unique_firm):  # str(int(name_bili[index]*1000)/10)
                draw_list.append((unique_firm[index], firm_num[index]))
                draw_list.sort(key=lambda x: x[1],reverse=True)
                index += 1
            rank = 0
            # print(draw_list)
            # 标识前3名厂商的数据
            while rank < 3:  # str(int(name_bili[index]*1000)/10)
                plt.text(draw_list[rank][0], draw_list[rank][1],
                         draw_list[rank][0] + "," + str(draw_list[rank][1]),
                         color="red")
                plt.scatter(draw_list[rank][0], draw_list[rank][1], marker='.', color='green', s=80)
                rank += 1
            plt.grid(axis='both', which='major', ls="--", alpha=0.5)
            plt.show()

    def start(self):
        # 读取数据
        car_details = self.read_car_datas()
        # 绘制柱状图
        self.draw_plot(car_details)


def main():
    analyse_car = AnalyseCar()
    analyse_car.start()


if __name__ == '__main__':
    main()

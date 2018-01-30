# -*- coding:utf-8 -*-
# Author Hsinhan Chiang
from pyecharts import Line, Page


def list2attr(list):
    count = 0
    day_num = 1
    day = 'day' + str(day_num)
    splited_list = list.split()
    attr, v = [], []
    for i in splited_list:
        if '-' in i:
            attr.append(day + ' ' + splited_list[count + 1])
        elif ':' in i:
            if i[0:2] == '01':
                day = 'day' + str(day_num)
                day_num += 1
        else:
            v.append(i)
        count += 1
    return attr, v


def make_line(list, tips, unit):
    attr1, v1 = list2attr(list[0])
    attr2, v2 = list2attr(list[1])
    line = Line(tips)
    line.add("上周", attr1, v1,
             mark_point=["max", "min"], mark_line=["average"])
    line.add("本周", attr2, v2,
             mark_point=["max", "min"], mark_line=["average"],
             yaxis_formatter=unit)
    return line


week_report = open('week_report', 'rb')
week_report_str = week_report.read()
week_report_list = week_report_str.split('FROM_UNIXTIME(clock)	value_max')
tips_list = ["10.151.4.30 CPU", "10.151.4.30 内存", "10.151.4.30 磁盘", "10.151.4.71 CPU", "10.151.4.71 内存",
             "10.151.4.71网络", "10.151.4.71磁盘", "核心交换机CPU", "核心交换机内存", "移动网络流量", "电信网络流量",
             "人保金服到集团核心网RT1", "人保金服到集团核心网RT2", "人保金服到华夏银行RT1", "人保金服到华夏银行RT2"]
unit_list = ["%", "%", "GB", "%", "%", "Kbps", "GB", "%", "%", "Kbps", "Kbps", "Kbps", "Kbps", "bps", "Kbps"]
page = Page()
count = 0
list_count = 1
for tips in tips_list:
    line = make_line(week_report_list[list_count:list_count + 2], tips, unit_list[count])
    count += 1
    list_count += 2
    page.add(line)
page.render()

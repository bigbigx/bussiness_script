# -*- coding:utf-8 -*-
# Author Hsinhan Chiang
from pyecharts import Line, Page


def handle_memory(mem_list):
    count = 0
    for i in mem_list:
        mem_list[count] = 67428462592 - i
        count += 1


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
            v.append(int(i.replace('.', '')))
        count += 1
    return attr, v


def chang_value(value_list, level):
    count = 0
    for v in value_list:
        value_list[count] = v * level
        count += 1


def make_line(list, tips, unit, level,count):
    attr_lastweek, value_lastweek = list2attr(list[0])
    attr_thisweek, value_thisweek = list2attr(list[1])
    if count in [1,4,]:
        handle_memory(value_thisweek)
        handle_memory(value_lastweek)
    chang_value(value_lastweek, level)
    chang_value(value_thisweek, level)
    line = Line(tips)
    line.add("上周", attr_lastweek, value_lastweek,
             mark_line=["max"],is_smooth=True)
    line.add("本周", attr_thisweek, value_thisweek,
             mark_line=["max"],
             yaxis_formatter=unit,is_smooth=True)
    return line


week_report = open('week_report-20180202', 'rb')
week_report_str = week_report.read().decode()
week_report_list = week_report_str.split('FROM_UNIXTIME(clock)	value_max')
tips_list = ["10.151.4.30 CPU", "10.151.4.30 内存", "10.151.4.30 磁盘", "10.151.4.71 CPU", "10.151.4.71 内存",
             "10.151.4.71网络", "10.151.4.71磁盘", "核心交换机CPU", "核心交换机内存", "移动网络流量", "电信网络流量",
             "人保金服到集团核心网RT1", "人保金服到集团核心网RT2", "人保金服到华夏银行RT1", "人保金服到华夏银行RT2"]
unit_list = ["%", "MB", "GB", "%", "MB", "Kbps", "GB", "%", "%", "Kbps", "Kbps", "Kbps", "Kbps", "bps", "Kbps"]
level_list = [0.01, 0.000001, 0.000000001, 0.01, 0.000001, 0.0001, 0.000000001, 1, 1, 0.0001, 0.0001,0.0001, 0.0001, 1, 0.0001]
page = Page()
count = 0
list_count = 1
for tips in tips_list:
    line = make_line(week_report_list[list_count:list_count + 2], tips, unit_list[count], level_list[count],count)
    count += 1
    list_count += 2
    page.add(line)
page.render()

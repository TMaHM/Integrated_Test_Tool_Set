"""
读取一个mac_list，以URL的格式输出到文件phones_url中，方便统计ip，以供AutoTest脚本使用
TODO：1.GUI 2.以函数重构 3.形成exe文件
"""

import re

ip_mac = {}
url_list = []
patt_mac = r'00[-:]?1\w[-:]?\w1[-:]?\w\w[-:]?\w\w[-:]?\w\w'
# 这里可能有问题，当前匹配以6，8，9开头，后面跟2个数字，最后可能有字母的一个组合，后期再改进 TODO
patt_judge_type = r'[6,8,9]\d\d\w*'

# 从mac_list文件中读取mac和model，允许没有model，字典中value为None
with open('mac_list.txt') as f_obj:
    for eachline in f_obj:
        judge_type = re.search(patt_judge_type, eachline[-5:-1])
        result = re.search(patt_mac, eachline)
        # 将result--mac作为key，因为mac不会重复，而model会重复，以免key重复，将值覆盖
        if (judge_type is not None) and (result is not None):
            try:
                mac = result.group()
                type = judge_type.group()
                ip_mac[mac] = type
            except TypeError:
                pass
        elif (judge_type is None) and (result is not None):
            try:
                mac = result.group()
                type = ""
                ip_mac[mac] = type
            except TypeError:
                pass

# 将读取到的mac地址转换为统一格式，以用于匹配IPMac的结果(例如：00-1F-C1-1D-2C-E8)
patt_format = r'^00-1\w-\w1-\w\w-\w\w-\w\w'
patt_grouping = r'(00)[:-]?(1\w)[:-]?(\w1)[:-]?(\w\w)[:-]?(\w\w)[:-]?(\w\w)[:-]?'

for key, value in ip_mac.items():
    formatted = re.match(patt_format, key)
    format_mac = re.match(patt_grouping, key)
    # 如果不是标准格式，转换为标准格式(这里其实可以不用if判断，直接全部转换，但是哪种方法效率更高呢？TODO)
    if not formatted:
        mac = format_mac.group(1).upper() + '-' + format_mac.group(2).upper(
        ) + '-' + format_mac.group(3).upper() + '-' + format_mac.group(
            4).upper() + '-' + format_mac.group(
                5).upper() + '-' + format_mac.group(6).upper()
        del ip_mac[key]
        ip_mac[mac] = value

with open('IPMac.txt') as f:
    counts = 0
    for eachline in f:
        read_mac = re.search(patt_mac, eachline)
        read_ip = re.split(r'\s', eachline.strip())
        if read_mac is not None:
            for mac in ip_mac.keys():
                if mac == read_mac.group() and ip_mac[mac]:
                    url = ("\"" + "http://" + read_ip[1] + "/AutoTest&" + "\""
                           + "\t#" + ip_mac[mac] + '\t' + mac)
                    url_list.append(url)
                    counts += 1
                # ip_mac[mac]-->model为空的情况，此时用\t替代model的位置，以保持输出格式
                elif mac == read_mac.group() and not ip_mac[mac]:
                    url = ("\"" + "http://" + read_ip[1] + "/AutoTest&" + "\""
                           + "\t#" + "\t" + '\t' + mac)
                    url_list.append(url)
                    counts += 1

with open('phones_url.txt', 'w') as f:
    for count, url in zip(range(1, counts + 1), url_list):
        f.write("URL" + str(count) + url + "\n")

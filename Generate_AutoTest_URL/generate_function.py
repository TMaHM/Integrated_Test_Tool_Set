import re


ip_mac_dir = {}
url_list = []
patt_mac = r'00[-:]?1\w[-:]?\w1[-:]?\w\w[-:]?\w\w[-:]?\w\w'
patt_judge_model = r'[6,8,9]\d\d\w*'


def read_mac(phones_mac):
    with open(phones_mac) as f_obj:
        for eachline in f_obj:
            if len(eachline) <= 17:
                judge_model = None
            else:
                judge_model = re.search(patt_judge_model, eachline[-5:-1])
            result = re.search(patt_mac, eachline)
            # 将result--mac作为key，因为mac不会重复，而model会重复，以免key重复，将值覆盖
            if (judge_model is not None) and (result is not None):
                try:
                    mac = result.group()
                    model = judge_model.group()
                    ip_mac_dir[mac] = model
                except TypeError:
                    pass
            elif (judge_model is None) and (result is not None):
                try:
                    mac = result.group()
                    model = " "
                    ip_mac_dir[mac] = model
                except TypeError:
                    pass


def get_ip():
    patt_format = r'^00-1\w-\w1-\w\w-\w\w-\w\w'
    patt_grouping = r'(00)[:-]?(1\w)[:-]?(\w1)[:-]?(\w\w)[:-]?(' \
                        r'\w\w)[:-]?(\w\w)[:-]?'

    for key, value in ip_mac_dir.items():
        formatted = re.match(patt_format, key)
        format_mac = re.match(patt_grouping, key)
        # 如果不是标准格式，转换为标准格式(这里其实可以不用if判断，直接全部转换，但是哪种方法效率更高呢？TODO)
        if not formatted:
            mac = format_mac.group(1).upper() + '-' + format_mac.group(
                2).upper(
            ) + '-' + format_mac.group(3).upper() + '-' + format_mac.group(
                4).upper() + '-' + format_mac.group(
                5).upper() + '-' + format_mac.group(6).upper()
            del ip_mac_dir[key]
            ip_mac_dir[mac] = value

    with open('IPMac.txt') as f:
        counts = 0
        for eachline in f:
            read_mac = re.search(patt_mac, eachline)
            read_ip = re.split(r'\s', eachline.strip())
            if read_mac is not None:
                for mac in ip_mac_dir.keys():
                    if mac == read_mac.group() and ip_mac_dir[mac]:
                        url = ("\"" + "http://" + read_ip[
                            1] + "/AutoTest&" + "\""
                               + "\t#" + ip_mac_dir[mac] + '\t' + mac)
                        url_list.append(url)
                        counts += 1
                    # ip_mac_dir[mac]-->model为空的情况，此时用\t替代model的位置，以保持输出格式
                    elif mac == read_mac.group() and not ip_mac_dir[mac]:
                        url = ("\"" + "http://" + read_ip[
                            1] + "/AutoTest&" + "\""
                               + "\t#" + "\t" + '\t' + mac)
                        url_list.append(url)
                        counts += 1
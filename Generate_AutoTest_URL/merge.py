import re


class UrlGenerator:
    def __init__(self, obj_mac_file, obj_ip_file, tg_file):
        self.obj_mac_file = obj_mac_file
        self.obj_ip_file = obj_ip_file
        self.tg_file = tg_file
        self.ip_mac = {}
        self.url_list = []
        self.patt_mac = r'00[-:]?1\w[-:]?\w1[-:]?\w\w[-:]?\w\w[-:]?\w\w'
        self.patt_judge_type = r'[6,8,9]\d\d\w*'

    def read_mac(self):
        with open(self.obj_mac_file) as f_obj:
            for eachline in f_obj:
                if ('-' in eachline) or (':' in eachline):
                    if len(eachline) <= 17:
                        self.judge_type = None
                    else:
                        self.judge_type = re.search(self.patt_judge_type,
                                                    eachline[-6:-1])
                elif '-' and ':' not in eachline:
                    self.judge_type = re.search(self.patt_judge_type,
                                                eachline[-5:-1])
                self.result = re.search(self.patt_mac, eachline)
                # 将result--mac作为key，因为mac不会重复，而model会重复，以免key重复，将值覆盖
                if (self.judge_type is not None) and (self.result is not None):
                    try:
                        self.mac = self.result.group()
                        self.type = self.judge_type.group()
                        self.ip_mac[self.mac] = self.type
                    except TypeError:
                        pass
                elif (self.judge_type is None) and (self.result is not None):
                    try:
                        self.mac = self.result.group()
                        self.type = ""
                        self.ip_mac[self.mac] = self.type
                    except TypeError:
                        pass
        # print(self.ip_mac) 测试函数是否正确生成mac:model的字典

    def formatting(self):
        self.patt_format = r'^00-1\w-\w1-\w\w-\w\w-\w\w'
        self.patt_grouping = r'(00)[:-]?(1\w)[:-]?(\w1)[:-]?(\w\w)[:-]?(\w\w)[:-]?(\w\w)[:-]?'
        for key, value in self.ip_mac.items():
            self.formatted = re.match(self.patt_format, key)
            self.format_mac = re.match(self.patt_grouping, key)
            # 如果不是标准格式，转换为标准格式(这里其实可以不用if判断，直接全部转换，但是哪种方法效率更高呢？TODO)
            if not self.formatted:
                self.mac = self.format_mac.group(
                    1).upper() + '-' + self.format_mac.group(
                    2).upper() + '-' + self.format_mac.group(
                    3).upper() + '-' + self.format_mac.group(4).upper(
                ) + '-' + self.format_mac.group(5).upper(
                ) + '-' + self.format_mac.group(6).upper()
                del self.ip_mac[key]
                self.ip_mac[self.mac] = value

    def read_ip(self):
        with open(self.obj_ip_file) as f:
            self.counts = 0
            for eachline in f:
                self.get_mac = re.search(self.patt_mac, eachline)
                self.get_ip = re.split(r'\s', eachline.strip())
                if self.get_mac is not None:
                    for key in self.ip_mac.keys():
                        if key == self.get_mac.group() and self.ip_mac[key]:
                            self.url = ("\"" + "http://" + self.get_ip[1] +
                                        "/AutoTest&" + "\"" + "\t#" +
                                        self.ip_mac[key] + '\t' + key)
                            self.url_list.append(self.url)
                            self.counts += 1
                        # ip_mac[mac]-->model为空的情况，此时用\t替代model的位置，以保持输出格式
                        elif key == self.get_mac.group(
                        ) and not self.ip_mac[key]:
                            self.url = ("\"" + "http://" + self.get_ip[1] +
                                        "/AutoTest&" + "\"" + "\t#" + "\t" +
                                        '\t' + key)
                            self.url_list.append(self.url)
                            self.counts += 1

    def generate_url(self):
        self.read_mac()
        self.formatting()
        self.read_ip()

        with open(self.tg_file, 'w') as f:
            for count, url in zip(range(1, self.counts + 1), self.url_list):
                f.write("URL=" + str(count) + url + "\n")

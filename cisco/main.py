#!/usr/bin/python3

import os
import re


def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]
    for i in range(int(mask_int)):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


if __name__ == '__main__':

    with open("./CN-20210601.txt") as f:
        lines = f.readlines()
        for line in lines:
            target = re.split(r'\t', line)[2]
            ip, mask = target.split('/')
            mask = exchange_maskint(mask)

            # print(ip, mask)
            # IP数据来源http://ipblock.chacuo.net/
            os.system("./writeRoute.sh {0} {1}".format(ip, mask))

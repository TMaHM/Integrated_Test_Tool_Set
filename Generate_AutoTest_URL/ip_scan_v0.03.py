import re

import generatefunction as gf

phones_mac = input("please enter your mac recording file")
phones_ip = 'IPMac.txt'

gf.read_mac(phones_mac)
gf.read_ip(phones_ip)
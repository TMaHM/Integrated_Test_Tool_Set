ip_mac = {}

with open('mac_list.txt') as file_object1:
    macs = file_object1.readlines()

for mac in macs:
    ip_mac[mac[-5:-1]] = mac[:17]

# for key, value in ip_mac.items():
#     print(key + ": " + value)
# print(ip_mac)
with open('IPMac.txt') as file_object:
    lines = file_object.readlines()

num_phones = range(1, 20)
ip_phones = []

for line in lines:
    for key, value in ip_mac.items():
        if value in line:
            ip_phones.append(line[4:-19].strip())
            print(key + '-->' + line[4:].rstrip())

with open('ip_phones.txt', 'w') as f_obj:
    for count, ip_phone in zip(num_phones, ip_phones):
        url_list = ("URL" + str(count) + "=\"" + "http://" + ip_phone +
                    "/AutoTest&\"\n")
        f_obj.write(url_list)

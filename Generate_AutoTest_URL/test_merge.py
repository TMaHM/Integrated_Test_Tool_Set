import merge as mrg

mac = input("Enter the mac list recording filename:\t")
mac = mac + '.txt'

ip_mac = input("Are you using IPMac?(Enter 'y' for 'yes', 'n' for 'no'):\t")
if ip_mac.lower() == 'y':
    ip_mac = 'IPMac.txt'
else:
    print("Sorry, we currently only support IPMac.")

out_file = input("Enter the out put filename:\t")
out_file = out_file + '.txt'


generate = mrg.UrlGenerator(mac, ip_mac, out_file)

generate.generate_url()

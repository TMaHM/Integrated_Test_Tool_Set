import tkinter as tk
import merge as mrg

# 定义根窗口
top = tk.Tk()
top.title('AutoTest URL Generator')
top.geometry('800x400')

label = tk.Label(top, text='Phones\' MAC list', bg='red', fg='white')
label.pack()

hit_generate = False
def generate():
    global hit_generate

    if hit_generate == False:
        hit_generate = True

        mac = 'mac_list.txt'
        ip_mac = 'IPMac.txt'
        output = 'phones_url.txt'

        gn = mrg.UrlGenerator(mac, ip_mac, output)
        gn.generate_url()

    else:
        hit_generate = False


button = tk.Button(top, text='Generate', activebackground='blue',
                   command=generate)

button.pack()

# 主循环
top.mainloop()

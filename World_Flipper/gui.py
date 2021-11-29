import tkinter as tk
import world_flipper_canzhan1
import world_flipper_fangzhu

if __name__ == '__main__':
    app = tk.Tk()
    app.title('Auto Player World Flipper')
    join_device_1 = tk.Entry(app)
    join_device_1.pack()
    modify_button = tk.Button(app,text = '修改')
    modify_button.pack()

    info = tk.Label(app,text='使用设备{0}参战'.format(join_device_1))
    info.pack()
    tk.mainloop()
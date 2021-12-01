# import queue
# import threading
# import tkinter as tk
# import time
# import tkinter.ttk as ttk

# class GUI:
#     def __init__(self, master):
#         self.master = master
#         self.test_button = tk.Button(self.master, command=self.tb_click)
#         self.test_button.configure(
#             text="Start", background="Grey",
#             padx=50
#             )
#         self.test_button.pack()

#     def progress(self):
#         self.prog_bar = ttk.Progressbar(
#             self.master, orient="horizontal",
#             length=200, mode="indeterminate"
#             )
#         self.prog_bar.pack()

#     def tb_click(self):
#         self.progress()
#         self.prog_bar.start()
#         self.queue = queue.Queue()
#         ThreadedTask(self.queue).start()
#         # self.master.after(100, self.process_queue)

#     def process_queue(self):
#         try:
#             msg = self.queue.get_nowait()
#             # Show result of the task if needed
#             self.prog_bar.stop()
#         except queue.Empty:
#             self.master.after(100, self.process_queue)

# class ThreadedTask(threading.Thread):
#     def __init__(self, queue):
#         super().__init__()
#         self.queue = queue
#     def run(self):
#         time.sleep(5)  # Simulate long running process
#         self.queue.put("Task finished")

# root = tk.Tk()
# root.title("Test Button")
# main_ui = GUI(root)
# root.mainloop()

import tkinter as tk
from tkinter import Tk
from  tkinter import messagebox


# 当点击右上角退出时，执行的程序
# class Root(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.protocol('WM_DELETE_WINDOW', self.on_closing)

#     def on_closing(self):
#         print("on_closing")
#         if messagebox.askokcancel("Quit", "Do you want to quit?"):
#             self.destroy()
# root = Root()
# # WM_DELETE_WINDOW 不能改变，这是捕获命令
# root.mainloop()

#App.py
import tkinter as tk
# import tkFont as tkfont
import subprocess

from subprocess import Popen
from subprocess import PIPE
from itertools import islice
from threading import Thread
from tkinter.ttk import Scrollbar
from tkinter import *
from queue import Queue, Empty

class App():
    def __init__(self, root):
        self.root = root
        # self.root.title_font = tkfont.Font(family ="Helvetica", size = 18, weight ="bold", slant ="italic")

        Grid.columnconfigure(self.root, 5, weight = 1)

        button_ok = tk.Button(self.root, text ="OK", width = 10, command = lambda: self.on_okay())
        button_ok.grid(row = 7, column = 0, padx = (20,0), pady = 10, sticky = W)

        xscrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        xscrollbar.grid(row=8, column=1, columnspan=4, sticky=E + W)

        yscrollbar = Scrollbar(self.root, orient=VERTICAL)
        yscrollbar.grid(row=8, column=5, sticky=N + S)

        self.textarea = Text(self.root, wrap=NONE, bd=0,
                             xscrollcommand=xscrollbar.set,
                             yscrollcommand=yscrollbar.set)
        self.textarea.grid(row=8, column=1, columnspan=4, rowspan=1,
                            padx=0, sticky=E + W + S + N)

    def on_okay(self):
        self.textarea.delete("1.0", END)

        exec_path = r"\\Test.py" #insert location of Test.py

        self.process = subprocess.Popen([exec_path, 'var_test'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

        self.q = Queue(maxsize = 1024)
        t = Thread(target=self.reader_thread, args=[self.q])
        t.daemon = True
        t.start()

        self.update(self.q)

    def reader_thread(self, q):
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        for line in self.iter_except(q.get_nowait, Empty):
            if line is None:
                #self.quit()
                return
            else:
                self.textarea.insert(INSERT, line)
                self.textarea.yview(END)
                break
        self.root.after(40, self.update, q)

    def iter_except(self, function, exception):
        try:
            while True:
                yield function()
        except exception:
            return

    def read_update(self):
        while True:
            line = self.process.stdout.readline()
            if line =="" and self.process.poll() != None:
                break
            elif line =="":
                pass
            else:
                self.textarea.insert(INSERT, line)
                self.textarea.yview(END)
                self.textarea.update_idletasks()    

    def quit(self):
        try:
            self.process.kill()
        except AttributeError:
            pass
        finally:
            self.root.destroy()
import sys

from time import sleep

var = sys.argv
print(var)

for i in range(1, 10):
    print (i)

print("finished printing numbers")
sleep(10)
print("finished")
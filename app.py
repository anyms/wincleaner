#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 Spidy developers (http://wincleaner.spidy.app)
See the file 'LICENSE' for copying permission
""" 

import os
import shutil
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from wincleaner import WinCleaner


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack()

        self.cleaner = WinCleaner()

    def clean(self):
        # self.status_label["text"] = "hello, world!"
        # self.progress_bar["value"] = 50
        proc = Thread(target=self.__clean)
        proc.start()

    def __clean(self):
        deleted_files = 0
        should_close = False
        if self.cleaner.is_chrome_running():
            should_close = messagebox.askokcancel("Confirm", "Chrome is running, would you like to close?")
            if should_close:
                self.cleaner.close_chrome()

        if not should_close:
            self.cleaner.num_of_files = self.cleaner.num_of_files - len(self.cleaner.caches["chrome"])

        for cache_type, abspath_list in self.cleaner.caches.items():
            if not should_close and cache_type == "chrome":
                continue

            for abspath in abspath_list:
                try:
                    if os.path.isdir(abspath):
                        shutil.rmtree(abspath)
                    else:
                        os.remove(abspath)
                except PermissionError: pass
                deleted_files += 1
                self.progress_bar["value"] = round(deleted_files * float(self.cleaner.num_of_files) / 100.0)

        self.status_label["text"] = "Cleaning completed!"
        self.progress_bar["value"] = 100

    def __analize(self):
        self.status_label["text"] = self.cleaner.analize()   

    def analize(self):
        proc = Thread(target=self.__analize)
        proc.start()

    def pack(self):
        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=X, padx=10, pady=10)
        self.status_label = Label(self.master, text="Click analize to see the cache size", fg="black")
        self.status_label.pack(fill=X, padx=10, pady=10)
        self.clean_button = Button(self.master, text="Clean", command=self.clean)
        self.clean_button.pack(fill=X, padx=10, pady=10)   
        self.analize_button = Button(self.master, text="Analize", command=self.analize)
        self.analize_button.pack(fill=X, padx=10, pady=10)

    def initialize(self):
        pass     

    
if __name__ == "__main__":
    root = Tk()
    root.geometry("400x200")
    app = App(root)
    root.mainloop()

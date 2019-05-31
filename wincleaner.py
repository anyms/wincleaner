#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 Spidy developers (http://wincleaner.spidy.app)
See the file 'LICENSE' for copying permission
""" 

import os
from pathlib import Path
import subprocess
import psutil as psutil


class WinCleaner:
    def __init__(self):
        self.home = str(Path.home())
        self.caches = {
            "tmp": [],
            "chrome": []
        }
        self.num_of_files = 0

    def is_chrome_running(self):
        for proc in psutil.process_iter():
            proc_name = proc.name()
            if proc_name == 'chrome.exe':
                return True
        return False

    def close_chrome(self):
        for proc in psutil.process_iter():
            proc_name = proc.name()
            if proc_name == 'chrome.exe':
                psutil.Process(proc.pid).kill()


    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return round(size, 2), power_labels[n]+'B'

    def clear_recylebin(self):
        subprocess.Popen(["powershell.exe", "-Command", "'Clear-RecycleBin -DriveLetter C -Force'"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def get_tmp_dir(self):
        return os.path.join(self.home, "AppData", "Local", "Temp")

    def get_chrome_cache_dir(self):
        return os.path.join(self.home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache")

    def analize(self):
        cache_size = 0
        for path, dirs, files in os.walk(self.get_chrome_cache_dir()):
            for f in files:
                abspath = os.path.join(path, f)
                cache_size += os.path.getsize(abspath)
                self.caches["chrome"].append(abspath)
                self.num_of_files += 1

        for path, dirs, files in os.walk(self.get_tmp_dir()):
            for f in files:
                abspath = os.path.join(path, f)
                cache_size += os.path.getsize(abspath)
                self.caches["tmp"].append(abspath)
                self.num_of_files += 1
                
        return self.format_bytes(cache_size)

import psutil as psutil

for proc in psutil.process_iter():
    proc_name = proc.name()
    if proc_name == 'chrome.exe':
        print('chrome is running now.')
    else:
        print(proc_name)

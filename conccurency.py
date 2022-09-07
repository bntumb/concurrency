import threading
from threading import Thread
from threading import Lock

from queue import Queue
import time
from collections import deque
import pandas as pd
import urllib.request as ur
import re


_sentinel = object()
df = pd.read_csv('links.csv')

def get_url_list():
    
    url_list = df.values.tolist()
    return url_list

def producer(out_queue):
    while True:
        if not q.full():
            for url in get_url_list():
                try:
                    site = ur.urlopen(url[0].strip('[]'))
                    markup = site.read()
                    out_queue.put(markup)
                except ur.HTTPError as e:
                    pass

            else:
                out_queue.put(_sentinel)
                break
    
def consumer(in_queue, lock):
    index = 0
    while pt.isAlive():
        if not q.empty():
            data = in_queue.get()
            with lock:
                try:
                    urls = re.findall('(?:(?:https?|ftp):\/\/)(?:[-\w.]|(?:%[/da-fA-F]{2}))+', data.decode('utf-8'))
                    index = index+1
                    key_name =  get_url_list()

                    for j in range (len (urls)):
                        print(f'URL: {key_name[index-1][0]} ... hyperlink {urls[j]}',  flush=True)
                        
                except AttributeError:
                    key_name.pop(index-1)
                    pass 
               
                except UnicodeDecodeError:
                    key_name.pop(index-1)
                    print("Found a bad char in file")
                    pass 
                    
            
            in_queue.task_done()
       
    
if __name__ == "__main__":
    lock = Lock()

    time_start = time.time()
    q = Queue()
    pt = Thread(target = producer, args =(q, ))
    ct = Thread(target = consumer , args =(q, lock ))

    pt.start()
    ct.start()
    pt.join()
    ct.join()
    q.join()
    time_end = time.time()

    print("Time elapsed: {}".format(round(time_end - time_start, 2)))
#!/usr/bin/env python
# coding=utf-8


from cmdline import parse_args
from threading import Thread
from Queue import Queue
import json
import requests
import time




# 创建任务
def task_new():
    resp = requests.get(server+'/task/new')
    return resp.json()


# 设置选项
def option_set(taskid, target):
    resp = requests.post(server+'/option/'+taskid+'/set', data=json.dumps({'url': target}), headers=headers)
    return resp.json()


# 开始扫描
def scan_start(taskid, target):
    resp = requests.post(server+'/scan/'+taskid+'/start', data=json.dumps({'url': target}), headers=headers)
    return resp.json()


# 判断扫描是否结束
def scan_status(taskid):
    resp = requests.get(server+'/scan/'+taskid+'/status')
    return resp.json()


# 查看扫描结果
def scan_data(taskid):
    resp = requests.get(server+'/scan/'+taskid+'/data')
    return resp.json()


# 暂停任务
def scan_stop(taskid):
    resp = requests.get(server+'/scan/'+taskid+'/stop')
    return resp.json()


# 结束任务进程
def scan_kill(taskid):
    resp = requests.get(server+'/scan/'+taskid+'/kill')
    return resp.json()


# 删除任务
def task_delete(taskid):
    resp = requests.get(server+'/task/'+taskid+'/delete')
    return resp.json()


# 创建一个队列用于存放待检测url
def scan_queue(target):
    with open(target, 'r') as f:
        content = f.readlines()
        for each in content:
            url_queue.put(each)


# 创建多线程
class ScanThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        while True:
            if url_queue.empty(): break
            url_now = url_queue.get()
            print url_now
            resp_json = task_new()
            task_id = resp_json['taskid']
            if resp_json['success']:
                print 'Set options...'
                option_json = option_set(task_id, url_now)
                if option_json['success']:
                    print 'Options are setted, start scan...'
                    start_json = scan_start(task_id, url_now)
                    # print start_json
                    start_time = time.time()
                    # print start_time
                    print 'Scanning...'
                    if start_json['success']:
                        while True:
                            status_json = scan_status(task_id)
                            # print status_json
                            if status_json['status'] != 'terminated':
                                time.sleep(10)
                            else:
                                # print status_json
                                print 'Scan is finished.'
                                # print task_id
                                data_json = scan_data(task_id)
                                # print data_json
                                if data_json['data'] == []:
                                    print 'There is no SQL Injection.'
                                else:
                                    print 'Data is ...'
                                    print data_json['data']
                                    sql_list.append(url_now)
                                task_delete(task_id)
                                print 'Delete task.'
                                break
                            # print time.time()
                            if time.time() - start_time > 3000:
                                print 'No response.'
                                scan_stop(task_id)
                                scan_kill(task_id)
                                task_delete(task_id)
                                break
                    else:
                        print 'Task Error.'
            url_queue.task_done()
            # print url_queue.empty()



def main(num_t):

    threads = []
    for x in xrange(num_t):
        threads.append(ScanThread())
        threads[x].start()

    for y in threads:
        y.join()


if __name__ == '__main__':

    server = 'http://127.0.0.1:8775'
    headers = {'Content-Type': 'application/json'}
    sql_list = []
    arg = parse_args()
    url_path = arg.u
    num_thread = arg.t
    url_queue = Queue()
    scan_queue(url_path)
    main(num_thread)
    print "\n------------------SQL Injections-------------------"
    print sql_list
    print "\n--------------------It's done.---------------------"

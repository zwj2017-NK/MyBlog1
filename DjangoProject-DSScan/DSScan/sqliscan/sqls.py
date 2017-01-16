# -*- coding: utf-8 -*-

import json
import requests
import time
from threading import Thread
from .models import SqlInjection

server = 'http://127.0.0.1:8775'
headers = {'Content-Type': 'application/json'}


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


# 查看扫描日志
def scan_log(taskid):
    resp = requests.get(server+'/scan/'+taskid+'/log')
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


# 创建多线程
class ScanThread(Thread):

    def __init__(self, url_queue):
        Thread.__init__(self)
        self.url_queue = url_queue

    def run(self):
        while True:
            if self.url_queue.empty(): break
            url_now = self.url_queue.get()
            print url_now
            task = SqlInjection.objects.get(target_url=url_now)
            resp_json = task_new()
            task_id = resp_json['taskid']
            task.task_id = task_id
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
                            task.scan_status = status_json['status']
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
                                    task.vulnerability = False
                                else:
                                    print 'Data is ...'
                                    print data_json['data']
                                    task.vulnerability = True
                                task.scan_data = data_json['data']
                                task.scan_log = scan_log(task_id)['log']
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
            self.url_queue.task_done()
            task.save()
            # print url_queue.empty()


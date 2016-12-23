#!/usr/bin/env python
# coding=utf-8


from cmdline import parse_args
import json
import requests
import time


server = 'http://127.0.0.1:8775'
headers = {'Content-Type': 'application/json'}
arg = parse_args()


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
    resp = requests.get(server+'/scan'+taskid+'/kill')
    return resp.json()


# 删除任务
def task_delete(taskid):
    resp = requests.get(server+'/task/'+taskid+'/delete')
    return resp.json()


def main(target):
    with open(target, 'r') as f:
        content = f.readlines()
        for each in content:
            # print each
            resp_json = task_new()
            # print resp_json
            task_id = resp_json['taskid']
            if resp_json['success']:
                print 'Set options...'
                option_json = option_set(task_id, each)
                if option_json['success']:
                    print 'Options are setted, start scan...'
                    start_json = scan_start(task_id, each)
                    start_time = time.time()
                    print 'Scanning...'
                    if start_json['success']:
                        while 1:
                            status_json = scan_status(task_id)
                            if status_json['status'] != 'terminated':
                                time.sleep(10)
                            else:
                                print 'Scan is finished.'
                                data_json = scan_data(task_id)
                                if data_json['data'] == []:
                                    print 'There is no SQL Injection.'
                                else:
                                    print 'Data is ...'
                                    print data_json['data']
                                task_delete(task_id)
                                print 'Delete task.'
                                break
                            if time.time() - start_time > 3000:
                                print 'No response.'
                                scan_stop(task_id)
                                scan_kill(task_id)
                                task_delete(task_id)
                                break
            else:
                print 'Task Error.'


if __name__ == '__main__':
    arg = parse_args()
    url_path = arg.u
    main(url_path)
    print "\n--------------------It's done.---------------------"

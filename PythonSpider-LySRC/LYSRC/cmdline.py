#!/usr/bin/env python
# coding=utf-8

import argparse
import sys

def parse_args():
    # 创建一个命令行参数对象
    parser = argparse.ArgumentParser(prog='LySrcPV', usage="LySrc.py [options]",
                                     description="* LySRC Public Vulnerabilities *",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', metavar='VulPages', type=int, default=6, help='Total pages')
    parser.add_argument('-s', metavar='VulSpeed', type=int, default=6, help='Speed of pages')
    parser.add_argument('-t', metavar='ThreadNum', type=int, default=10, help='Num of threads')

    # 什么都没输入情况，就输入一个脚本名，sys.argv 就只有一个参数
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    # 返回一个保存命令行参数的命名空间
    args = parser.parse_args()
    return args
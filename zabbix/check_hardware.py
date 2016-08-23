#!/usr/bin/python
#coding:utf-8
import os,sys
import json
from subprocess import Popen,PIPE

values = []

def help():
    print 'Usage: '
    print 'python %s <disc|data> <cpus|fans> [id]' %sys.argv[0]

# 风扇ID发现
def fans_disc():
    global values
    fans_id = os.popen("""/usr/bin/omreport chassis fans | awk '/^Index/{print $NF}'""")
    for id in fans_id:
        r1 = os.path.basename(id.strip())
        values += [{'{#FAN_ID}':r1}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))        
        
#CPU ID发现
def cpus_disc():
    global values
    cpus_id = os.popen("""/usr/bin/omreport chassis temps | awk '/^Index/{print $NF}'""")
    for value in cpus_id.readlines():
        r2 = os.path.basename(value.strip())
        values += [{'{#CPU_ID}':r2}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))        

def fans_data(id):
    id = int(sys.argv[3])
    os.environ['id'] = str(id)
    (stdout,stderr) = Popen("/usr/bin/omreport chassis fans | awk '/Reading/{print $(NF-1)}'", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    rpm = r[id]
    print rpm

def cpus_data(id):
    id = int(sys.argv[3])
    os.environ['id'] = str(id)
    (stdout,stderr) = Popen("/usr/bin/omreport chassis temps | awk '/Reading/{print $(NF-1)}'", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    t = stdout.strip().split()
    # 根据id 输出需要的数值
    temps = t[id]
    print temps

if sys.argv[1] == "disc":
    if sys.argv[2] == "fans":
        fans_disc()
    elif sys.argv[2] == "cpus":
        cpus_disc()

elif sys.argv[1] == "data":
    if sys.argv[2] == "fans":
        fans_data(sys.argv[3])
    elif sys.argv[2] == "cpus":
        cpus_data(sys.argv[3])

else:
    help()

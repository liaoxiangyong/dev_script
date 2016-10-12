#!/usr/bin/python
#coding:utf-8
import os,sys
import json
from subprocess import Popen,PIPE

values = []

def help():
    print 'Usage: '
    print 'python %s <disc|data> <cpus|fans|pdisks|vdisks|mems|powers> [id1] [id2]' %sys.argv[0]

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
    (stdout,stderr) = Popen("/usr/bin/omreport chassis fans | awk '/^Reading/{print $(NF-1)}'", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    rpm = r[id]
    print rpm

def cpus_data(id):
    id = int(sys.argv[3])
    os.environ['id'] = str(id)
    (stdout,stderr) = Popen("/usr/bin/omreport chassis temps | awk '/^Reading/{print $(NF-1)}'", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    t = stdout.strip().split()
    # 根据id 输出需要的数值
    temps = t[id]
    print temps

# 获取阵列卡（控制器）信息，返回json
def controllers_disc():
    global values
    controllers_id = os.popen("""/usr/bin/omreport storage controller | awk '/^ID/{print $NF}'""")
    for value in controllers_id.readlines():
        c = os.path.basename(value.strip())
        values += [{'{#CONT_ID}':c}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def pdisks_disc():
    global values
    # 获取controller id
    (stdout,stderr) = Popen("/usr/bin/omreport storage controller | awk '/^ID/{print $NF}'",shell=True, stdout=PIPE, stderr=PIPE).communicate()
    c = stdout.strip().split()
    for c2 in c:
        os.environ['c2']=str(c2)
        pdisks_id = os.popen("""/usr/bin/omreport storage pdisk controller=$c2 | awk -F: '/^ID/{print $NF}'""")
        num = 0
        for value in pdisks_id.readlines():
            #p = os.path.basename(value.strip())
            p = str(num)
            values += [{'{#PDISK_ID}':p}]
            num+=1
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def vdisks_disc():
    global values
    vdisks_id = os.popen("""/usr/bin/omreport storage vdisk | awk '/^ID/{print $NF}'""")
    for value in vdisks_id.readlines():
        v = os.path.basename(value.strip())
        values += [{'{#VDISK_ID}':v}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def mems_disc():
    global values
    mems_id = os.popen("""/usr/bin/omreport chassis memory | awk '/^Index/{if($NF~/[0-9]/)print $NF}'""")
    for value in mems_id.readlines():
        m = os.path.basename(value.strip())
        values += [{'{#MEM_ID}':m}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def powers_disc():
    global values
    powers_id = os.popen("""/usr/bin/omreport chassis pwrsupplies | awk '/^Index/{print $NF}'""")
    for value in powers_id.readlines():
        m = os.path.basename(value.strip())
        values += [{'{#POWER_ID}':m}]
    print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def pdisks_data(pid):
    pid = int(sys.argv[3])
    os.environ['pid'] = str(pid)
    # 判断物理硬盘状态是否“Ok”，并输出1 或 0
    #(stdout,stderr) = Popen("""/usr/bin/omreport storage pdisk controller=0 | awk '/^Status/{if($NF=="Ok"){print 1}else{print 0}}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 判断物理硬盘状态是否“Ok”，并输出状态
    (stdout,stderr) = Popen("""/usr/bin/omreport storage pdisk controller=0 | awk '/^Status/{print $NF}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    pdisk_status = r[pid]
    print pdisk_status

def vdisks_data(vid):
    vid = int(sys.argv[3])
    os.environ['vid'] = str(vid)
    # 判断虚拟磁盘状态是否“Ok”，并输出1 或 0
    #(stdout,stderr) = Popen("""/usr/bin/omreport storage vdisk | awk '/^Status/{if($NF=="Ok"){print 1}else{print 0}}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 判断虚拟磁盘状态是否“Ok”, 并输出状态
    (stdout,stderr) = Popen("""/usr/bin/omreport storage vdisk | awk '/^Status/{print $NF}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    vdisk_status = r[vid]
    print vdisk_status

def mems_data(mid):
    mid = int(sys.argv[3])
    os.environ['mid'] = str(mid)
    # 判断内存状态是否“Ok”，并输出1 或 0
    #(stdout,stderr) = Popen("""/usr/bin/omreport chassis memory | awk '{a[NR]=$0;if(a[NR-1]~/^Index.*[0-9]/) {print $NF}}' | awk '{if($NF=="Ok"){print 1}else{print 0}}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 判断内存状态是否“Ok”，并输出状态
    (stdout,stderr) = Popen("""/usr/bin/omreport chassis memory | awk '{a[NR]=$0;if(a[NR-1]~/^Index.*[0-9]/) {print $NF}}' | awk '{print $NF}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    mem_status = r[mid]
    print mem_status

def pwrsupplies_data(pid):
    pid = int(sys.argv[3])
    os.environ['pid'] = str(pid)
    # 判断电源状态是否“Ok”，并输出1 或 0
    #(stdout,stderr) = Popen("""/usr/bin/omreport chassis pwrsupplies | awk '/^Status/{if($NF=="Ok"){print 1}else{print 0}}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 判断电源状态是否“Ok”，并输出状态
    (stdout,stderr) = Popen("""/usr/bin/omreport chassis pwrsupplies | awk '/^Status/{print $NF}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip().split()
    # 根据id 输出需要的数值
    power_status = r[pid]
    print power_status

def pwrmonitor_data():
    # 获取电源功耗
    (stdout,stderr) = Popen("""/usr/bin/omreport chassis pwrmonitoring | awk '{a[NR]=$0;if(a[NR-4]=="Power Consumption")print $(NF-1)}'""", shell=True, stdout=PIPE, stderr=PIPE).communicate()
    # 生成list
    r = stdout.strip()
    # 根据id 输出需要的数值
    print r


if sys.argv[1] == "disc":
    if sys.argv[2] == "fans":
        fans_disc()
    elif sys.argv[2] == "cpus":
        cpus_disc()
    elif sys.argv[2] == "controllers":
        controllers_disc()
    elif sys.argv[2] == "pdisks":
        pdisks_disc()
    elif sys.argv[2] == "vdisks":
        vdisks_disc()
    elif sys.argv[2] == "mems":
        mems_disc()
    elif sys.argv[2] == "powers":
        powers_disc()

elif sys.argv[1] == "data":
    if sys.argv[2] == "fans":
        fans_data(sys.argv[3])
    elif sys.argv[2] == "cpus":
        cpus_data(sys.argv[3])
    elif sys.argv[2] == "pdisks":
        pdisks_data(sys.argv[3])
    elif sys.argv[2] == "vdisks":
        vdisks_data(sys.argv[3])
    elif sys.argv[2] == "mems":
        mems_data(sys.argv[3])
    elif sys.argv[2] == "pwrsupplies":
        pwrsupplies_data(sys.argv[3])
    elif sys.argv[2] == "pwrmonitor":
        pwrmonitor_data()

else:
    help()

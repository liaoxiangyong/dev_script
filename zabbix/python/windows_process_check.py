import sys
import os
import json
import re

#################
# create by Cumin
# 20161014
# used for zabbix to get windows process's handlecounts and threadcounts
#################

values = []

def help():
	print 'Usage: '
   # print 'python %s <disc|data> full_process_name' %sys.argv[0]
   # print 'Such as : python %s <disc|data> chrome.exe' %sys.argv[0]

# get ProcessName's ProcessId List with Json format
def disc(ProcessName):
	global values
	ProcessName = sys.argv[2]
	cmd = 'wmic process where name="' + ProcessName + '" get processid'
	ProcessIdList = os.popen(cmd)
	for ProcessId in ProcessIdList:
		p = os.path.basename(ProcessId.strip())
		if re.match(r'^\d+',p):
		    values += [{'{#P_ID}':p}]
	print json.dumps({'data':values},sort_keys=True,indent=4,separators=(',',':'))

def HandleCountdata(ProcessId):
	global values
	ProcessId = str(sys.argv[2])
	cmd = 'wmic process where processid="' + ProcessId + '" get handlecount'
	HandleCount_data = os.popen(cmd)
	for HandleCount in HandleCount_data:
		HC = os.path.basename(HandleCount.strip())
		if re.match(r'^\d+',HC):
			print HC

def ThreadCount(ProcessId):
	global values
	ProcessId = str(sys.argv[2])
	cmd = 'wmic process where processid="' + ProcessId + '" get threadcount'
	TheadCount_data = os.popen(cmd)
	for ThreadCount in TheadCount_data:
		TC = os.path.basename(ThreadCount.strip())
		if re.match(r'^\d+',TC):
			print TC


if sys.argv[1] == "disc":
	disc(sys.argv[2])
elif sys.argv[1] == "handlecount":
	HandleCountdata(sys.argv[2])
elif sys.argv[1] == "threadcount":
    ThreadCount(sys.argv[2])
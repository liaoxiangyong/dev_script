#!/usr/bin/python

import os
import sys
import subprocess
import docker

def check_container_info(container_name,container_item):
    null = ''
    get_container_info = docker_client.stats(container_name)
    old_result = eval(get_container_info.next())
    new_result = eval(get_container_info.next())
    get_container_info.close()
    
    if container_item == "cpu_total_usage":
        result = new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage']['total_usage']
    elif container_item == "system_cpu_usage":
        result = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
    elif container_item == "cpu_percent":
        total_cpu_usage = new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage']['total_usage']
        sys_cpu_usage = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
        cpu_num = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        result = round(float(total_cpu_usage)/float(sys_cpu_usage)*cpu_num*100.0,2)
    elif container_item == "mem_usage":
        result = new_result['memory_stats']['usage'] 
    elif container_item == "mem_limit":
        result = new_result['memory_stats']['limit']
    elif container_item == "total_cache":
        result = new_result['memory_stats']['stats']['total_cache']
    elif container_item == "total_swap":
        result = new_result['memory_stats']['stats']['total_swap']
    elif container_item == "mem_percent":
        mem_usage = new_result['memory_stats']['usage'] 
        mem_limit = new_result['memory_stats']['limit'] 
        result = round(float(mem_usage)/float(mem_limit)*100.0,2)
    elif container_item == "eth0_rx_byte":
        result = new_result['networks']['eth0']['rx_bytes'] - old_result['networks']['eth0']['rx_bytes']
    elif container_item == "eth0_tx_byte":
        result = new_result['networks']['eth0']['tx_bytes'] - old_result['networks']['eth0']['tx_bytes']
    return result

if __name__ == "__main__":
    docker_client = docker.Client(base_url='unix://var/run/docker.sock',version='1.23')
    container_name = sys.argv[1]
    container_item = sys.argv[2]
    global result
    print check_container_info(container_name,container_item)

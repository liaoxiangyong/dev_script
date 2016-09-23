#!/bin/bash
# docker_name = process_name
# check process_name is running
if [ $# -gt 2 ];then
    echo "Usage: $0 container_name[uptime]"
fi

function check_proc(){
    sudo /bin/docker exec $1 ps aux | grep -v "ps aux" | grep $1  > /dev/null 2>&1
    if [ $? -ne 0 ];then
        echo "0"
    else 
        echo "1"
    fi
}

function run_time(){
    uptime=$(sudo /bin/docker exec $1 cat /proc/uptime | awk '{print $1}')
    echo "${uptime}"
}

function contain_uptime(){
    docker_run_list=$(sudo /bin/docker ps | grep -v "CONTAINER ID" | awk -F"Up" '{print $2}' | awk '{print $1,$2,$NF}')
    
    container_runtime=$(echo "${docker_run_list}" | grep $1 | awk '{print $1,$2}')
    
    up_date=$(date "+%F %H:%M:%S" -d "-${container_runtime}")
    
    now_date=$(date "+%F %H:%M:%S")
  
    up_date_sec=$(date +%s -d "${up_date}")
    now_date_sec=$(date +%s -d "${now_date}")
    let uptime_sec=${now_date_sec}-${up_date_sec}
    echo ${uptime_sec}
}

if [ $# -eq 1 ];then
    check_proc $1
elif [ $# -eq 2 ] && [ $2 == "uptime" ];then
    contain_uptime $1 $2
    #run_time $1 $2
else 
    echo "0"
fi

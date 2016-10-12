#!/bin/bash
#######################################
# 用于zabbix 语音报警
# 关于语音接口的费用：
# 可以在后台查看每个appId# 的费用。
# PS:该接口对英文支持不是十分友好，尽量使用中文
#######################################
# 业务必选参数
# type（模板编号，当前只有1）
# name1（告警等级）
# name2（触发器名称）
# name3（IP地址）
# name4（检测值）

appId="123"
token="345"

timestamp=$(date +%s)
md5=$(echo -n "${appId}${token}${timestamp}" | md5sum| awk '{print $1}')

curl="https://api.vlink.cn/interface/open/v1/webcall"

# 这个function没意义，只用来记录电话号码与人的关系
function tel_num_list(){
    relationship = "
        '12345678901': '甲'
    "
}

function tel_alert(){
    tel_list="$1"
    alert_level="$2"
    alert_time="now"
    alert_message=$3
    ip_addr=$(echo ${alert_message} | awk -F: '{print $1}')
    ip_addr_cn=$(echo ${ip_addr} | sed 's/\./点/g')
    alert_value=$(echo ${alert_message} | awk -F: '{print $2}')
    DATE=$(date "+%F %T")
    for tel_num in `echo "${tel_list}"| awk 'BEGIN{RS=","}{print $0}'`;do
        result=$(/usr/bin/curl -X POST -s -d tel=${tel_num} -d appId=${appId} -d sign=${md5} -d timestamp=${timestamp} -d type=1 -d name1="${alert_level}" -d name2="${alert_time}" -d name3="${ip_addr_cn}" -d name4="${alert_value}" "${curl}" )
        #result=$(/usr/bin/curl -X POST -s -d tel=${tel_num} -d appId=${appId} -d sign=${md5} -d timestamp=${timestamp} -d type=1 --data-urlencode name1="${alert_level}" --data-urlencode name2="${alert_time}" --data-urlencode name3="${ip_addr_cn}" --data-urlencode name4="${alert_value}" "${curl}" )
        result_code=$(echo "${result}"|jq '.result')
        result_description=$(echo "${result}"|jq '.description')
        echo "${DATE} phone call for ${tel_num} result_code:${result_code} result_description:${result_description}" >> /tmp/tel_alert.log
        echo "command is /usr/bin/curl -X POST -s -d tel=${tel_num} -d appId=${appId} -d sign=${md5} -d timestamp=${timestamp} -d type=1 -d name1="${alert_level}" -d name2="${alert_time}" -d name3="${ip_addr_cn}" -d name4="${alert_value}" "${curl}" " >> /tmp/tel_alert.log
    done
}

if [ $# == 3 ];then
    tel_alert $1 $2 "$3"
else
    echo "${DATE} phone call Error parameters" >>  /tmp/tel_alert.log
fi

#!/usr/bin/env bash
#################
#a=1
#b=2
#c=$((a+b))
#d=$(($a+$b))
#e=$(($a+$b))

##################

##################
#while ((1==1))
#do
#	curl https://localhost:4757
#	if (($? != 0))
#	then
#		date >> curl.log
#	break
#	fi
#done
#####################

# 1 вариант
#array_ip=("192.168.0.1" "173.194.222.113" "87.250.250.242")
#for i in ${array_ip[@]}
#do
#   ping=$(ping $i -c 5)
#   echo $ping >> curl.log
#done

#1 Вариант
#for n in {1..5}; do {
#host=("192.168.0.1" "173.194.222.113" "87.250.250.242")
#for i in ${host[@]}; do
#  nc=$(nc -z $i 80)
#  echo $nc >> curl.log
#done
#  }
#done

# Вариант 2
#hosts=("192.168.0.1" "173.194.222.113" "87.250.250.242")
#for host in ${hosts[@]}; do
#          result=$(ping -c 5 -W  1 -q  $host | grep transmitted)
#          pattern="0 received";
#          if [[ $result =~ $pattern ]]; then
#                echo "$host is down" >> result_chk-PING.log
#          else
#                echo "$host is up" >> result_chk-PING.log
#          fi
#done

# Вариант 3
#for n in {1..5}; do {
#hosts=("192.168.0.1" "173.194.222.113" "87.250.250.242")
#port=("80")
#for host in ${hosts[@]}; do
#          nc -z $host $port
#          if (($?==0)); then
#                echo "`date` ->    $host:$port is available" >> result_chk-NC.log
#          else
#                echo "`date` ->    $host:$port is Not_available" >> result_chk-NC.log
#          fi
#done
#                  }
#done

#################

# Вариант 1
#array_ip=("173.194.222.113" "192.168.0.1" "87.250.250.242")
#for i in ${array_ip[@]}; do
#  ping $i -c 5
#  if (($?==0)); then
#    echo "$i Good available" >> error.log
#  else
#    echo "$i not available" >> error.log
#  break
#  fi
#done

# Вариант 2
#while ((1==1))
#do {
#hosts=("192.168.0.1" "173.194.222.113" "87.250.250.242")
#port=("80")
#for host in ${hosts[@]}; do
#          nc -z $host $port
#          if (($?==0)); then
#                echo "`date` ->    $host:$port is available" > ok.log
#          else
#                echo "`date` ->    $host:$port is Not_available" > error.log
#          break
#          fi
#sleep 30s
#done
#}
#done




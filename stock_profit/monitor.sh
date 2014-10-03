#!/bin/bash
##############################################
# Author peng
##############################################
NAME=monitor
BASEDIR='/www'
PROG='shuijing_monitor.py'
MPID=''
LOGFILE=$NAME.log
PIDFILE=$NAME.pid
##############################################
#PHP=""
#监控进程 python -u shuijing_monitor.py
#如果退出就重新运行
#ps -ef | grep "python -u shuijing_monitor.py" | grep -v "grep" | awk '{print $2,$3}'
#子进程ID，父进程ID
##############################################
source /home/ubuntu/djenv/bin/activate

function run(){
    while true;
    do
        count=`ps -fe | grep "shuijing_monitor.py" | grep -v "grep"`
        if [ "$?" != "0" ]; then            
            python -u shuijing_monitor.py >> shuijing.log &
            MPID=`ps -ef | grep "python -u shuijing_monitor.py" | grep -v "grep" | awk '{print $2,$3}'`
            echo $MPID > $PIDFILE
        fi
        sleep 60
    done
        
}
function start(){
    if [ -f "$PIDFILE" ]; then
        echo $PIDFILE
        exit 2
    fi
 
    for (( ; ; ))
    do
        run
    done &
}
function stop(){
    [ -f $PIDFILE ] && kill `cat $PIDFILE` && rm -rf $PIDFILE
}
function status(){
    ps ax | grep $PROG | grep -v grep | grep -v status
}
function reset(){
    pkill $PROG
    [ -f $PIDFILE ] && rm -rf $PIDFILE
}
case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  restart)
    stop
    start
    ;;
  reset)
    reset
    ;;
  *)
    echo $"Usage: $0 {start|stop|status|restart|reset}"
    exit 2
esac
 
exit $?
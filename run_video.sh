#!/usr/bin/env bash
# 部署指定tag 的api程序
# __author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
# __copyright__ = "Copyright of GoChinaTV (2017)."


deploy_tag(){
    echo '******************************'
    echo '********开始部署api：'
    echo '******************************'
#    kill -9 `ps aux | grep gunicorn | awk '{print $2}'`
    source env.sh
    gunicorn -w 2  -b 0.0.0.0:8002 run_video:app
    echo '******************************'
    echo '********部署成功'
    echo '******************************'
}

main(){
    deploy_tag
}

main
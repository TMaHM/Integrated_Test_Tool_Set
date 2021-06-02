#!/bin/bash
dir=`pwd`

cat $dir/iplist | while read line
do
    ip=`echo $line | awk '{print $1}'`
    mask=`echo $line | awk '{print $2}'`

    $dir/writeRoute.sh $ip $mask &
done

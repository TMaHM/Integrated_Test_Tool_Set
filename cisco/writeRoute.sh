#!/usr/bin/expect

set IP [lindex $argv 0]
set MASK [lindex $argv 1]
#IP=$1
#MASK=$2

set address 10.1.0.1
set timeout 5

spawn telnet $address

expect "*Password:"
send "Htek2020\r"
expect "*>"
send "en\r"
expect "*Password:"
send "admin\r"
expect "*#"
send "conf t\r"
expect "*(config)#" {send "ip route $IP $MASK 192.168.0.2\r"}

expect "*#"
send "end\r"
sleep 1
expect "*#"
sleep 1
send "quit\r"
expect eof

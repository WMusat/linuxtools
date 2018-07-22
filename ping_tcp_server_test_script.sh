#!/bin/bash
#simple script to test the ping tcp server tools
#pass in the port number then the regex (in the order)
#EX. ./ping_tcp_server_test_script.sh <port number> <some text>
#EX. ./ping_tcp_server_test_script.sh 2010 textHere
#This script will run the test with everything correct according to the ping_tcp_server script
#then it will try to test it with the wrong expression (the text will be incorrect) - but the inro of "PING:" will be correct
#finally it will try to hit the tcp server with everything incorrect - you shuold get 3 different responses
#response 1: PONG: FOUND
#response 2: PONG: not found
#response 3: unknown error - possibly missing PING: at the beginning

clear
echo ""

echo "=====EVERYTHING CORRECT===="
printf 'PING: '$2'\n'|  nc localhost $1
echo ""
echo ""
echo ""




echo "=====WRONG REGEX===="
printf 'PING: WRONG TEXT'|  nc localhost $1 
echo ""
echo ""
echo ""




echo "=====EVERYTHING WRONG===="
printf 'WRONG EVERYTHING'|  nc localhost $1
echo ""
echo ""
echo ""


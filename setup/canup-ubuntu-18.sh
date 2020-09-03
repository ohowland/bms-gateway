#!/bin/bash

ip link set can0 down
ip link set dev can0 type can bitrate 500000 restart-ms 1000
ip link set can0 up

ip link set can1 down
ip link set dev can1 type can bitrate 500000 restart-ms 1000
ip link set can1 up

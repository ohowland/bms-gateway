#!/bin/bash

CAN_INTERFACE="/etc/network/interfaces"
BAUDRATE=500000

echo -e "auto can0\niface can0 inet manual\n  pre-up /sbin/ip link set \$IFACE type can bitrate $BAUDRATE\n  up /sbin/ifconfig \$IFACE up\n  down /sbin/ifconfig \$IFACE down\n" >> $CAN_INTERFACE 

echo -e "auto can1\niface can1 inet manual\n  pre-up /sbin/ip link set \$IFACE type can bitrate $BAUDRATE\n  up /sbin/ifconfig \$IFACE up\n  down /sbin/ifconfig \$IFACE down" >> $CAN_INTERFACE

/etc/init.d/network-manager restart

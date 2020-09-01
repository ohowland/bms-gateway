#!/bin/bash

CAN0_FILE="/etc/systemd/network/20-can0.network"
CAN1_FILE="/etc/systemd/network/20-can1.network"

BAUDRATE=500000

echo -e "
[Match]
Name=can0

[CAN]
BitRate=$BAUDRATE
SamplePoint=75%
RestartSec=30
Termination=no
ListenOnly=no
" >> $CAN0_FILE

echo -e "
[Match]
Name=can1

[CAN]
BitRate=$BAUDRATE
SamplePoint=75%
RestartSec=30
Termination=no
ListenOnly=no
" >> $CAN1_FILE

systemctl restart systemd-networkd

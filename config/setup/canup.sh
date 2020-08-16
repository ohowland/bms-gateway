
echo "auto can0\niface can0 inet manual\n  pre-up /sbin/ip link set $IFACE type can bitrate 500000\n up /sbin/ifconfig $IFACE up\n down /sbinifconfig $IFACE down" > ~/tmp.txt
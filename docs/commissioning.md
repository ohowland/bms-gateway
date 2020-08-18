# Setup of Gateway Hardware
## Install the Peak Linux Drivers (download latest from website)

`https://www.peak-system.com/fileadmin/media/linux/index.htm`

```
make
make -C driver NET=NETDEV_SUPPORT
sudo make install
sudo modprobe pcan
ifconfig -ai
```  

`grep PEAK_ /boot/config-'uname -r'`   

## Auto-up CAN interfaces
The script `setup/canup.sh` will configure the `/etc/network/interface` with the following:
``` 
auto can0  
iface can0 inet manual  
  pre-up /sbin/ip link set $IFACE type can bitrate 500000
  up /sbin/ifconfig $iface up  
  down /sbin/ifconfig $iface up

auto can1  
iface can1 inet manual  
  pre-up /sbin/ip link set $IFACE type can bitrate 500000
  up /sbin/ifconfig $iface up  
  down /sbin/ifconfig $iface up
```
the network service must be reset after installation:

`sudo /etc/init.d/networking restart`  
OR  
`sudo systemctl restart networking`

# Setup test environment

will need PCANusb and linux host.

`sudo apt-get install python3-dev, pip3, virtualenv, git, vim`

`pip install cantools`

Connect PCANusb to linux test pc check the link:  
`ip link dev set can0 type can bitrate 500000`  
`ip link set can0 up`

# CANbus verification

Connect CANbus cabling from can0 to target device. in the terminal use:  

`candump can0`  

to confirm raw frames are being set on the canbus.

Another option is to use pcanview, which may expedite the process.

## Verify DBC file

unsure if Nuvation BMS is litten endian or big endian. They're also not very clear on the size and scaling of the registers. using cantools:  

`candump can0 | cantools decode config/*.dbc`   
OR
`cantools monitor config/*.dbc`  

and matching against values read from nuvation BMS.

Do this for both the SMA and Nuvation fix errors where found 

# Install the Gateway

`virtualenv -p python3 venv`
`source venv/bin/activate`

`pip install -r requirements.txt`

## Run integration test suite

`nosetests --nocapture -l debug -v`

## Run Gateway

python gateway 

## Commissioning of embedded unit

other than making sure the CAN interfaces are brought up at boot. there are a few other tasks the OS should take care of.

# auto start the script
using systemd:
https://github.com/torfsen/python-systemd-tutorial 

# push error.log to github
chronjob and commit script

# limit size of error.log

use RotatingFileHandler:
https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python

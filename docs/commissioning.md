# Install the Peak Linux Drivers (download latest from website)

`make`   
`make -C driver NET=NETDEV_SUPPORT`  
`sudo make install`  
`sudo modprobe pcan`  
`ifconfig -ai`  

`grep PEAK_ /boot/config-'uname -r'`   

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

## Run integration test suite

## Run Gateway

python3 can

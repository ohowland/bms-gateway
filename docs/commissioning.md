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
./python gateway  

# OS Scripts/Services/Routines 

other than making sure the CAN interfaces are brought up at boot. there are a few other tasks the OS should take care of.

## auto start the script
this is done using systemd:

use the unit file `/setup/gateway.service`  
this file can be placed any number of locations, one that works is: `~/.config/systemd/user/`  
reload the systemd daemon to pickup the new service `systemctl --user daemon-reload`  
start the service with `systemctl --user start gateway.service`  
check status with `systemctl --user status gateway.service`  
follow status with `journalctl --user-unit gateway.service -f`  

## enable ssh server
`sudo apt-get install openssh-server`  
Allow traffic through the firewall:
`sudo ufw allow ssh`

# Configuration of the Nuvation BMS:
## Update BMS CAN Configuration Registers
```
sc_canbus_map[0].address @sc_clock.seconds
sc_canbus_map[1].address @stack_power.voltage
sc_canbus_map[2].address @stack_power.current
sc_canbus_map[3].address @stack_soc.soc
sc_canbus_map[4].address @stack_soc.dod
sc_canbus_map[5].address @stack_cell_stat.max
sc_canbus_map[6].address @stack_cell_stat.min
sc_canbus_map[7].address @stack_cell_stat.avg
sc_canbus_map[8].address @stack_therm_stat.max
sc_canbus_map[9].address @stack_therm_stat.min
sc_canbus_map[10].address @stack_therm_stat.avg
sc_canbus_map[11].address @stack_safety.safe
sc_canbus_map[12].address @stack_safety.safetocharge
sc_canbus_map[13].address @stack_safety.safetodischarge
sc_canbus_map[14].address @stack_current_limit.charge_current_limit
sc_canbus_map[15].address @stack_current_limit.charge_current_percent
sc_canbus_map[16].address @stack_current_limit.discharge_current_limit
sc_canbus_map[17].address @stack_current_limit.discharge_current_percent
sc_canbus_map[18].address @stack_control.connection_state
sc_canbus_map[19].address @stack_safety.clear_faults
sc_canbus_map[20].address @stack_control.requested_state
sc_canbus_map[21].address @sc_controller_heartbeat.value

-- NEW --

sc_canbus_map[22].address @stack_fault_voltage_hi
sc_canbus_map[23].address @stack_fault_voltage_lo
sc_canbus_map[24].address @stack_fault_therm_hi
sc_canbus_map[25].address @stack_fault_therm_lo
sc_canbus_map[26].address @stack_fault_charge_therm_hi
sc_canbus_map[27].address @stack_fault_charge_therm_lo
sc_canbus_map[28].address @stack_fault_current_hi
sc_canbus_map[29].address @stack_fault_current_lo
sc_canbus_map[30].address @stack_fault_coil_fail
sc_canbus_map[31].address @stack_fault_linkbus_wdt

sc_canbus_map[32].address @stack_soc.vfull
sc_canbus_map[33].address @stack_soc.vempty
```

# Installation of Hardware
Install splitter at nuvation bms terminate male connection at CANbus input on nuvation bms low voltage controller. Connect RJ45 termination resistor to one female splitter port and the gateway_CAN0 line to the other.
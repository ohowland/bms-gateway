# Setup Gateway Hardware
## Install the Peak Linux Drivers (download latest from website) *- required*

`https://www.peak-system.com/fileadmin/media/linux/index.htm`

```
make
make -C driver NET=NETDEV_SUPPORT
sudo make install
sudo modprobe pcan
```  

## Auto-up CAN interfaces *- required*
DEBIAN 10:
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

UBUNTU 18.04LTS:  
The script `setup/canup-ubuntu-19.sh` will configure the /etc/systemd/network with the following:

```
[match]  
name=can0  
  
[CAN]  
...
  
[match]  
name=can1  
  
[CAN]  
...
```  
Unforuntatly ubuntu 18.04 LTS uses systemd-237 and we need systemd-239 for this to work.  
we can always use the command:

`ip link set dev can0 up type can bitrate 500000 restart-ms 1000`  
`ip link set dev can1 up type can bitrate 500000 restart-ms 1000`

inspect the can interface with: `ip -details link show can0`

This has been placed in the script `canup-ubuntu-18.sh` copy this file into the
`/etc/init.d/` folder. This will run on startup.

## Run the modprobe script (autoload pcan)

`/setup/modprobe-pcan.sh`

# Configure the Gateway Software

`sudo apt install virtualenv`  
`virtualenv -p python3 venv && source venv/bin/activate`  
`pip install -r requirements.txt`

## Create the gateway.service unit (autostart) *- required*
this is done using systemd:

use the unit file `/setup/gateway.service` 
this file can be placed any number of locations, one that works is: `~/.config/systemd/user/`, though for this project we will make it part of the system and locate it at `/etc/systemd/system/`. This is not advisable, as the script has root access.  

Enable the unit with `systemctl enable gateway.service` and reload the systemd daemon to pickup the new service `systemctl daemon-reload`  

Start the service with `systemctl start gateway.service` and check status with `systemctl status gateway.service`

Follow status with `journalctl -f -u gateway.service`   

## Remove 'Wait for Network to be Configured' dependency

`systemctl show -p WantedBy network-online.target` shows that this occurs due to iscsid which has a dependency on the network. We're not using this service, so it can be disabled:  
`sudo systemctl disable iscsid.service`

## Enable ssh server *- required*
`sudo apt-get install openssh-server`  
Allow traffic through the firewall:
`sudo ufw allow ssh`

# Commissioning Test Environment

will need PCANusb and linux host.

`sudo apt-get install python3-dev, pip3, virtualenv, git, vim`

`pip install cantools`

Connect PCANusb to linux test pc check the link:  
`ip link dev set can0 type can bitrate 500000`  
`ip link set can0 up`

## CANbus verification

Connect CANbus cabling from can0 to target device. in the terminal use:  

`candump can0`  

to confirm raw frames are being set on the canbus.
Another option is to use pcanview, which may expedite the process.

Another option is to use PCANusb with busmaster. Associate the database files with the project and you should be able to verify that the messages are being read/scaled correctly.

## Verify DBC file

unsure if Nuvation BMS is litten endian or big endian. They're also not very clear on the size and scaling of the registers. using cantools:  

`candump can0 | cantools decode config/*.dbc` OR `cantools monitor config/*.dbc` and matching against values read from nuvation BMS. Do this for both the SMA and Nuvation fix errors where found 

## Run integration test suite

God I broke all of these.

`nosetests --nocapture -l debug -v`

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

## Nuvation BMS

The BMS utilizes an unterminated RJ-45 jack for communication. Proper communication requires an RJ-45 splitter and termination plug, both are included in the installation kit.

Install splitter at Nuvation BMS and terminate male connection at CANbus input on BMS low voltage controller. Connect RJ45 termination resistor to one female splitter port and the gateway_CAN0 line to the other.

## SMA Sunny Island

## Gateway



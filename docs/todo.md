# Documentation
- [x] PeakCAN driver installation and testing
- [x] CAN interface auto-up
- [ ] Testing agenda for IE Facility:
  1. [x] Document process for checking CAN signal integrity
  2. [ ] Process for checking CAN messaging integrity (scale, addr, size)
- [x] Document connector build
- [x] Finalize parts list

# Core Code
- [x] Use filters on CANreader to reject unknown messages
- [x] Instrument software to log all the errors in debug mode
- [ ] Command line interface dump object data.  
Referred to as a REPL, use the subprocess module and pipes, see SO post here:
https://stackoverflow.com/questions/19880190/interactive-input-output-using-python [ ] Define method for writing static values to SMA
- [x] Finish DBC for nuvation
- [x] Define method for translating nuvation alarms (bool) to SMA alarm (two bit)
- [x] Initialize writer before allowing publish to canbus
  1. [x] Initialize static values in `self._control` of the inverter (writer)
  2. [x] Initialize unused alarms (are there any unused alarms?) in the inverter (writer)
  2. [x] Wait until all signal names are found in `self.control` before enabling can publishing 
- [x] Read a charge V and discharge V from nuvation, report to SMA. what registers are we mapping? these registers are in the dbc file after the nuvation alarms.
- [x] limit error log size, see rotatinghandler
- [x] Verify behavior when None is return from Map
- [x] use pylint to clean up code.
- [x] define error paths in software, what errors should cause the system to crash/restart? what should be handled internally?

# Testing hardware/code
- [ ] Check unit test coverage
- [x] Complete basic unittests for each module
- [x] Write integration tests
- [ ] Test error handling
  1. [x] loss of connection
  2. [x] out of range id recieved
  3. [x] what happens when a read, write, or translate loop crashes? I think the service should exit and allow systemd to restart it.
this should only happen on an unexpected error.

# System Scripts
- [x] Write chronjob scripts for pushing errors to github **IGNORED**
- [x] Write scripts for auto boot. running as systemd
- [x] Network setup script
- [x] Script to download required packages
  - canutils, virtualenv, openssh-server
- [x] Start SSH server. this will automatically come up with openssh-server, remember to let through firewall.

# Hardware Build Setup
- [x] Build rj45-db9 connectors with termination
- [x] Install mPCIe CAN cards

# Gateway configraution
- [x] SSH access from ethernet interface
- [x] Install and test PCAN drivers on embedded PC

# Component Ordering
- [x] 2x LogicSupply PCs
- [x] 2x Peak mPCIe dual can cards
- [x] 4x CAN-RJ45 converters

# Before Shipping
- [ ] Configure ethernet settings:
- unit #1 (Tom's FIL House):  
ip: 192.168.254.88  
subnet: 255.255.255.0  
gateway: 192.168.254.254
dns 192.168.16.2

- unit #2 (HLM Residence):  
ip: 172.16.200.88
subnet: 255.255.255.0
gateway 172.16.0.1
dns: 172.16.100.1
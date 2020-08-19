# Documentation
- [x] PeakCAN driver installation and testing
- [x] CAN interface auto-up
- [ ] Testing agenda for IE Facility:
  1. [x] Document process for checking CAN signal integrity
  2. [ ] Process for checking CAN messaging integrity (scale, addr, size)
- [x] Document connector build
- [ ] Finalize parts list

# Core Code
- [x] Use filters on CANreader to reject unknown messages
- [x] Instrument software to log all the errors in debug mode
- [ ] Command line interface dump object data.  
Referred to as a REPL, use the subprocess module and pipes, see SO post here:
https://stackoverflow.com/questions/19880190/interactive-input-output-using-python [ ] Define method for writing static values to SMA
- [x] Finish DBC for nuvation
- [x] Define method for translating nuvation alarms (bool) to SMA alarm (two bit)
- [ ] Initialize writer before allowing publish to canbus
  1. [ ] Initialize static values in `self._control` of the inverter (writer)
  2. [ ] Initialize unused alarms (are there any unused alarms?) in the inverter (writer)
  2. [ ] Wait until all signal names are found in `self.control` before enabling can publishing 
- [ ] Read a charge V and discharge V from nuvation, report to SMA. what registers are we mapping? these registers are in the dbc file after the nuvation alarms.
- [x] limit error log size, see rotatinghandler
- [ ] Verify behavior when None is return from Map

# Testing hardware/code
- [ ] Check unit test coverage
- [x] Complete basic unittests for each module
- [ ] Write integration tests
- [ ] Write test for PCANPCI
- [ ] Test PCANPCI from second system using PCANUSB

# System Scripts
- [x] Write chronjob scripts for pushing errors to github **IGNORED**
- [x] Write scripts for auto boot. running as systemd
- [x] Network setup script
- [ ] Script to download required packages
  - git, canutils, python3.6, pip3, virtualenv, gcc, build-essentials, openssh-server
- [x] Start SSH server. this will automatically come up with openssh-server, remember to let through firewall.

# Hardware Build Setup
- [ ] Build rj45-db9 connectors with termination
- [ ] Install mPCIe CAN cards

# Gateway configraution
- [ ] SSH access from ethernet interface
- [ ] Install and test PCAN drivers on embedded PC

# Component Ordering
- [x] 2x LogicSupply PCs
- [x] 2x Peak mPCIe dual can cards
- [x] 4x CAN-RJ45 converters

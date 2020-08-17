# Documentation
- [x] PeakCAN driver installation and testing
- [x] CAN interface auto-up
- [ ] Testing agenda for IE Facility:
  1. [ ] Document process for checking CAN signal integrity
  2. [ ] Process for checking CAN messaging integrity (scale, addr, size)
- [x] Document connector build

# Core Code
- [ ] Use filters on CANreader to reject unknown messages
- [ ] Instrument software to log all the errors in debug mode
- [ ] Command line interface dump object data.
- [x] Finish DBC for nuvation

# Testing hardware/code
- [ ] Check unit test coverage
- [x] Complete basic unittests for each module
- [ ] Write integration tests
- [ ] Write test for PCANPCI
- [ ] Test PCANPCI from second system using PCANUSB

# System Scripts
- [ ] Write chronjob scripts for pushing errors to github 
- [ ] Write scripts for auto boot
- [x] Network setup script
- [ ] Script to download required packages
  - git, canutils, python3.6, pip3, virtualenv, gcc, build-essentials

# Hardware Build Setup
- [ ] Build rj45-db9 connectors with termination
- [ ] Install mPCIe CAN cards

# Gateway configraution
- [ ] SSH access from ethernet interface
- [ ] Install and test PCAN drivers on embedded PC

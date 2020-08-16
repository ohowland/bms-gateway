# Setup test environment

will need PCANusb and linux host.

Confirm drives are installed:
``` grep PEAK_ /boot/config-`uname -r` ```

Confirm can device is initialized:
``` lsmod | grep ^peak ```

should see peak_usb

Setup

# CANbus verification

Connect PCANusb to linux test pc check the link:
```ip link dev add

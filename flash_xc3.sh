#!/bin/bash

set -e
set -x

/sbin/fxload -t fx2 -I /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/xusb_xp2.hex -D /dev/bus/usb/001/*`cat /sys/bus/usb/devices/1-3/devnum`
sleep 10
../xc3sprog/build/xc3sprog -c xpc -m /opt/Xilinx/14.7/ISE_DS/ISE/xbr/data -v build/urukul.jed:w

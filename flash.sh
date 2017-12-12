#!/bin/bash

set -e
source /opt/Xilinx/14.7/ISE_DS/settings64.sh
XIL_IMPACT_USE_LIBUSB=1 impact -batch flash.cmd

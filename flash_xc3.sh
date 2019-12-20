#!/bin/bash

set -e

XC3SPROG=xc3sprog
CABLE=${1-xpc}

set -x
$XC3SPROG -c $CABLE -m /opt/Xilinx/14.7/ISE_DS/ISE/xbr/data -v build/urukul.jed:w

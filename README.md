# Urukul CPLD code

[Urukul overview](https://github.com/sinara-hw/Urukul/wiki)

[Urukul Schematics/Layout](https://github.com/sinara-hw/Urukul/releases)

[NU-Servo](https://github.com/m-labs/nu-servo)

## Building

Needs [migen](https://github.com/m-labs/migen) and [Xilinx ISE](https://www.xilinx.com/products/design-tools/ise-design-suite.html). Assumes ISE is installed in ``/opt/Xilinx``.

```
make
```

## Flashing

With Digilent [JTAG HS2](https://store.digilentinc.com/jtag-hs2-programming-cable/) cable:

  - download firmware to dongle. Manually (adjust USB bus as needed):
  ```
  /sbin/fxload -t fx2 -I /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/xusb_xp2.hex -D /dev/bus/usb/001/*`cat /sys/bus/usb/devices/1-3/devnum`
  ```
  or automatically via the ``udev`` rule:
  ```
  SUBSYSTEM=="usb", ACTION="add", ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", ATTR{manufacturer}=="Digilent", RUN+="/usr/bin/fxload -v -t fx2 -I /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/xusb_xp2.hex -D $tempnode"
  ```

  - install [xc3sprog](http://xc3sprog.sourceforge.net/)

  - ``flash_xc3.sh jtaghs2``

  - look for ``Verify: Success``

# License

GPLv3+

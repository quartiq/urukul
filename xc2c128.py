from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.build.xilinx.ise import XilinxISEToolchain

_io = [
        ("user_led", 0, Pins("P138"), IOStandard("LVCMOS33")),

        ("scki", 0, Pins("P30"), IOStandard("LVCMOS33")),
        ]


class Platform(XilinxPlatform):
    def __init__(self):
        XilinxPlatform.__init__(self, "xc2c128-6-tq144", _io)
        self.toolchain.xst_opt = """-ifmt MIXED"""
"""
ngdbuild ...

cpldfit -ofmt verilog -optimize speed -p xc2c128-6-tq144 top.ngd
taengine -f top.vm6 -detail -iopath -l top.tim
hprep6 -s IEEE1532 -i top.vm6
"""

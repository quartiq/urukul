from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.build.xilinx.ise import XilinxISEToolchain

_io = [
        ("tp", 0, Pins("P143")),
        ("tp", 1, Pins("P140")),
        ("tp", 2, Pins("P138")),
        # ("tp", 3, Pins("P136")),
        # ("tp", 4, Pins("P134")),

        # P112 is open on Urukul/v1.0
        ("ifc_mode", 0, Pins("P104 P105 P110 P112")),

        # P111 is IFC_MODE_SEL3 on Urukul/v1.0
        # 10k low: AD9912, 0R high: AD9910
        ("variant", 0, Pins("P111")),

        # fail save LVDS enable, LVDS mode selection
        # high: type 2 receiver, failsafe low
        ("fsen", 0, Pins("P115")),

        ("clk", 0,
            Subsignal("div", Pins("P11")),
            Subsignal("in_sel", Pins("P12")),
            Subsignal("mmcx_osc_n_sel", Pins("P136")),
            Subsignal("osc_en_n", Pins("P134"))),

        ("att", 0,
            Subsignal("clk", Pins("P95")),
            Subsignal("le", Pins("P94")),
            Subsignal("rst_n", Pins("P96")),
            Subsignal("s_in", Pins("P133")),
            Subsignal("s_out", Pins("P97"))),

        ("dds_common", 0,
            Subsignal("master_reset", Pins("P102")),
            Subsignal("reset", Pins("P120")),
            Subsignal("io_reset", Pins("P129")),
            Subsignal("profile", Pins("P130 P131 P132"))),

        ("dds_sync", 0,
            Subsignal("clk0", Pins("P38"), Misc("PULLUP")),  # DDS_SYNC_CLK0
            Subsignal("clk_out_en", Pins("P86")),  # DDS_SYNC_CLK_OUTEN
            Subsignal("sync_sel", Pins("P60")),  # DDS_SYNC_CLKSEL
            Subsignal("sync_out_en", Pins("P92"))),  # DDS_SYNC_OUTEN

        ("dds", 0,
            Subsignal("rf_sw", Pins("P103")),
            Subsignal("led", Pins("P128 P126")),
            Subsignal("smp_err", Pins("P19"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("P21"), Misc("PULLUP")),
            Subsignal("io_update", Pins("P4")),
            Subsignal("sck", Pins("P3")),
            Subsignal("sdo", Pins("P113"), Misc("PULLUP")),
            Subsignal("sdi", Pins("P2")),
            Subsignal("cs_n", Pins("P119"))),

        ("dds", 1,
            Subsignal("rf_sw", Pins("P101")),
            Subsignal("led", Pins("P118 P125")),
            Subsignal("smp_err", Pins("P28"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("P35"), Misc("PULLUP")),
            Subsignal("io_update", Pins("P10")),
            Subsignal("sck", Pins("P9")),
            Subsignal("sdo", Pins("P6"), Misc("PULLUP")),
            Subsignal("sdi", Pins("P7")),
            Subsignal("cs_n", Pins("P5"))),

        ("dds", 2,
            Subsignal("rf_sw", Pins("P100")),
            Subsignal("led", Pins("P116 P117")),
            Subsignal("smp_err", Pins("P40"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("P41"), Misc("PULLUP")),
            Subsignal("io_update", Pins("P14")),
            Subsignal("sck", Pins("P13")),
            Subsignal("sdo", Pins("P17"), Misc("PULLUP")),
            Subsignal("sdi", Pins("P15")),
            Subsignal("cs_n", Pins("P16"))),

        ("dds", 3,
            Subsignal("rf_sw", Pins("P98")),
            Subsignal("led", Pins("P121 P124")),
            Subsignal("smp_err", Pins("P39"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("P49"), Misc("PULLUP")),
            Subsignal("io_update", Pins("P25")),
            Subsignal("sck", Pins("P22")),
            Subsignal("sdo", Pins("P23"), Misc("PULLUP")),
            Subsignal("sdi", Pins("P26")),
            Subsignal("cs_n", Pins("P24"))),

        ("eem", 0,
            Subsignal("io", Pins("P30")),
            Subsignal("oe", Pins("P58"))),
        ("eem", 1,
            Subsignal("io", Pins("P53")),
            Subsignal("oe", Pins("P52"))),
        ("eem", 2,
            Subsignal("io", Pins("P45")),
            Subsignal("oe", Pins("P57"))),
        ("eem", 3,
            Subsignal("io", Pins("P50")),
            Subsignal("oe", Pins("P61"))),
        ("eem", 4,
            Subsignal("io", Pins("P43")),
            Subsignal("oe", Pins("P64"))),
        ("eem", 5,
            Subsignal("io", Pins("P51")),
            Subsignal("oe", Pins("P59"))),
        ("eem", 6,
            Subsignal("io", Pins("P54")),
            Subsignal("oe", Pins("P68"))),
        ("eem", 7,
            Subsignal("io", Pins("P56")),
            Subsignal("oe", Pins("P69"))),
        ("eem", 8,
            Subsignal("io", Pins("P32")),
            Subsignal("oe", Pins("P80"))),
        ("eem", 9,
            Subsignal("io", Pins("P71")),
            Subsignal("oe", Pins("P85"))),
        ("eem", 10,
            Subsignal("io", Pins("P74")),
            Subsignal("oe", Pins("P82"))),
        ("eem", 11,
            Subsignal("io", Pins("P78")),
            Subsignal("oe", Pins("P77"))),
        ("eem", 12,
            Subsignal("io", Pins("P70")),
            Subsignal("oe", Pins("P79"))),
        ("eem", 13,
            Subsignal("io", Pins("P87")),
            Subsignal("oe", Pins("P81"))),
        ("eem", 14,
            Subsignal("io", Pins("P76")),
            Subsignal("oe", Pins("P91"))),
        ("eem", 15,
            Subsignal("io", Pins("P88")),
            Subsignal("oe", Pins("P83"))),
]


class Platform(XilinxPlatform):
    def __init__(self):
        XilinxPlatform.__init__(self, "xc2c128-6-tq144", _io)
        self.toolchain.xst_opt = "-ifmt MIXED"
        self.toolchain.par_opt = ("-optimize speed -unused pullup "
                "-iostd LVCMOS33")

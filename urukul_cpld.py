from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.build.xilinx.ise import XilinxISEToolchain

_io = [
        ("tp", 0, Pins("A4")),
        ("tp", 1, Pins("A5")),
        ("tp", 2, Pins("B5")),
        ("tp", 3, Pins("A6")),
        ("tp", 4, Pins("A7")),

        ("ifc_mode", 0, Pins("E14 B16 A16 B15")),
        ("hw_rev", 0, Pins("C16 D15 E15 E16")),

        # 10k low: AD9912, 0R high: AD9910
        ("variant", 0, Pins("A15")),

        # fail save LVDS enable, LVDS mode selection
        # high: type 2 receiver, failsafe low
        ("fsen", 0, Pins("N15")),

        ("clk", 0,
            Subsignal("div", Pins("E5")),
            Subsignal("in_sel", Pins("G5")),
            Subsignal("mmcx_osc_sel", Pins("C11")),
            Subsignal("osc_en_n", Pins("B6"))),

        ("dds_common", 0,
            Subsignal("master_reset", Pins("F16")),
            Subsignal("io_reset", Pins("B9"))),

        ("dds_sync", 0,
            Subsignal("clk0", Pins("P5"), Misc("PULLUP")),  # DDS_SYNC_CLK0
            Subsignal("clk_out_en", Pins("T5")),  # DDS_SYNC_CLK_OUTEN
            Subsignal("sync_sel", Pins("T10")),  # DDS_SYNC_CLKSEL
            Subsignal("sync_out_en", Pins("R6"))),  # DDS_SYNC_OUTEN

        ("att", 0,
            Subsignal("clk", Pins("E9")),
            Subsignal("rst_n", Pins("N9")),
            Subsignal("le", Pins("E10 P8 C8 K4")),
            Subsignal("s_in", Pins("B7 D8 D7 L5")),
            Subsignal("s_out", Pins("C10 C9 E8 R9"))),

        ("dds", 0,
            Subsignal("rf_sw", Pins("D13")),
            Subsignal("led", Pins("E11 B10")),
            Subsignal("smp_err", Pins("D4"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("E4"), Misc("PULLUP")),
            Subsignal("io_update", Pins("B1")),
            Subsignal("profile", Pins("A9 B8 A8")),
            Subsignal("osk", Pins("C13")),
            Subsignal("drover", Pins("D11")),
            Subsignal("drhold", Pins("E13")),
            Subsignal("drctl", Pins("C14")),
            Subsignal("reset", Pins("B13")),
            Subsignal("sck", Pins("A2")),
            Subsignal("sdo", Pins("A3"), Misc("PULLUP")),
            Subsignal("sdi", Pins("B2")),
            Subsignal("cs_n", Pins("B3"))),

        ("dds", 1,
            Subsignal("rf_sw", Pins("C12")),
            Subsignal("led", Pins("A13 A11")),
            Subsignal("smp_err", Pins("J1"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("K2"), Misc("PULLUP")),
            Subsignal("io_update", Pins("P4")),
            Subsignal("profile", Pins("D3 D2 E2")),
            Subsignal("osk", Pins("C3")),
            Subsignal("drover", Pins("B4")),
            Subsignal("drhold", Pins("C7")),
            Subsignal("drctl", Pins("C4")),
            Subsignal("reset", Pins("F2")),
            Subsignal("sck", Pins("K3")),
            Subsignal("sdo", Pins("J3"), Misc("PULLUP")),
            Subsignal("sdi", Pins("K5")),
            Subsignal("cs_n", Pins("J4"))),

        ("dds", 2,
            Subsignal("rf_sw", Pins("D10")),
            Subsignal("led", Pins("A14 B14")),
            Subsignal("smp_err", Pins("P6"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("N7"), Misc("PULLUP")),
            Subsignal("io_update", Pins("H5")),
            Subsignal("profile", Pins("M1 M6 M5")),
            Subsignal("osk", Pins("L1")),
            Subsignal("drover", Pins("L2")),
            Subsignal("drhold", Pins("L4")),
            Subsignal("drctl", Pins("K1")),
            Subsignal("reset", Pins("R10")),
            Subsignal("sck", Pins("H4")),
            Subsignal("sdo", Pins("J2"), Misc("PULLUP")),
            Subsignal("sdi", Pins("H3")),
            Subsignal("cs_n", Pins("H1"))),

        ("dds", 3,
            Subsignal("rf_sw", Pins("D9")),
            Subsignal("led", Pins("A12 B11")),
            Subsignal("smp_err", Pins("N6"), Misc("PULLUP")),
            Subsignal("pll_lock", Pins("P7"), Misc("PULLUP")),
            Subsignal("io_update", Pins("E3")),
            Subsignal("profile", Pins("N3 P1 P2")),
            Subsignal("osk", Pins("N2")),
            Subsignal("drover", Pins("N5")),
            Subsignal("drhold", Pins("N4")),
            Subsignal("drctl", Pins("N1")),
            Subsignal("reset", Pins("T8")),
            Subsignal("sck", Pins("H2")),
            Subsignal("sdo", Pins("G3"), Misc("PULLUP")),
            Subsignal("sdi", Pins("F5")),
            Subsignal("cs_n", Pins("G4"))),

        ("eem", 0,
            Subsignal("io", Pins("M2" )),
            Subsignal("oe", Pins("P15"))),
        ("eem", 1,
            Subsignal("io", Pins("R13")),
            Subsignal("oe", Pins("M15"))),
        ("eem", 2,
            Subsignal("io", Pins("T16")),
            Subsignal("oe", Pins("K15"))),
        ("eem", 3,
            Subsignal("io", Pins("R16")),
            Subsignal("oe", Pins("N16"))),
        ("eem", 4,
            Subsignal("io", Pins("R15")),
            Subsignal("oe", Pins("L15"))),
        ("eem", 5,
            Subsignal("io", Pins("R14")),
            Subsignal("oe", Pins("M16"))),
        ("eem", 6,
            Subsignal("io", Pins("R12")),
            Subsignal("oe", Pins("L16"))),
        ("eem", 7,
            Subsignal("io", Pins("T15")),
            Subsignal("oe", Pins("P16"))),
        ("eem", 8,
            Subsignal("io", Pins("M3")),
            Subsignal("oe", Pins("R7"))),
        ("eem", 9,
            Subsignal("io", Pins("J5")),
            Subsignal("oe", Pins("T4"))),
        ("eem", 10,
            Subsignal("io", Pins("R3")),
            Subsignal("oe", Pins("R4"))),
        ("eem", 11,
            Subsignal("io", Pins("R2")),
            Subsignal("oe", Pins("R5"))),
        ("eem", 12,
            Subsignal("io", Pins("R1")),
            Subsignal("oe", Pins("M7"))),
        ("eem", 13,
            Subsignal("io", Pins("T1")),
            Subsignal("oe", Pins("R8"))),
        ("eem", 14,
            Subsignal("io", Pins("T2")),
            Subsignal("oe", Pins("T7"))),
        ("eem", 15,
            Subsignal("io", Pins("T3")),
            Subsignal("oe", Pins("M8"))),
]


class Platform(XilinxPlatform):
    def __init__(self):
        XilinxPlatform.__init__(self, "xc2c256-6-ft256", _io)
        self.toolchain.xst_opt = "-ifmt MIXED"
        self.toolchain.par_opt = ("-optimize speed -unused pullup "
                "-iostd LVCMOS33")

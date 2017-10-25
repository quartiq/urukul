from migen import *


class CFG(Module):
    def __init__(self, platform, n=4):
        self.write = Record([
            ("rf_sw", n),
            ("led", n),
            ("profile", 3),
            ("in_sel", 1),
            ("reset", 1),
            ("io_reset", 1),
            ("master_reset", 1),
            ("att_rst", 1),
            ("smp_err", n),
            ("pll_lock", n),
        ])
        self.read = Record(self.write.layout)
        dds_common = platform.lookup_request("dds_common")
        att = platform.lookup_request("att")
        in_sel = platform.request("in_sel")
        self.comb += [
                dds_common.profile.eq(self.write.profile),
                self.read.profile.eq(dds_common.profile),

                in_sel.eq(self.write.in_sel),
                self.read.in_sel.eq(in_sel),

                dds_common.reset.eq(self.write.reset),
                self.read.reset.eq(dds_common.reset),

                dds_common.reset.eq(self.write.io_reset),
                self.read.reset.eq(dds_common.io_reset),

                dds_common.master_reset.eq(self.write.master_reset),
                self.read.master_reset.eq(dds_common.master_reset),

                att.rst_n.eq(~self.write.att_rst),
                self.read.att_rst.eq(~att.rst_n),
        ]

        for i in range(n):
            sw = platform.request("eem", 12 + i)
            dds = platform.lookup_request("dds", i)
            self.comb += [
                    sw.oe.eq(0),
                    dds.rf_sw.eq(sw.io ^ self.write.rf_sw[i]),
                    self.read.rf_sw[i].eq(dds.rf_sw),
                    dds.led[0].eq(dds.rf_sw),

                    dds.led[1].eq(self.write.led[i]),
                    self.read.led[i].eq(dds.led[1]),

                    self.read.smp_err[i].eq(dds.smp_err),

                    self.read.pll_lock[i].eq(dds.pll_lock),
            ]



class Top(Module):
    def __init__(self, platform):
        self.clock_domains.cd_sys = ClockDomain("sys", reset_less=True)
        sck = platform.request("eem", 0)
        self.comb += [
                sck.oe.eq(0),
                self.cd_sys.clk.eq(sck.io),
        ]

        ifc_mode = platform.request("ifc_mode")
        dds_common = platform.request("dds_common")
        att = platform.request("att")
        dds = [platform.request("dds", i) for i in range(4)]
        # att
        # sr
        # cs mux
        # ifc mode
        # spi, io_update, io_update ret
        # sync routing, dds_common

        self.submodules += CFG(platform)

        tp = [platform.request("tp", i) for i in range(5)]
        self.sync += tp[0].eq(~tp[0])


def main():
    from urukul_cpld import Platform
    p = Platform()
    top = Top(p)
    p.build(top, mode="cpld")


if __name__ == "__main__":
    main()

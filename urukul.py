from migen import *


class SR(Module):
    def __init__(self, width):
        self.sdi = Signal()
        self.sdo = Signal()
        self.sel = Signal()

        self.data = Signal(width)

        # # #

        sr = Signal(width)
        cnt = Signal(max=width, reset=width-1)
        cnt_done = Signal()

        self.comb += [
                self.sdo.eq(sr[-1]),
                cnt_done.eq(cnt == 0),
        ]
        i = Signal()
        self.sync.sck1 += [
                If(self.sel,
                    i.eq(self.sdi)
                )
        ]
        self.sync.sck0 += [
                If(cnt_done,
                    cnt.eq(cnt.reset),
                    self.data.eq(sr),
                ).Elif(self.sel,
                    sr.eq(Cat(i, sr)),
                    cnt.eq(cnt - 1)
                )
        ]


class CFG(Module):
    def __init__(self, platform, n=4):
        self.cfg = Record([
            ("rf_sw", n),
            ("led", n),
            ("profile", 3),

            ("att_le", 1),

            ("clk_sel", 1),
            ("sync_sel", 1),

            ("dds_rst", 1),
            ("io_rst", 1),
            ("att_rst", 1),
        ])
        dds_common = platform.lookup_request("dds_common")
        dds_sync = platform.lookup_request("dds_sync")
        att = platform.lookup_request("att")
        clk = platform.lookup_request("clk")
        self.comb += [
                dds_common.profile.eq(self.cfg.profile),
                clk.in_sel.eq(self.cfg.clk_sel),
                dds_sync.sync_sel.eq(self.cfg.sync_sel),
                dds_common.reset.eq(self.cfg.dds_rst),
                dds_common.master_reset.eq(dds_common.reset),
                dds_common.io_reset.eq(self.cfg.io_rst),
                att.rst_n.eq(~self.cfg.att_rst),
                att.le.eq(self.cfg.att_le),
        ]

        for i in range(n):
            sw = platform.request("eem", 12 + i)
            dds = platform.lookup_request("dds", i)
            self.comb += [
                    sw.oe.eq(0),
                    dds.rf_sw.eq(sw.io ^ self.cfg.rf_sw[i]),
                    dds.led[0].eq(dds.rf_sw),  # green
                    dds.led[1].eq(self.cfg.led[i] | dds.smp_err | ~dds.pll_lock),
            ]


class Top(Module):
    def __init__(self, platform):
        clk = platform.request("clk")
        dds_sync = platform.request("dds_sync")
        dds_common = platform.request("dds_common")
        ifc_mode = platform.request("ifc_mode")
        att = platform.request("att")
        dds = [platform.request("dds", i) for i in range(4)]

        ts_clk_div = TSTriple()
        self.specials += [
                ts_clk_div.get_tristate(clk.div)
        ]

        eem = []
        for i in range(12):
            tsi = TSTriple()
            eemi = platform.request("eem", i)
            self.specials += tsi.get_tristate(eemi.io)
            self.comb += eemi.oe.eq(tsi.oe)
            eem.append(tsi)

        # AD9910 only
        self.clock_domains.cd_sys = ClockDomain("sys", reset_less=True)
        self.clock_domains.cd_sck1 = ClockDomain("sck0", reset_less=True)
        self.clock_domains.cd_sck0 = ClockDomain("sck1", reset_less=True)

        sck1, nu_sck = Signal(), Signal()
        self.specials += [
                Instance("CLK_DIV2", i_CLKIN=dds_sync.clk0,
                    o_CLKDV=self.cd_sys.clk),
                Instance("BUFG", i_I=eem[7].i, o_O=nu_sck),
                Instance("BUFG", i_I=eem[0].i, o_O=sck1),
        ]

        en_9910 = Signal()  # AD9910 populated (instead of AD9912)
        en_nu = Signal()  # NU-Servo operation with quad SPI
        en_eemb = Signal()  # EEM-B connected
        en_unused = Signal()
        self.comb += Cat(en_9910, en_nu, en_eemb, en_unused).eq(ifc_mode)

        self.comb += [
                [eem[i].oe.eq(0) for i in range(12) if i not in (2, 10)],
                eem[2].oe.eq(~en_nu),
                eem[10].oe.eq(~en_nu & en_eemb),
                eem[10].o.eq(eem[6].i),
                self.cd_sck1.clk.eq(Mux(en_nu, nu_sck, sck1)),
                self.cd_sck0.clk.eq(~self.cd_sck1.clk),
                dds_sync.clk_out_en.eq(~en_nu & en_eemb & en_9910),
                dds_sync.sync_out_en.eq(~en_nu & en_eemb & en_9910),
                # 1: div-by-4 for AD9910
                # z: div-by-1 for AD9912
                ts_clk_div.oe.eq(~en_9910),
                ts_clk_div.o.eq(1),
        ]

        cfg = CFG(platform)
        sr = SR(len(cfg.cfg))
        self.submodules += cfg, sr

        sel = Signal(8)
        self.comb += [
                Array(sel)[Cat(eem[3].i, eem[4].i, eem[5].i)].eq(1),
                att.clk.eq(sel[3] & sck1),
                att.s_in.eq(eem[1].i),
                If(sel[3],
                    eem[2].o.eq(att.s_out)),

                sr.sel.eq(sel[1]),
                sr.sdi.eq(eem[1].i),
                If(sel[1],
                    eem[2].o.eq(sr.sdo)),

                cfg.cfg.raw_bits().eq(sr.data)
        ]
        for seli, ddsi, nu_mosi in zip(sel[4:], dds, eem[8:]):
            self.comb += [
                    ddsi.cs_n.eq(~(seli | (en_nu & eem[2].i))),
                    ddsi.sck.eq(Mux(en_nu & ~seli, nu_sck, sck1)),
                    ddsi.sdi.eq(Mux(en_nu & ~eem[5].i, nu_mosi.i,
                        eem[1].i)),
                    If(seli,
                        eem[2].o.eq(ddsi.sdo)),
                    ddsi.io_update.eq(eem[6].i),
            ]

        for ddsi in dds:
            self.comb += platform.request("tp").eq(ddsi.smp_err)
        self.comb += platform.request("tp").eq(
                ~Cat([ddsi.pll_lock for ddsi in dds]) == 0)


def main():
    from urukul_cpld import Platform
    p = Platform()
    top = Top(p)
    p.build(top, mode="cpld")


if __name__ == "__main__":
    main()

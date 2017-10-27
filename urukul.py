from migen import *


class SR(Module):
    def __init__(self, width):
        self.sdi = Signal()
        self.sdo = Signal()
        self.sel = Signal()

        self.di = Signal(width)
        self.do = Signal(width)

        # # #

        # CPOL = 0, CPHA = 0, strictly width bits per sel cycle

        sr = Signal(width)
        cnt = Signal(max=width, reset=width-1)
        cnt_done = Signal()
        self._cnt_done = cnt_done
        i = Signal()
        self._i = i

        self.comb += [
                self.sdo.eq(sr[-1]),
                cnt_done.eq(cnt == 0),
        ]
        self.sync.sck1 += [
                If(self.sel,
                    i.eq(self.sdi)
                )
        ]
        self.sync.sck0 += [
                If(self.sel,
                    If(cnt_done,
                        self.di.eq(sr),
                        sr.eq(self.do),
                        cnt.eq(cnt.reset)
                    ).Else(
                        sr.eq(Cat(i, sr)),
                        cnt.eq(cnt - 1)
                    )
                )
        ]


class CFG(Module):
    def __init__(self, platform, n=4):
        self.data = Record([
            ("rf_sw", n),
            ("led", n),

            ("profile", 3),

            ("att_le", 1),

            ("mask_nu", 4),

            ("clk_sel", 1),
            ("sync_sel", 1),

            ("io_update", 1),

            ("rst", 1),
            ("io_rst", 1),
        ])
        dds_common = platform.lookup_request("dds_common")
        dds_sync = platform.lookup_request("dds_sync")
        att = platform.lookup_request("att")
        clk = platform.lookup_request("clk")
        ifc_mode = platform.lookup_request("ifc_mode")
        en_9910 = ifc_mode[0]
        self.comb += [
                dds_common.profile.eq(self.data.profile),
                clk.in_sel.eq(self.data.clk_sel),
                dds_sync.sync_sel.eq(self.data.sync_sel),
                dds_common.master_reset.eq(self.data.rst),
                dds_common.io_reset.eq(self.data.io_rst),
                att.rst_n.eq(~self.data.rst),
                att.le.eq(self.data.att_le),
        ]

        for i in range(n):
            sw = platform.request("eem", 12 + i)
            dds = platform.lookup_request("dds", i)
            self.comb += [
                    sw.oe.eq(0),
                    dds.rf_sw.eq(sw.io ^ self.data.rf_sw[i]),
                    dds.led[0].eq(dds.rf_sw),  # green
                    dds.led[1].eq(self.data.led[i] | (en_9910 & (
                        dds.smp_err | ~dds.pll_lock))),  # red
            ]


class Status(Module):
    def __init__(self, platform, n=4):
        self.data = Record([
            ("rf_sw", n),
            ("smp_err", n),
            ("pll_lock", n),
            ("ifc_mode", 4),
        ])
        self.comb += [
                self.data.ifc_mode.eq(platform.lookup_request("ifc_mode"))
        ]
        for i in range(n):
            dds = platform.lookup_request("dds", i)
            self.comb += [
                    self.data.rf_sw[i].eq(dds.rf_sw),
                    self.data.smp_err[i].eq(dds.smp_err),
                    self.data.pll_lock[i].eq(dds.pll_lock),
            ]


class Urukul(Module):
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
            tsi._pin = eemi.io
            self.specials += tsi.get_tristate(eemi.io)
            self.comb += eemi.oe.eq(tsi.oe)
            eem.append(tsi)

        # AD9910 only
        self.clock_domains.cd_sys = ClockDomain("sys", reset_less=True)
        self.clock_domains.cd_sck0 = ClockDomain("sck0", reset_less=True)
        self.clock_domains.cd_sck1 = ClockDomain("sck1", reset_less=True)

        platform.add_period_constraint(eem[0]._pin, 8.)
        platform.add_period_constraint(eem[2]._pin, 8.)

        nu_sck = Signal()
        sync_clk = Signal()
        self.specials += [
                Instance("BUFG", i_I=eem[0].i, o_O=self.cd_sck1.clk),
                Instance("BUFG", i_I=eem[2].i, o_O=nu_sck),
                Instance("BUFG", i_I=dds_sync.clk0, o_O=sync_clk),
                Instance("CLK_DIV2", i_CLKIN=sync_clk,
                    o_CLKDV=self.cd_sys.clk),
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
                self.cd_sck0.clk.eq(~self.cd_sck1.clk),
                dds_sync.clk_out_en.eq(~en_nu & en_eemb & en_9910),
                dds_sync.sync_out_en.eq(~en_nu & en_eemb & en_9910),
                # 1: div-by-4 for AD9910
                # z: div-by-1 for AD9912
                ts_clk_div.oe.eq(~en_9910),
                ts_clk_div.o.eq(1),
        ]

        cfg = CFG(platform)
        stat = Status(platform)
        sr = SR(24)
        assert len(cfg.data) <= len(sr.di)
        assert len(stat.data) <= len(sr.do)
        self.submodules += cfg, stat, sr

        sel = Signal(8)
        cs = Signal(3)
        miso = Signal(8)
        mosi = eem[1].i
        self.comb += [
                cs.eq(Cat(eem[3].i, eem[4].i, ~en_nu & eem[5].i)),
                Array(sel)[cs].eq(1),  # one-hot
                eem[2].o.eq(Array(miso)[cs]),
                miso[3].eq(miso[4]),  # for all-DDS take DDS0:MISO

                att.clk.eq(sel[2] & self.cd_sck1.clk),
                att.s_in.eq(mosi),
                miso[2].eq(att.s_out),

                sr.sel.eq(sel[1]),
                sr.sdi.eq(mosi),
                miso[1].eq(sr.sdo),

                cfg.data.raw_bits().eq(sr.di),
                sr.do.eq(stat.data.raw_bits()),

                dds_common.reset.eq(cfg.data.rst |
                    (~en_9910 & eem[7].i)),
        ]
        for i, ddsi in enumerate(dds):
            seli = Signal()
            nu_mosi = eem[i + 8].i
            en_nu_i = Signal()
            self.comb += [
                    seli.eq(sel[i + 4] | (sel[3] & cfg.data.mask_nu[i])),
                    en_nu_i.eq(~seli & (en_nu & ~cfg.data.mask_nu[i])),
                    ddsi.cs_n.eq(~(seli | (en_nu_i & eem[5].i))),
                    ddsi.sck.eq(Mux(en_nu_i, nu_sck, self.cd_sck1.clk)),
                    ddsi.sdi.eq(Mux(en_nu_i, nu_mosi, mosi)),
                    miso[i + 4].eq(ddsi.sdo),
                    ddsi.io_update.eq(Mux(cfg.data.mask_nu[i],
                        cfg.data.io_update, eem[6].i)),
            ]

        tp = [platform.request("tp", i) for i in range(5)]
        self.comb += [
                tp[0].eq(Cat([ddsi.smp_err for ddsi in dds]) == 0),
                tp[1].eq(Cat([~ddsi.pll_lock for ddsi in dds]) == 0),
                tp[2].eq(sr._cnt_done),
                tp[3].eq(sr._i),
                tp[4].eq(sr.sel),
        ]


def main():
    from urukul_cpld import Platform
    p = Platform()
    urukul = Urukul(p)
    p.build(urukul, build_name="urukul", mode="cpld")


if __name__ == "__main__":
    main()

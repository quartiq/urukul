from collections import namedtuple

from migen import *
from migen.fhdl.specials import Tristate
from migen.build.generic_platform import ConstraintError

from urukul import Urukul
from urukul_cpld import Platform


class SimTristate:
    @staticmethod
    def lower(dr):
        return SimTristateImpl(dr.i, dr.o, dr.oe, dr.target)


class SimTristateImpl(Module):
    def __init__(self, i, o, oe, target):
        self.i = i
        self.o = o
        self.oe = oe
        self.target = target
        self.comb += [
                # If(oe, target.eq(o)),
                # i.eq(Mux(oe, o, target))
                i.eq(target)
        ]


class SimInstance:
    @staticmethod
    def lower(dr):
        return Module()


class TB(Module):
    def __init__(self, platform, dut):
        self.platform = platform
        self.submodules.dut = dut
        for k in "tp dds dds_common dds_sync clk ifc_mode att eem".split():
            v = []
            while True:
                try:
                    v.append(platform.lookup_request(k, len(v)))
                except ConstraintError:
                    break
            if len(v) == 1:
                v = v[0]
            setattr(self, k, v)
        self.cs = Signal(3)
        self.comb += [
                Cat(self.eem[3].io, self.eem[4].io, self.eem[5].io).eq(
                    self.cs)
        ]

    def spi(self, cs, n, mosi):
        # while (yield self.dut.cd_sck0.clk):
        #     pass
        yield self.cs.eq(cs)
        miso = 0
        for i in range(n - 1, -1, -1):
            yield self.eem[1].io.eq((mosi >> i) & 1)
            yield self.eem[0].io.eq(0)
            yield
            yield self.eem[0].io.eq(1)
            miso = (miso << 1) | (yield self.eem[2].io)
            yield
            yield self.eem[0].io.eq(0)
        yield
        yield self.cs.eq(0)
        yield
        return miso

    def test(self):
        p = self.platform
        dut = self.dut
        yield self.ifc_mode[0].eq(1)  # en_9910
        yield self.ifc_mode[1].eq(0)  # en_nu
        yield self.ifc_mode[2].eq(1)  # en_eemb
        yield self.eem[12].io.eq(1)  # rf_sw[0]
        yield self.dds[1].smp_err.eq(1)
        yield self.dds[0].pll_lock.eq(1)
        yield
        yield from self.spi(1, 24, 0x123456)
        yield from self.spi(2, 32, 0xf0f0f0f0)  # ATT
        yield from self.spi(4, 16, 0x1234)
        yield


def main():
    p = Platform()
    dut = Urukul(p)
    tb = TB(p, dut)
    run_simulation(tb, [tb.test()], vcd_name="urukul.vcd",
            # just operate on sck0
            clocks={"sys": 8, "sck1": (16, 4), "sck0": (16, 12)},
            special_overrides={Tristate: SimTristate, Instance: SimInstance})


if __name__ == "__main__":
    main()

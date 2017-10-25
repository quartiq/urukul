from migen import *


class Top(Module):
    def __init__(self, platform):
        scki = platform.request("eem", 0).io
        self.clock_domains.cd_sys = cd_sys = ClockDomain("sys", reset_less=True)
        self.comb += self.cd_sys.clk.eq(scki)

        led = platform.request("dds", 0).led[0]
        self.sync += led.eq(~led)


def main():
    from urukul_cpld import Platform
    p = Platform()
    top = Top(p)
    p.build(top, mode="cpld")


if __name__ == "__main__":
    main()

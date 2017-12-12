def main():
    from urukul_cpld import Platform
    from urukul import Urukul

    p = Platform()
    urukul = Urukul(p)
    p.build(urukul, build_name="urukul", mode="cpld")


if __name__ == "__main__":
    main()

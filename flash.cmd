setMode -bscan
setCable -p auto
# setCableSpeed -speed 6000000
# addDevice -p 1 -file build/pdq_3ch.bit
readIdCode -p 1
# attachFlash -p 1 -spi AT45DB161D
# assignfiletoattachedflash -p 1 -file build/pdq_3ch.mcs
# program -e -v -p 1 -dataWidth 1 -spionly -loadfpga
quit

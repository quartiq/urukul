setMode -bscan
setCable -p auto
# setCableSpeed -speed 6000000
readIdCode -p 1
identify -inferir
identifyMPM
assignFile -p 1 -file build/urukul.jed
program -e -v -p 1
quit

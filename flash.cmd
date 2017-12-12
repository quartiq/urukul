setMode -bscan
setCable -p auto
# setCableSpeed -speed 6000000
identify -inferir
identifyMPM
readIdCode -p 1
assignFile -p 1 -file build/urukul.jed
program -e -v -p 1
quit

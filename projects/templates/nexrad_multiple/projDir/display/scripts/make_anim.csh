#! /bin/bash
#  CIDD example Anim script - Take a series of stills and make an animated GIf
#   - Creates a Unique name for the gif : output??????.gif
#  This example adds a 5 frame "dwell" at the end of the loop
#   It also schedules the originals for removal in 5 minutes.
# F. Hage NCAR/RAP  May 2000

ARGV=( $@ )
ARGC=${#ARGV[@]}
TIME=`date +%Y%m%d_%H%M%S`
mkdir -p ${HOME}/images/save
moviePath=${HOME}/images/save/cidd_loop_${TIME}.gif
echo "Writing movie file: ${moviePath}"

convert -verbose -delay 20 -loop 0 \
    $* \
	${ARGV[${ARGC} -1]} \
	${ARGV[${ARGC} -1]} \
	${ARGV[${ARGC} -1]} \
	${ARGV[${ARGC} -1]} \
	${ARGV[${ARGC} -1]} \
	${moviePath} &

# echo "/bin/rm -f $*" | at now + 5 minutes

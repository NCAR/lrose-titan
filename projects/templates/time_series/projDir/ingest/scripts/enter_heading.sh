#! /bin/bash
# script to enter a heading and append it to a file
#
#--------------------------------------------------------------------

# set the path

export PATH=.:/bin:/usr/bin:/sbin:/usr/sbin:/usr/bin/X11:/usr/local/bin:/usr/local/sbin

#######################################################
# get run time

year=`date +'%Y'`
month=`date +'%m'`
day=`date +'%d'`
hour=`date +'%H'`
min=`date +'%M'`
sec=`date +'%S'`
datestr=${year}${month}${day}.${hour}${min}${sec}

#--------------------------------------------------------------------

echo
echo "**********************************************"
echo "  Runtime: $year/$month/$day $hour:$min:$sec"
echo "**********************************************"
echo "  UTILITY TO ENTER MOBILE PLATFORM HEADING:"
echo "**********************************************"
echo

while [ 1 ]
do
  read -ep "Enter heading (decimal degrees): " heading
  echo "$heading `date`" >> $HOME/headings
done


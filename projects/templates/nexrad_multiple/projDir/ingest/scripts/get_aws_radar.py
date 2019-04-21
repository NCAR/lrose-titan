#!/usr/bin/env python

import os
import getopt
import time
import sys
import string
import urllib

from xml.dom import minidom
from sys import stdin
from urllib import urlopen
from subprocess import call

output_dir = "./"
dry_run = 0
verbose = 0

def usage(prog_name):
    print "Usage: %s [-h] [-o output_dir] (-t time or -st start_time -et end_time) -r radar(s) [-d -v]\n" % prog_name
    print "Description: Script to download nexrad level2 radar data from ncdc web archive.\n"
    print "-h\t\tprint this help message"
    print "-t Single date and time\t\t(YYYYMMDDHHMM)"
    print "-st Starting date and time\t\t(YYYYMMDDHHMM)"
    print "-et Ending date and time\t\t(YYYYMMDDHHMM)"
    print "-r radar or radars to process"
    print "-o Output directory to save data"
    print "-d Dry run, do not actually download data, lists what would be downloaded"
    print "-v Verbose, show lots of debugging info"
    
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def download(filepath, site):

    dataURL = "https://noaa-nexrad-level2.s3.amazonaws.com"
    print "Downloading %s" % (filepath)
    if(dry_run == 0):
        (dir,file) = os.path.split(filepath)
        local = open(os.path.join(output_dir,file),'wb')
        try:
            opener = urllib.URLopener()
            myfile = opener.open(os.path.join(dataURL,filepath))
        except:
            print "ERROR: Got a URL error: %s" % e
        local.write(myfile.read())
        local.close()
    
def getRadarData(site, stime, etime):

    date =  time.strftime("%Y/%m/%d", stime)
    starttime = time.mktime(stime)
    endtime = time.mktime(etime)
    bucketURL = "http://noaa-nexrad-level2.s3.amazonaws.com"
    dirListURL = bucketURL+ "/?prefix=" + date + "/" + site

    sys.stdout.write("listing files from dir %s/%s ... " % (date, site))
    sys.stdout.flush()
    #xmldoc = minidom.parse(stdin)
    xmldoc = minidom.parse(urlopen(dirListURL))
    itemlist = xmldoc.getElementsByTagName('Key')
    print len(itemlist) , "keys found"

    process = 0
    lastfiletime = 0
    lastfile = ""
    for x in itemlist:
        file = getText(x.childNodes)
        # Only process files that look like "2012/07/02/KJAX/KJAX20120702_030836_V06.gz"
        try:
            filetime = time.mktime((string.atoi(file[20:24]), string.atoi(file[24:26]), string.atoi(file[26:28]), string.atoi(file[29:31]), string.atoi(file[31:33]), string.atoi(file[33:35]), 0, 0, 0))
        except:
            continue

        if(verbose):
            print "%s  %s" % (file, filetime)
        if(process == 0 and starttime < filetime and endtime > lastfiletime):
            process = 1
            download(lastfile,site)
        if(endtime < filetime):
            process = 0

        if(process):
            download(file,site)
            
        lastfiletime = filetime
        lastfile = file
         
    
if __name__ == "__main__":
    
    stime = ""
    etime = ""
    radars = ""
    odir = ""
    
    # Process command args
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "dvht:s:e:r:o:")
    except:
        print "%s: error in parsing options, %s" % (sys.argv[0], sys.exc_value)
        usage(sys.argv[0])
        sys.exit(2)

    for i in xrange(0,len(optlist)):
        if optlist[i][0] == "-t":
            stime = optlist[i][1]
            if len(stime) != 12:
                print "%s: error - incorrect time format, use YYYYMMDDHHMM" % sys.argv[0]
                usage(sys.argv[0])
                sys.exit(2)
        elif optlist[i][0] == "-s":
            stime = optlist[i][1]
            if len(stime) != 12:
                print "%s: error - incorrect time format, use YYYYMMDDHHMM" % sys.argv[0]
                usage(sys.argv[0])
                sys.exit(2)
        elif optlist[i][0] == "-e":
            etime = optlist[i][1]
            if len(etime) != 12:
                print "%s: error - incorrect time format, use YYYYMMDDHHMM" % sys.argv[0]
                usage(sys.argv[0])
                sys.exit(2)
        elif optlist[i][0] == "-h":
            usage(sys.argv[0])
            sys.exit(2)
        elif optlist[i][0] == "-r":
            radars = optlist[i][1]
        elif optlist[i][0] == "-o":
            odir = optlist[i][1]
        elif optlist[i][0] == "-d":
            dry_run = 1
        elif optlist[i][0] == "-v":
            verbose = 1

    if(verbose):
        print "Verbose mode, Command line arguments:"
        print "Radars: %s" % radars
        print "StartTime: %s" % stime
        print "EndTime: %s" % etime
        if(odir != ''):
            print "OutputDir: %s" % odir
            
    if(radars == ''):
        print "Error - Must supply radar or radars to process"
        usage(sys.argv[0])
        sys.exit(2)
    if(stime == ''):
        print "Error - Must supply time to process"
        usage(sys.argv[0])
        sys.exit(2)
    if(odir != ''):
        if not os.path.isdir(odir):
            os.mkdir(odir)
        output_dir = odir

    try:
        starttime = (string.atoi(stime[:4]), string.atoi(stime[4:6]), string.atoi(stime[6:8]), string.atoi(stime[8:10]), string.atoi(stime[10:12]), 59, 0, 0, 0)
        if(etime == ''):
            endtime = (string.atoi(stime[:4]), string.atoi(stime[4:6]), string.atoi(stime[6:8]), string.atoi(stime[8:10]), string.atoi(stime[10:12]), 59, 0, 0, 0)
        else:
            endtime = (string.atoi(etime[:4]), string.atoi(etime[4:6]), string.atoi(etime[6:8]), string.atoi(etime[8:10]), string.atoi(etime[10:12]), 59, 0, 0, 0)
    except:
        print "Error - Time supplied does not match format YYYYMMDDHHMM "
        usage(sys.argv[0])
        sys.exit(2)

    if(verbose):
        print "StartTime: %d" % time.mktime(starttime)
        print "EndTime: %d" % time.mktime(endtime)
        
    for radar in radars.split(","):
        getRadarData(radar, starttime, endtime)

#!/usr/bin/env python

#=====================================================================
#
# Download NEXRAD radar files from AWS
#
#=====================================================================

from __future__ import print_function

import os
import sys
import time
import datetime
from datetime import timedelta

import string
import subprocess
from optparse import OptionParser

import urllib
from xml.dom import minidom
from sys import stdin
from urllib import urlopen
from subprocess import call

def main():

    global options
    global tmpDir
    global singleTime, startTime, endTime
    global doSingle, doInterval
    global fileCount

    # initialize file count

    fileCount = 0

    global thisScriptName
    thisScriptName = os.path.basename(__file__)

    # parse the command line

    parseArgs()
    
    # initialize
    
    beginString = "BEGIN: " + thisScriptName
    nowTime = datetime.datetime.now()
    beginString += " at " + str(nowTime)
    
    print("=============================================", file=sys.stderr)
    print(beginString, file=sys.stderr)
    print("=============================================", file=sys.stderr)

    # create dirs

    try:
        os.makedirs(options.tmpDir)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: cannot make tmp dir: ", options.tmpDir, file=sys.stderr)
            print("  ", exc, file=sys.stderr)
            
    try:
        os.makedirs(options.outputDir)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: cannot make output dir: ", options.outputDir, file=sys.stderr)
            print("  ", exc, file=sys.stderr)

    # actually get the data

    if (doSingle):
        # single time
        startDay = datetime.date(startTime.year, startTime.month, startTime.day)
        getForInterval(options.radarName, startDay, singleTime, singleTime)
    else:
        if (startTime.day == endTime.day):
            # single day
            startDay = datetime.date(startTime.year, startTime.month, startTime.day)
            getForInterval(options.radarName, startDay, startTime, endTime)
        else:
            # multiple days
            tdiff = endTime - startTime
            tdiffSecs = tdiff.total_seconds()
            if (options.debug):
                print("Proc interval in secs:  ", tdiffSecs, file=sys.stderr)
            startDay = datetime.date(startTime.year, startTime.month, startTime.day)
            endDay = datetime.date(endTime.year, endTime.month, endTime.day)
            thisDay = startDay
            while (thisDay <= endDay):
                if (options.debug):
                    print("===>>> processing day:  ", thisDay, file=sys.stderr)
                if (thisDay == startDay):
                    # get to end of start day
                    periodStart = startTime
                    periodEnd = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                                  23, 59, 59)
                    getForInterval(options.radarName, thisDay, periodStart, periodEnd)
                elif (thisDay == endDay):
                    # get from start of end day
                    periodStart = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                                    0, 0, 0)
                    periodEnd = endTime
                    getForInterval(options.radarName, thisDay, periodStart, periodEnd)
                else:
                    # get for the full day
                    periodStart = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                                    0, 0, 0)
                    periodEnd = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                                  23, 59, 59)
                    getForInterval(options.radarName, thisDay, periodStart, periodEnd)
                thisDay = thisDay + datetime.timedelta(1)
                
    print("---->> Num files downloaded: ", fileCount, file=sys.stderr)
        
    endString = "END: " + thisScriptName
    nowTime = datetime.datetime.now()
    endString += " at " + str(nowTime)
    
    print("==============================================", file=sys.stderr)
    print(endString, file=sys.stderr)
    print("==============================================", file=sys.stderr)

    sys.exit(0)

########################################################################
# Get the data for the specified time interval

def getForInterval(radarName, thisDay, startTime, endTime):

    # get the local file list, i.e. files already downloaded

    localFileList = getLocalFileList(thisDay, radarName)

    # construct the URL

    awsDateStr =  startTime.strftime("%Y/%m/%d")
    bucketURL = "http://noaa-nexrad-level2.s3.amazonaws.com"
    dirListURL = bucketURL+ "/?prefix=" + awsDateStr + "/" + radarName
    if (options.debug):
        print("dirListURL: ", dirListURL, file=sys.stderr)

    # get the listing in XML

    xmldoc = minidom.parse(urlopen(dirListURL))
    itemlist = xmldoc.getElementsByTagName('Key')
    if (options.debug):
        print("number of keys found: ", len(itemlist), file=sys.stderr)

    for x in itemlist:
        # Only process files that look like "2012/07/02/KJAX/KJAX20120702_030836_V06.gz"
        fileEntry = str(getNodeText(x.childNodes))
        try:
            (fyear, fmonth, fday, rname, fileName) = str.split(fileEntry, '/')
            if (options.verbose):
                print("==>> fyear, fmonth, fday, rname, fname: ",
                      fyear, fmonth, fday, rname, fileName, file=sys.stderr)
            year = int(fileName[4:8]);
            month = int(fileName[8:10]);
            day = int(fileName[10:12]);
            hour = int(fileName[13:15]);
            minute = int(fileName[15:17]);
            sec = int(fileName[17:19]);
            fileTime = datetime.datetime(year, month, day, hour, minute, sec);
        except:
            if(options.verbose):
                print("bad entry: ", fileEntry, file=sys.stderr)
            continue

        if(options.verbose):
            print("checking file, time: ", fileEntry, fileTime, file=sys.stderr)

        if(fileTime >= startTime and fileTime <= endTime):
            if (options.force):
                doDownload(radarName, fileTime, fileEntry, fileName)
            else:
                if (fileName not in localFileList):
                    doDownload(radarName, fileTime, fileEntry, fileName)
                elif (options.debug):
                    print("file previously downloaded: ", fileName, file=sys.stderr)
    
########################################################################
# Get text for nodes

def getNodeText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


########################################################################
# Download specified file

def doDownload(radarName, fileTime, fileEntry, fileName):

    global fileCount

    if (options.debug):
        print("Downloading entry, name: ",
              fileEntry, ", ", fileName, file=sys.stderr)

    if(options.dryRun):
        # no download
        return

    # download into tmp file

    dataURL = "https://noaa-nexrad-level2.s3.amazonaws.com"
    tmpPath = os.path.join(options.tmpDir, fileName)
    try:
        tmpFile = open(tmpPath, 'wb')
        opener = urllib.URLopener()
        myfile = opener.open(os.path.join(dataURL,fileEntry))
        tmpFile.write(myfile.read())
        tmpFile.close()
        fileCount = fileCount + 1
    except OSError as e:
        print("ERROR: Got error: ", e, file=sys.stderr)

    # create final dir

    dateStr =  fileTime.strftime("%Y%m%d")
    outDayDir = os.path.join(options.outputDir, dateStr)
    try:
        os.makedirs(outDayDir)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: trying to create dir: ", outDayDir, file=sys.stderr)
            print("Exception: ", exc, file=sys.stderr)
    
    # move to output dir
    
    cmd = "mv " + tmpPath + " " + outDayDir
    runCommand(cmd)

    # write latest_data_info
    
    timeStr = fileTime.strftime("%Y%m%d%H%M%S")
    relPath = os.path.join(dateStr, fileName)
    cmd = "LdataWriter -dir " + options.outputDir \
          + " -rpath " + relPath \
          + " -ltime " + timeStr \
          + " -writer " + thisScriptName \
          + " -dtype bufr"
    runCommand(cmd)

########################################################################
# Get list of files already downloaded

def getLocalFileList(date, radarName):

    # make the target directory and go there
    
    dateStr = date.strftime("%Y%m%d")
    localDayDir = os.path.join(options.outputDir, dateStr)
    try:
        os.makedirs(localDayDir)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: trying to create dir: ", localDayDir, file = sys.stderr)
            print("  exception: ", exc, file = sys.stderr)

    # get local file list - i.e. those which have already been downloaded
    
    os.chdir(localDayDir)
    localFileList = os.listdir(localDayDir)
    localFileList.reverse()

    if (options.verbose):
        print("==>> localFileList: ", localFileList, file=sys.stderr)

    return localFileList
            
########################################################################
# Parse the command line

def parseArgs():
    
    global options
    global singleTime, startTime, endTime
    global doSingle, doInterval

    # parse the command line

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option('--debug',
                      dest='debug', default=False,
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--verbose',
                      dest='verbose', default=False,
                      action="store_true",
                      help='Set verbose debugging on')
    parser.add_option('--radarName',
                      dest='radarName',
                      default='KFTG',
                      help='4-character name for radar')
    parser.add_option('--outputDir',
                      dest='outputDir',
                      default='/tmp/aws',
                      help='Path of output dir to which the files are written')
    parser.add_option('--tmpDir',
                      dest='tmpDir',
                      default='/tmp/stage',
                      help='Path of tmp dir for staging data')
    parser.add_option('--force',
                      dest='force', default=False,
                      action="store_true",
                      help='Force transfer even if file previously downloaded')
    parser.add_option('--dryRun',
                      dest='dryRun', default=False,
                      action="store_true",
                      help='Dry run: do not download data, list what would be downloaded')
    parser.add_option('--latest',
                      dest='getLatest', default=False,
                      action="store_true",
                      help='Get latest file')
    parser.add_option('--continuous',
                      dest='runContinuously', default=False,
                      action="store_true",
                      help='Run continuously - use with --latest')
    parser.add_option('--single',
                      dest='singleTime',
                      default='1970 01 01 00 00 00',
                      help='Single time for retrieval')
    parser.add_option('--start',
                      dest='startTime',
                      default='1970 01 01 00 00 00',

                      help='Start time for retrieval')
    parser.add_option('--end',
                      dest='endTime',
                      default='1970 01 01 00 00 00',
                      help='End time for retrieval')

    (options, args) = parser.parse_args()

    if (options.verbose):
        options.debug = True
        
    year, month, day, hour, minute, sec = options.singleTime.split()
    singleTime = datetime.datetime(int(year), int(month), int(day),
                                   int(hour), int(minute), int(sec))
    if (singleTime.year > 1970):
        doSingle = True
    else:
        doSingle = False
    
    year, month, day, hour, minute, sec = options.startTime.split()
    startTime = datetime.datetime(int(year), int(month), int(day),
                                  int(hour), int(minute), int(sec))
    
    year, month, day, hour, minute, sec = options.endTime.split()
    endTime = datetime.datetime(int(year), int(month), int(day),
                                int(hour), int(minute), int(sec))
    if (startTime.year > 1970 and endTime.year > 1970):
        doInterval = True
    else:
        doInterval = False
    
    if (options.debug):
        print("Options:", file=sys.stderr)
        print("  debug? ", options.debug, file=sys.stderr)
        print("  force? ", options.force, file=sys.stderr)
        print("  dryRun? ", options.dryRun, file=sys.stderr)
        print("  radarName: ", options.radarName, file=sys.stderr)
        print("  outputDir: ", options.outputDir, file=sys.stderr)
        print("  tmpDir: ", options.tmpDir, file=sys.stderr)
        print("  getLatest? ", options.getLatest, file=sys.stderr)
        print("  runContinuously? ", options.runContinuously, file=sys.stderr)
        print("  doSingle? ", doSingle, file=sys.stderr)
        print("  singleTime: ", singleTime, file=sys.stderr)
        print("  doInterval? ", doInterval, file=sys.stderr)
        print("  startTime: ", startTime, file=sys.stderr)
        print("  endTime: ", endTime, file=sys.stderr)

    if (doSingle == True and doInterval == True):
        print("ERROR - ", thisScriptName, file=sys.stderr)
        print("  Cannot set both single and start/end times", file=sys.stderr)
        sys.exit(1)

    if (options.getLatest == True and doSingle == True):
        print("ERROR - ", thisScriptName, file=sys.stderr)
        print("  Cannot set both latest and single modes", file=sys.stderr)
        sys.exit(1)

    if (options.getLatest == True and doInterval == True):
        print("ERROR - ", thisScriptName, file=sys.stderr)
        print("  Cannot set both latest and interval modes", file=sys.stderr)
        sys.exit(1)

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.debug):
        print("running cmd: ", cmd, file=sys.stderr)
    
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print("Child was terminated by signal: ", -retcode, file=sys.stderr)
        else:
            if (options.debug):
                print("Child returned code: ", retcode, file=sys.stderr)
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e

########################################################################
# kick off main method

if __name__ == "__main__":

   main()

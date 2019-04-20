#!/usr/bin/env python

#=====================================================================
#
# Download NEXRAD radar files from AWS
#
#=====================================================================

import os
import sys
import time
import datetime
from datetime import timedelta

import string
import ftplib
import subprocess
from optparse import OptionParser

import urllib
from xml.dom import minidom
from sys import stdin
from urllib import urlopen
from subprocess import call

def main():

    global options
    global ftpUser
    global ftpPassword
    global ftpDebugLevel
    global tmpDir
    global singleTime, startTime, endTime
    global doSingle, doInterval
    global count
    count = 0

    global thisScriptName
    thisScriptName = os.path.basename(__file__)

    # parse the command line

    parseArgs()
    sys.exit(0)
    
    # initialize
    
    beginString = "BEGIN: " + thisScriptName
    today = datetime.datetime.now()
    beginString += " at " + str(today)
    
    if (options.force):
        beginString += " (ftp forced)"

    print "\n========================================================"
    print beginString
    print "========================================================="

    # create tmp dir if necessary

    try:
        os.makedirs(options.tmpDir)
    except OSError as exc:
        if (options.verbose):
            print >>sys.stderr, "WARNING: cannot make tmp dir: ", options.tmpDir
            print >>sys.stderr, "  ", exc
            
    # set ftp debug level

    if (options.verbose):
        ftpDebugLevel = 2
    elif (options.debug):
        ftpDebugLevel = 1
    else:
        ftpDebugLevel = 0
    
    # get current date and time

    nowTime = time.gmtime()
    now = datetime.datetime(nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday,
                            nowTime.tm_hour, nowTime.tm_min, nowTime.tm_sec)
    nowDateStr = now.strftime("%Y%m%d")
    nowDateTimeStr = now.strftime("%Y%m%d%H%M%S")

    # compute time strings

    startDateTimeStr = startTime.strftime("%Y%m%d%H%M%S")
    startDateStr = startTime.strftime("%Y%m%d")
    endDateTimeStr = endTime.strftime("%Y%m%d%H%M%S")
    endDateStr = endTime.strftime("%Y%m%d")

    # set up list of days to be checked

    timeInterval = endTime - startTime
    if (options.debug):
        print >>sys.stderr, "  startTime: ", startTime
        print >>sys.stderr, "  endTime: ", endTime
        print >>sys.stderr, "  timeInterval: ", timeInterval
        print >>sys.stderr, "  nDays: ", timeInterval.days

    # loop through the hours

    thisTime = startTime
    while (thisTime <= endTime):
        if (options.debug):
            print >>sys.stderr, "  thisTime: ", thisTime
        thisTime = thisTime + timedelta(0, 3600, 0)
        try:
            getDataForHour(thisTime)
        except:
            print >>sys.stderr, "FTP failed"
        
    if (count == 0):
        print "---->> No files to download"
        
    print "==============================================================="
    print "END: " + thisScriptName + str(datetime.datetime.now())
    print "==============================================================="

    sys.exit(0)

########################################################################
# Get the data for a specified hour

def getDataForHour(dataTime):

    global count

    if (options.debug):
        print >>sys.stderr, "====>> getting data for time: ", dataTime
        print >>sys.stderr, "  year: ", dataTime.year
        print >>sys.stderr, "  month: ", dataTime.month
        print >>sys.stderr, "  day: ", dataTime.day
        print >>sys.stderr, "  hour: ", dataTime.hour

    # make the target directory and go there
    
    dateStr = dataTime.strftime("%Y%m%d")
    timeStr = dataTime.strftime("%Y%m%d%H%M%S")
    localDayDir = os.path.join(options.targetDir, dateStr)
    try:
        os.makedirs(localDayDir)
    except OSError as exc:
        if (options.verbose):
            print >>sys.stderr, "WARNING: trying to create dir: ", localDayDir
            print >>sys.stderr, "  ", exc
    os.chdir(localDayDir)

    # get local file list - i.e. those which have already been downloaded
    
    localFileList = os.listdir('.')
    localFileList.reverse()
    if (options.verbose):
        print >>sys.stderr, "  localFileList: ", localFileList
            
    # open ftp connection
    
    ftp = ftplib.FTP(options.ftpServer, options.ftpUser, options.ftpPasswd)
    ftp.set_debuglevel(ftpDebugLevel)

    # got to source directory on the ftp site

    hourStr = dataTime.strftime("%Y/%m/%d/%H")
    hourDir = options.sourceDir + "/" + hourStr

    if (options.debug):
        print >>sys.stderr, "====>> cd to hourDir: ", hourDir

    ftp.cwd(hourDir)

    # get list of volume times in this hour

    hourDirList = ftp.nlst()
    if (options.debug):
        print >>sys.stderr, "====>> times in this hour: ", dataTime
    
    # loop through the vol times

    for volTimeStr in hourDirList:
        
        # go there

        volDir = hourDir + "/" + volTimeStr

        if (options.debug):
            print >>sys.stderr, "  volTimeStr: ", volTimeStr
            print >>sys.stderr, "  volDir: ", volDir

        ftp.cwd(volDir)

        # get list of files

        fileList = ftp.nlst()

        # loop through file list, getting the BUFR files

        for fileName in fileList:
            if (fileName.find('BUFR') > 0):
                if (fileName not in localFileList):
                    downloadFile(ftp, dateStr, timeStr, fileName)
                    count = count + 1

    # close ftp connection
    
    ftp.quit()

########################################################################
# Download a file into the current directory

def downloadFile(ftp, dateStr, timeStr, fileName):
    
    if (options.debug):
        print >>sys.stderr, "  downloading file: ", fileName
        
    # get file, store in tmp

    tmpPath = os.path.join(options.tmpDir, fileName)

    if (options.verbose):
        print >>sys.stderr, "retrieving file, storing as tmpPath: ", tmpPath
    ftp.retrbinary('RETR '+ fileName, open(tmpPath, 'wb').write)

    # move to final location - i.e. this directory
    
    cmd = "mv " + tmpPath + " ."
    runCommand(cmd)

    # write latest_data_info
    
    relPath = os.path.join(dateStr, fileName)
    cmd = "LdataWriter -dir " + options.targetDir \
          + " -rpath " + relPath \
          + " -ltime " + timeStr \
          + " -writer " + thisScriptName \
          + " -dtype bufr"
    runCommand(cmd)

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
        print >>sys.stderr, "Options:"
        print >>sys.stderr, "  debug? ", options.debug
        print >>sys.stderr, "  force? ", options.force
        print >>sys.stderr, "  dryRun? ", options.dryRun
        print >>sys.stderr, "  radarName: ", options.radarName
        print >>sys.stderr, "  outputDir: ", options.outputDir
        print >>sys.stderr, "  tmpDir: ", options.tmpDir
        print >>sys.stderr, "  doSingle? ", doSingle
        print >>sys.stderr, "  singleTime: ", singleTime
        print >>sys.stderr, "  doInterval? ", doInterval
        print >>sys.stderr, "  startTime: ", startTime
        print >>sys.stderr, "  endTime: ", endTime

    if (doSingle == True and doInterval == True):
        print >>sys.stderr, "ERROR - ", thisScriptName
        print >>sys.stderr, "  Cannot set both single and start/end times"
        sys.exit(1)

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.debug):
        print >>sys.stderr, "running cmd:",cmd
    
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal: ", -retcode
        else:
            if (options.debug):
                print >>sys.stderr, "Child returned code: ", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

########################################################################
# kick off main method

if __name__ == "__main__":

   main()

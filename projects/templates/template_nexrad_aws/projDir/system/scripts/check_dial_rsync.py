#!/usr/bin/env python

# ========================================================================== #
#
# check rsync of DIAL data from field to server
#
# ========================================================================== #

import os
import sys
from optparse import OptionParser
import time
import datetime
from datetime import date
from datetime import timedelta
import subprocess
import smtplib

def main():

    global options
    global emailList

    # parse the command line

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option('--debug',
                      dest='debug',
                      default='False',
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--verbose',
                      dest='verbose',
                      default='False',
                      action="store_true",
                      help='Set verbose debugging on')
    parser.add_option('--dataDir',
                      dest='dataDir',
                      default='/export/eldora1/wvdial_1_data',
                      help='Data directory')
    parser.add_option('--emails',
                      dest='emails',
                      default='wvdial@ucar.edu',
                      help='Comma-delimited list of email addresses for warning messages')
    parser.add_option('--maxDelayMins',
                      dest='maxDelayMins',
                      default=12,
                      help='Max number of minutes delay in data arrival before warning')
    
    (options, args) = parser.parse_args()

    if (options.verbose == True):
        options.debug = True

    emailList = options.emails.split(",")

    if (options.debug == True):
        print >>sys.stderr, "Running: ", os.path.basename(__file__)
        print >>sys.stderr, "  Options:"
        print >>sys.stderr, "    Debug: ", options.debug
        print >>sys.stderr, "    Verbose: ", options.verbose
        print >>sys.stderr, "    dataDir: ", options.dataDir
        print >>sys.stderr, "    emails: ", options.emails
        print >>sys.stderr, "    emailList: ", emailList

    # get current time

    now = time.gmtime()
    nowTime = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday,
                                now.tm_hour, now.tm_min, now.tm_sec)

    # check if the latest data has updated

    exists, file, delta = check_dir(options.dataDir)
    max_delta = timedelta(minutes=int(options.maxDelayMins))
    sender = "rsfdata@eldora.eol.ucar.edu"

    missing_msg = """From: {0}
To: {1}
Subject: missing DIAL data 

{2} not found
"""
    stale_msg = """From: {0}
To: {1}
Subject: stale DIAL data 

{2} has not been updated for {3}
"""

    if exists:
	if delta < max_delta:
	    print('file {0} exists (and is up-to-date) '.format(file) )
	else:
	    print('file {0} is stale '.format(file))
	    hours, remainder = divmod(delta.total_seconds(), 3600)
	    minutes, seconds = divmod(remainder, 60)
	    dstr = "%02d:%02d:%02d" % (hours, minutes, seconds)
	    mail_warning(sender, emailList, 
		stale_msg.format(sender,",".join(emailList), file, dstr))
	
    else:
	print('file {0} is missing '.format(file))
	mail_warning(sender, emailList, 
		missing_msg.format(sender, ",".join(emailList), file) )
	
    sys.exit(0)

########################################################################
# Check directory for updates

def check_dir(dir, now=datetime.datetime.utcnow()):

    """ check if a data file exists with the correct name"""
    
    fname = now.strftime('%Y/%Y%m%d/MCSsample%H0000.nc')
    fullname = os.path.join(dir, fname)
    exists = os.path.exists(fullname)
    delta = timedelta(minutes = 99)
    if exists:
	delta =  now - datetime.datetime.fromtimestamp(os.path.getctime(fullname))
     
    return (exists, fullname, delta)

########################################################################
# email out a warning message

def mail_warning(sender, receivers, msg):
    try:
	smtp = smtplib.SMTP('localhost')
	print 'sending ', msg
	smtp.sendmail(sender, receivers, msg)
    except smtplib.SMTPException:
	print "Error: unable to send email"

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.debug == True):
        print >>sys.stderr, "running cmd:",cmd
    
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal: ", -retcode
        else:
            if (options.debug == True):
                print >>sys.stderr, "Child returned code: ", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

########################################################################
# Run - entry point

if __name__ == "__main__":
   main()


#!/usr/bin/env python

# ========================================================================== #
#
# Create links to the parameter files in the data tree template
#
# ========================================================================== #

import os
import sys
from optparse import OptionParser
import subprocess

def main():

    global options

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
    parser.add_option('--templateDir',
                      dest='templateDir', default="/tmp/templateDir",
                      help='Path of template - i.e. the directory tree template')
    parser.add_option('--installDir',
                      dest='installDir', default="/tmp/installDir",
                      help='Where the tree will be installed')
    (options, args) = parser.parse_args()
    
    if (options.verbose):
        options.debug = True

    # debug print

    if (options.debug):
        print >>sys.stderr, "Running script: ", os.path.basename(__file__)
        print >>sys.stderr, "  Options:"
        print >>sys.stderr, "    Debug: ", options.debug
        print >>sys.stderr, "    Verbose: ", options.verbose
        print >>sys.stderr, "    Template dir: ", options.templateDir
        print >>sys.stderr, "    Install dir: ", options.installDir

    # make the install dir

    try:
        os.makedirs(options.installDir)
    except OSError as exc:
        if (options.verbose):
            print >>sys.stderr, "WARNING: trying to create install dir"
            print >>sys.stderr, "  ", exc

    # Walk the template directory tree

    for dirPath, subDirList, fileList in os.walk(options.templateDir):
        for fileName in fileList:
            if (fileName[0] == '_'):
                handleParamFile(dirPath, fileName)

    sys.exit(0)

########################################################################
# Handle a parameter file entry

def handleParamFile(dirPath, paramFileName):

    if (options.debug):
        print >>sys.stderr, "Handling param file, dir, paramFile: ", \
            dirPath, ", ", paramFileName

    # compute sub dir

    subDir = dirPath[len(options.templateDir):]

    # compute install sub dir

    installSubDir = options.installDir + subDir

    if (options.debug):
        print >>sys.stderr, "subDir: ", subDir
        print >>sys.stderr, "installSubDir: ", installSubDir

    # make the install sub dir and go there

    try:
        os.makedirs(installSubDir)
    except OSError as exc:
        pass

    os.chdir(installSubDir)

    # remove the link if it exists

    if (os.path.exists(paramFileName)):
        os.remove(paramFileName)

    # create the link

    paramFilePath = os.path.join(options.templateDir + subDir, paramFileName)
    cmd = "ln -s " + paramFilePath
    runCommand(cmd)

    return

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.verbose == True):
        print >>sys.stderr, "running cmd:",cmd
    
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal: ", -retcode
        else:
            if (options.verbose == True):
                print >>sys.stderr, "Child returned code: ", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

########################################################################
# Run - entry point

if __name__ == "__main__":
   main()

#!/usr/bin/env python

# ========================================================================== #
#
# Configure the project, install relevant files
#
# Run from within: git/lroae-titan
# Requires ~/git/lrose-core to be checkout out.
#
# ========================================================================== #

from __future__ import print_function

import os
import sys
from optparse import OptionParser
import datetime
import subprocess
import string

def main():

    global options

    homeDir = os.environ['HOME']
    projDir = os.path.join(homeDir, 'projDir')
    controlDir = os.path.join(projDir, 'control')
    titanGitDir = os.path.join(homeDir, "git/lrose-titan")
    coreGitDir = os.path.join(homeDir, "git/lrose-core")

    # parse the command line
    
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option('--debug',
                      dest='debug', default=True,
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--dataDir',
                      dest='dataDir', default='/data/titan',
                      help='Path of installed data dir')
    (options, args) = parser.parse_args()
    
    # compute paths

    gitProjDir = os.path.join(titanGitDir, 'projects/nexrad_multiple/projDir')
    gitSystemDir = os.path.join(gitProjDir, 'system')
    
    # debug print

    print("Running script: ", os.path.basename(__file__), file=sys.stderr)
    print("", file=sys.stderr)
    print("  Options:", file=sys.stderr)
    print("    Debug: ", options.debug, file=sys.stderr)
    print("    homeDir: ", homeDir, file=sys.stderr)
    print("    projDir: ", projDir, file=sys.stderr)
    print("    controlDir: ", controlDir, file=sys.stderr)
    print("    titanGitDir: ", titanGitDir, file=sys.stderr)
    print("    coreGitDir: ", coreGitDir, file=sys.stderr)
    print("    gitProjDir: ", gitProjDir, file=sys.stderr)
    print("    gitSystemDir: ", gitSystemDir, file=sys.stderr)
    print("    dataDir: ", options.dataDir, file=sys.stderr)
    
    # banner

    print(" ")
    print("*********************************************************************")
    print("  configure project - NEXRAD multiple")
    print("  runtime: " + str(datetime.datetime.now()))
    print("  dataDir: " + options.dataDir)
    print("*********************************************************************")
    print(" ")

    # check that the git dirs exist

    if (os.path.exists(titanGitDir) == False):
        print("ERROR - titanGitDir: ", titanGitDir, " does not exist.", file=sys.stderr)
        print("  You must check this out into the home directory, as follows:", file=sys.stderr)
        print("    mkdir ~/git", file=sys.stderr)
        print("    cd ~/git", file=sys.stderr)
        print("    git clone https://github.com/lrose-titan", file=sys.stderr)
        sys.exit(1)

    if (os.path.exists(coreGitDir) == False):
        print("ERROR - coreGitDir: ", coreGitDir, " does not exist.", file=sys.stderr)
        print("  You must check this out into the home directory, as follows:", file=sys.stderr)
        print("    mkdir ~/git", file=sys.stderr)
        print("    cd ~/git", file=sys.stderr)
        print("    git clone https://github.com/lrose-core", file=sys.stderr)
        sys.exit(1)

    # make links to the dotfiles in git projDir
    
    os.chdir(homeDir)
    for rootName in ['cshrc', 'emacs', 'Xdefaults' ]:
        dotName = '.' + rootName
        removeSymlink(homeDir, dotName)
        sourceDir = os.path.join(gitSystemDir, 'dotfiles')
        sourcePath = os.path.join(sourceDir, rootName)
        cmd = "ln -s " + sourcePath + " " + dotName
        runCommand(cmd)

    # make link to projDir

    removeSymlink(homeDir, 'projDir')
    os.chdir(homeDir)
    cmd = "ln -s " + gitProjDir
    runCommand(cmd)

    # install runtime scripts from lrose into projDir/lrose

    os.chdir(coreGitDir + "/codebase/apps/scripts/src")
    cmd = "install_scripts.lrose " + homeDir + "/projDir/lrose/scripts"
    runCommand(cmd)
    
    #os.chdir(coreGitDir + "/codebase/apps/procmap/src/scripts")
    #cmd = "install_scripts.lrose " + homeDir + "/projDir/lrose/scripts"
    #runCommand(cmd)
    
    os.chdir(coreGitDir + "/codebase/libs/perl5/src")
    cmd = "install_perl5.lrose " + homeDir + "/projDir/lrose/lib/"
    runCommand(cmd)
    
    ############################################
    # create data directory
    
    installDataDir = os.path.join(options.dataDir, 'data')
    print("Install data dir: ", installDataDir, file=sys.stderr)
    cmd = "mkdir -p " + installDataDir
    runCommand(cmd)

    # create symlink to data

    os.chdir(projDir)
    removeSymlink(projDir, "data")
    if (os.path.exists('data') == False):
        cmd = "ln -s " + installDataDir
        runCommand(cmd)

    # create symlink to logs

    os.chdir(projDir)
    removeSymlink(projDir, "logs")
    if (os.path.exists('logs') == False):
        cmd = "ln -s data/logs"
        runCommand(cmd)

    # done

    sys.exit(0)
    
########################################################################
# Remove a symbolic link
# Exit on error

def removeSymlink(dir, linkName):

    os.chdir(dir)

    # remove if exists
    if (os.path.islink(linkName)):
        os.unlink(linkName)
        return

    if (os.path.exists(linkName)):
        # link name exists but is not a link
        print("ERROR - trying to remove symbolic link", file=sys.stderr)
        print("  dir: ", dir, file=sys.stderr)
        print("  linkName: ", linkName, file=sys.stderr)
        print("This is NOT A LINK", file=sys.stderr)
        print("Please move this file out of the way: ~/" + linkName, file=sys.stderr)
        sys.exit(1)

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.debug):
        print("running cmd:",cmd, file=sys.stderr)

    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal: ", -retcode
        else:
            if (options.debug):
                print("Child returned code: ", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)

########################################################################
# Run - entry point

if __name__ == "__main__":
   main()

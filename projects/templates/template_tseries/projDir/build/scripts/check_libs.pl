#!/usr/bin/perl
#
# check_libs: Check installed libraries
#
# Usage:
#   daily_backup.pl <options>
#
#    Options:
#       -help                : Print usage
#       -debug               : debugging on
#       -host_type           : host type
#       -list                : check list
#
#===================================================================================
# Get the needed PERL supplied library modules.
#===================================================================================

require 'getopts.pl';
use Getopt::Long;                                                                           
use Time::Local;#

#===================================================================================
# Set up the needed environment variables
#===================================================================================

use Env qw(RAP_LIB_DIR);

#
# Get the program basename.
#

($prog = $0) =~ s|.*/||;

#
# Unbuffer standard output
#

$| = 1;

#set flushing

$OUTPUT_AUTOFLUSH = 1;

#
# Set file permissions
#

umask 002;

# Initialize command line arguments

$opt_debug = "";
$opt_params = "";
$opt_host_type = "unknown";

$usage =
    "\nUsage: $prog <options>\n" .
    "Options:\n" .
    "  -help                 :Print usage\n" .
    "  -dir                  :lib dir (required)\n" .
    "  -host_type            :host type\n" .
    "  -list                 :lib check list (required)\n" .
    "  -debug                :debugging on\n" .
    "\n";

# Get the arguments from the command line

$results = &GetOptions('help',
                       'dir:s',
                       'host_type:s',
                       'list:s',
                       'debug');

if ($opt_help) {
    print $usage;
    exit 0;
}

if (!$opt_list) {
    print "\nERROR - you must specify the lib list\n";
    print $usage;
    exit 0;
}

if (!$opt_dir) {
    print "\nERROR - you must specify the lib dir\n";
    print $usage;
    exit 0;
}

# read in the list of installed libs, from the lib directory

opendir(DIRHANDLE, $opt_dir) || die "Cannot open dir: $opt_dir: $!";
$count = 0;
foreach $name (sort readdir(DIRHANDLE)) {
    if ($name =~ m/.a$/) {
        @installed_libs[$count] = $name;
        $count++;
    }
}
closedir(DIRHANDLE);

if ($opt_debug) {
    printf STDERR "======= INSTALLED LIBS =====\n";
    foreach $lib (@installed_libs) {
        print STDERR "$lib\n";
    }
    print STDERR "============================\n";
}

# read in list of required libs, from check list

open(CHECKLIST, "< $opt_list") || die("can't open $opt_list: $!");
$count = 0;
while(($name = <CHECKLIST>)) {
    chop($name);
    if (!($name =~ m/^\#/)) {
        @required_libs[$count] = $name;
        $count++;
    }
}
close(CHECKLIST);

if ($opt_debug) {
    printf STDERR "======= REQUIRED LIBS =====\n";
    foreach $lib (@required_libs) {
        print STDERR "$lib\n";
    }
    print STDERR "============================\n";
}

# find libs which are not installed

$nmiss = 0;
foreach $rlib (@required_libs) {
    $found = 0;
    foreach $ilib (@installed_libs) {
        if ($ilib eq $rlib) {
            $found = 1;
            break;
        }
    }
    if (!$found) {
        @missing_libs[$nmiss] = $rlib;
        $nmiss++;
    }
}

# if libs are missing, print out error message

if ($nmiss > 0) {
    foreach $mlib (@missing_libs) {
        printf STDERR "  Library \'$mlib\' missing\n";
    }
    printf STDERR "Number of missing libraries: $nmiss\n";
    printf STDERR "===================>> ERROR <<====================\n";
    printf STDERR "===>> INCOMPLETE CP2 TITAN LIB INSTALLATION <<====\n";
    printf STDERR "====>> Host type: $opt_host_type <<=====\n";
    exit 1;
} else {
    printf STDERR "==================>> SUCCESS <<====================\n";
    printf STDERR "========>> ALL CP2 TITAN LIBS INSTALLED <<=========\n";
    printf STDERR "====>> Host type: $opt_host_type <<=====\n";
    exit 0;
}

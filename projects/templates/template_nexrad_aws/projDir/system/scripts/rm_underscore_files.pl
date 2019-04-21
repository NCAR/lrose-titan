#! /usr/bin/perl
#
# rm_underscore_files
#
# Remove files in data tree which begin with underscore,
# except for _latest_data_info files.
#
# =================================================================

#------------------------------- Set defaults --------------------------
#
# External modules

use Getopt::Long;
use Env;

# Get program name

($script = $0) =~ s%.*/%%;

# Usage statement

$usage=
  "Purpose: To remove underscore files in data tree.\n" .
  "Usage : $script [options as below ...]\n" .
  "Options:\n" .
  "  [-dir ?] specify top dir, default is /data/spol/data\n" .
  "  [-h] print usage\n" .
  "  [-debug] set debug mode on\n" .
  "  [-verbose] set verbose debug mode on\n";

# Initialize

$help = 0;
$debug = 0;
$verbose = 0;
$top_dir = "/data/spol/data";

#------------------------- Save command line for later -------------------

$command_line = "$script";
foreach $arg (@ARGV) {
  $command_line = $command_line . " $arg";
}

#------------------------- Parse command line ----------------------------

&GetOptions("h!" => \$help,
	    "debug!" => \$debug,
	    "verbose!" => \$verbose,
	    "dir=s" => \$top_dir);

if ($help) {
  print $usage;
  exit 0;
}

if ($verbose) {
    $debug = 1;
}

if ($debug) {
  print STDERR "=========>>>> Running script $script ================\n";
  print STDERR "  top_dir: $top_dir\n";
}

# recursively process all directories in the data tree

&processDir($top_dir);

exit 0;

#---------------------------------------------------------------------------
#
# Subroutine: processDir
#

sub processDir {

    local($dir) = @_;
    local($path, $entry);

    if ($verbose) {
	printf STDERR "Processing dir: $dir\n";
    }
    
# open directory
    
    opendir(DIR, $dir);
    my @files = readdir DIR;
    closedir(DIR);

    foreach $entry (@files) {
	
	# ignore . and ..
	
	if ($entry eq "." || $entry eq "..") {
	    next;
	}
	
	# compute path
	
	$path = "$dir/$entry";

	# if a directory, call recursively

	if (-d $path) {
	    &processDir($path);
	    next;
	}
	
	# if a file, check whether to remove
	
	if (-f $path) {

	    $remove = 0;

	    if ($entry =~ /^_DsMdvServer/) {
		$remove = 1;
	    } elsif ($entry =~ /^_DsSpdbServer/) {
		$remove = 1;
	    } elsif ($entry =~ /2Symprod/) {
		$remove = 1;
	    } elsif ($entry =~ /^_Janitor/) {
		$remove = 1;
	    } elsif ($entry =~ /^_janitor/) {
		$remove = 1;
	    } elsif ($entry =~ /^_Scout/) {
		$remove = 1;
	    } elsif ($entry =~ /^_DsFileDist/) {
		$remove = 1;
	    }

	    if ($remove) {
		if ($debug) {
		    printf STDERR "---> removing file: $path\n";
		}
		unlink($path);
	    }

	}

    } # while
    
    if ($verbose) {
	printf STDERR "Done with dir: $dir\n";
    }

}

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
  "Purpose: To selectively remove time series files.\n" .
  "Usage : $script [options as below ...]\n" .
  "Options:\n" .
  "  [-h] print usage\n" .
  "  [-debug] set debug mode on\n" .
  "  [-verbose] set verbose debug mode on\n";

# Initialize

$help = 0;
$debug = 0;
$verbose = 0;
$data_dir =  $ENV{'DATA_DIR'};

#------------------------- Save command line for later -------------------

$command_line = "$script";
foreach $arg (@ARGV) {
  $command_line = $command_line . " $arg";
}

#------------------------- Parse command line ----------------------------

&GetOptions("h!" => \$help,
	    "debug!" => \$debug,
	    "verbose!" => \$verbose);

if ($help) {
  print $usage;
  exit 0;
}

if ($verbose) {
    $debug = 1;
}

if ($debug) {
  print STDERR "=========>>>> Running script $script ================\n";
}

# get sizes of main directories

$sunscanSize = getDirSize("$data_dir/tsarchive/sunscan");
$stationarySize = getDirSize("$data_dir/tsarchive/stationary");
$vertSize = getDirSize("$data_dir/tsarchive/vert");
$saveSize = getDirSize("$data_dir/tsarchive/save");

print "\n";
print "Enter directory from which to delete data:\n\n";
print "  sunscan    (size: $sunscanSize)\n";
print "  vert       (size: $vertSize)\n";
print "  save       (size: $saveSize)\n";
print "  stationary (size: $stationarySize)\n";
print "  all\n";
print "\n";
$main_action = &promptUser("  Enter your choice (return for no action)");
print "\n";

if ($main_action eq "") {

  exit 0;

} elsif ($main_action eq "all") {

  deleteFromDir("$data_dir/tsarchive/sunscan");
  deleteFromDir("$data_dir/tsarchive/vert");
  deleteFromDir("$data_dir/tsarchive/save");
  deleteFromDir("$data_dir/tsarchive/stationary");

} elsif ($main_action eq "sunscan") {

  deleteFromDir("$data_dir/tsarchive/sunscan");

} elsif ($main_action eq "vert") {

  deleteFromDir("$data_dir/tsarchive/vert");

} elsif ($main_action eq "save") {

  deleteFromDir("$data_dir/tsarchive/save");

} elsif ($main_action eq "stationary") {

  deleteFromDir("$data_dir/tsarchive/stationary");

} else {

  print STDERR "ERROR - choice not valid\n";
  print STDERR "  No data will be deleted\n";
  exit 255;

}

exit 0;

#----------------------------(  getDirSize  )-----------------------------#
#                                                                         #
#  PURPOSE:	Get size of data in a directory, as a string              #
#                                                                         #
#  ARGS:	$dir - directory in question                              #
#                                                                         #
#  Returns:	$sizestr- string showing size                             #
#                                                                         #
#-------------------------------------------------------------------------#

sub getDirSize {

   local($dir) = @_;

   $duStr = `du -sh $dir`;
   ($sizeStr, $path) = split(/\s/, $duStr);

   return $sizeStr;

}

#----------------------------(  deleteFromDir ) --------------------------#
#                                                                         #
#  PURPOSE:	Delete data from specified dir                            #
#                                                                         #
#  ARGS:	$dir - directory in question                              #
#                                                                         #
#-------------------------------------------------------------------------#

sub deleteFromDir {

   local($dir) = @_;
   local($ii, @subDirs, @paths, @sizes, $dirToDelete);

#  find date sub-directories

   @subDirs = getSubDirs($dir);

   if ($#subDirs < 0) {
     print "NOTE: no data in dir: $dir\n";
     return;
   }
   
   print "---------------------------------------------------------------\n";
   print "Deleting data from dir: $dir\n";

   for ($ii = 0; $ii <= $#subDirs; $ii++) {
     @paths[$ii] = "${dir}/$subDirs[$ii]";
     @sizes[$ii] = getDirSize(@paths[$ii]);
   }
   
   print "\n";
   print "Enter date directories to be deleted:\n\n";
   for ($ii = 0; $ii <= $#subDirs; $ii++) {
     print "  $subDirs[$ii]: (size @sizes[$ii])\n";
   }
   print "  all\n";
   
   print "\n";
   $dirToDelete = &promptUser("  Enter your choice (return for no action)");
   print "\n";

   if ($dirToDelete eq "") {

     return;

   } elsif ($dirToDelete eq "all") {

     foreach $path (@paths) {
       deleteDir($path);
     }

   } else {

     $path = "${dir}/$dirToDelete";
     deleteDir($path);
     
   }
   
}

#----------------------------(  deleteDir ) ------------------------------#
#                                                                         #
#  PURPOSE:	Delete specified dir                            #
#                                                                         #
#-------------------------------------------------------------------------#

sub deleteDir {
  
  local($dir) = @_;
  system("/bin/rm -rf $dir");
  print "==>> $dir: deleted!\n";
  
}

#---------------------------------------------------------------------------
#
# Subroutine: getSubDirs
#

sub getSubDirs {

    local($dir) = @_;
    local($path, $entry);
    $count = 0;

#   open directory
    
    opendir(DIR, $dir);
    my @files = readdir DIR;
    closedir(DIR);
    
    foreach $entry (@files) {

#     ignore . and ..
      
      if ($entry eq "." || $entry eq "..") {
	next;
      }
      
#     compute path
      
      $path = "$dir/$entry";
      
#     if a directory, add to list
      
      if (-d $path) {

	$subDirs[$count] = $entry;
	$count++;
	next;
      }
      
    }
	
    return @subDirs;

}

#----------------------------(  promptUser  )-----------------------------#
#                                                                         #
#  FUNCTION:	promptUser                                                #
#                                                                         #
#  PURPOSE:	Prompt the user for some type of input, and return the    #
#		input back to the calling program.                        #
#                                                                         #
#  ARGS:	$promptString - what you want to prompt the user with     #
#		$defaultValue - (optional) a default value for the prompt #
#                                                                         #
#-------------------------------------------------------------------------#

sub promptUser {

   #-------------------------------------------------------------------#
   #  two possible input arguments - $promptString, and $defaultValue  #
   #  make the input arguments local variables.                        #
   #-------------------------------------------------------------------#

   local($promptString,$defaultValue) = @_;

   #-------------------------------------------------------------------#
   #  if there is a default value, use the first print statement; if   #
   #  no default is provided, print the second string.                 #
   #-------------------------------------------------------------------#

   if ($defaultValue) {
      print $promptString, "[", $defaultValue, "]: ";
   } else {
      print $promptString, ": ";
   }

   $| = 1;               # force a flush after our print
   $_ = <STDIN>;         # get the input from STDIN (presumably the keyboard)


   #------------------------------------------------------------------#
   # remove the newline character from the end of the input the user  #
   # gave us.                                                         #
   #------------------------------------------------------------------#

   chomp;

   #-----------------------------------------------------------------#
   #  if we had a $default value, and the user gave us input, then   #
   #  return the input; if we had a default, and they gave us no     #
   #  no input, return the $defaultValue.                            #
   #                                                                 # 
   #  if we did not have a default value, then just return whatever  #
   #  the user gave us.  if they just hit the <enter> key,           #
   #  the calling routine will have to deal with that.               #
   #-----------------------------------------------------------------#

   if ("$defaultValue") {
      return $_ ? $_ : $defaultValue;    # return $_ if it has a value
   } else {
      return $_;
   }
}



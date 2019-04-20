#!/usr/bin/perl
#
# FTP ops image files
#
# Mike Dixon, RAP, NCAR, Boulder, CO, USA
# Feb 2008
#

# system Perl modules

use Net::FTP;
use Time::Local;
use Getopt::Long;
 
#
# RAP Perl modules
#

use Env qw(RAP_INST_LIB_DIR);
use lib "$RAP_INST_LIB_DIR/perl5/";
use Procmap;
use Toolsa;

$debug = 0;                              # Ordinary debugging flag.
$verbose = 0;                            # Verbose debugging flag.
$proj_dir = $ENV{'PROJ_DIR'};

#------------------------- Parse command line ----------------------------

($prog = $0) =~ s%.*/%%;                 # Determine program basename.
&GetOptions("unix_time=s" => \$unix_time,
	    "year=s" => \$year,
	    "month=s" => \$month,
	    "day=s" => \$day,
	    "hour=s" => \$hour,
	    "min=s" => \$min,
	    "sec=s" => \$sec,
            "debug!" => \$debug,
            "verbose!" => \$verbose,
	    "rap_data_dir=s" => \$rap_data_dir,
	    "full_path=s" => \$full_path,
	    "abs_dir_path=s" => \$abs_dir_path,
	    "sub_dir=s" => \$sub_dir,
	    "rel_dir=s" => \$rel_dir,
	    "file_ext=s" => \$file_ext,
	    "data_type=s" => \$data_type,
	    "user_info1=s" => \$user_info1,
	    "user_info2=s" => \$user_info2,
	    "is_forecast=s" => \$is_forecast,
	    "forecast_lead_secs=s" => \$forecast_lead_secs,
	    "writer=s" => \$writer,
	    "data_late_secs=s" => \$data_late_secs,
	    "rel_data_path=s" => \$rel_data_path);

$orig_dir = $full_path;
$file_name = $rel_data_path;
$xml_name = $file_name;
$xml_name =~ s/png/xml/;

$data_path = $orig_dir . '/' . $file_name;
$xml_path = $orig_dir . '/' . $xml_name;
$day_str = sprintf "%.4d%.2d%.2d", $year, $month, $day;
$time_str = sprintf "%.4d%.2d%.2d%.2d%.2d%.2d", $year, $month, $day, $hour, $min, $sec;

if ($debug) {
    print STDERR "Running ftp_snapshot_files:\n";
    print STDERR "  orig_dir: $full_path\n";
    print STDERR "  file_name: $file_name\n";
    print STDERR "  data_path: $data_path\n";
    print STDERR "  xml_path: $xml_path\n";
    print STDERR "  day_str: $day_str\n";
    print STDERR "  time_str: $time_str\n";
}


#------------------------- initialize ----------------------------

$| = 1;                           # Unbuffer standard output.
umask 002;                        # Set file permissions.
$ftp_timeout = 60;                # Max time for single file transfer

# --------------- move the files to a day dir  -----------------------

$day_dir = $orig_dir . '/' . $day_str;
$data_path_moved = $day_dir . '/' . $file_name; 
$xml_path_moved = $day_dir . '/' . $xml_name; 

if ($debug) {
    print STDERR "Moving files to day dir: $day_dir\n";
 }
system("mkdir -p $day_dir");
system("/bin/mv $data_path $day_dir");
system("/bin/mv $xml_path $day_dir");

#----------------- send files to NCAR ------------------------------

#$ftp_host = "ftp.rap.ucar.edu"; 
#$ftp_host = "cp2server"; 
#$user = "anonymous";       # The remote username.
#$passwd = "dixon\@ucar.edu";      # The remote password.
#$targetdir = "incoming/irap/Queensland/images/radar/${day_str}"; # The remote target data directory.

#&send_file($ftp_host, $user, $passwd, $targetdir);

#----------------- send files to QLAND govt ------------------------

$ftp_host = "cloudseed.nrw.qld.gov.au"; 
$user = "dixonm";       # The remote username.
$passwd = "dr0ught!";      # The remote password.
$targetdir = "RadarQuickImages/MergedComposite/${day_str}"; # The remote target data directory.
&send_file($ftp_host, $user, $passwd, $targetdir);

exit 0;

# --------------------------------------------------------------------
# send_file function: Send file to remote host
# Arg: host

sub send_file {

  local($ftp_host, $user, $passwd, $targetdir) = @_;
  local($ftp);
  
  if ($debug) {
    print STDERR "Sending: ftp_host: $ftp_host\n";
    print STDERR "         user: $user\n";
    print STDERR "         passwd: $passwd\n";
    print STDERR "         targetdir: $targetdir\n";
    print STDERR "         file: $data_path_moved\n";
  }
  
  $ftp = Net::FTP->new($ftp_host, Passive=>true, Timeout=>$ftp_timeout);
  if (!$ftp) {
    print STDERR "ftp-new failure\n";
    return;
  }
  if ($ftp->login($user, $passwd) == 0) {
    print STDERR "ftp-login failure, user: $user, password: $pass\n";
    $ftp->quit;
    return;
  }
  
  $ftp->mkdir($targetdir,"true");
  
  if ($ftp->cwd($targetdir) == 0) {
    print STDERR "ftp-cwd failure\n";
    $ftp->quit;
    return;
  }
  
  $ftp->binary;
  
  if ($ftp->put($data_path_moved, $file_name) != 0) {
    print STDERR "ftp-put failure\n";
    $ftp->quit;
    return;
  }
  
  $ftp->quit;
  
  if ($debug) {
    print STDERR "-->> success\n";
  }
  
}


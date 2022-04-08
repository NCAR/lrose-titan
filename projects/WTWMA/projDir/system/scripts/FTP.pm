# Net::FTP.pm
#
# Copyright (c) 1995 Graham Barr <Graham.Barr@tiuk.ti.com>. All rights
# reserved. This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.

package Net::FTP;

=head1 NAME

FTP - implements FTP Client

=head1 SYNOPSIS

use Net::FTP;

$ftp = Net::FTP->new(<host>,[port]);

=head1 DESCRIPTION

This package provides a class object which can be used for connecting to remote
FTP servers and transfering data.

=head2 NOTE: C<This Documentation is VERY incomplete>

=cut

require 5.001;
use Socket;
use Carp;

sub Version { sprintf("%d.%02d", q$Revision: 1.2 $ =~ /(\d+)\.(\d+)/) }

BEGIN {

 # format to pack to build argment for socket call
 $sockaddr = 'S n a4 x8';

 $socksym = "ftp00000";
}

##
## Really WANT FileHandle::new to return this !!!
##
sub gensym {\*{"FTP::Net::" . $socksym++}}

sub new {
 my $pkg  = shift;
 my $host = shift;
 my $port = shift;
 my($destaddr, $destproc, $me);
 my $sock = gensym();

 if($host =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/) {
  $destaddr = pack('C4', $1, $2, $3, $4);
 }
 else {
  $destaddr = (gethostbyname($host))[4] or
    carp "Cannot get IP address of '$host'" and return undef;
 }

 # get ftp port; I'll use getservbyname, but assume port 21 if it fails
 $port = (getservbyname("ftp", "tcp"))[2] || 21 unless(defined $port);

 $destproc = pack($sockaddr, AF_INET, $port, $destaddr);

 # get protocol number for tcp, assume 6 if getprotobyname fails
 my $tcp = (getprotobyname("tcp"))[2] || 6;

 if(socket($sock, AF_INET, SOCK_STREAM, $tcp)) {
  if(connect($sock, $destproc)) {

   my $cmdaddr = (unpack ($sockaddr, getsockname($sock)))[2];
   my $cmdname = pack($sockaddr, AF_INET, 0, $cmdaddr);

   $me = {
          SOCK    => $sock,     # Command socket connection
          LISTEN  => undef,     # Listen socket
          DATA    => undef,     # Data socket

          CmdAddr => $cmdaddr,  # Address of command socket
          CmdName => $cmdname,  # name of command socket

          Type    => 'A',       # Ascii/Binary/etc mode
          Timeout => 55,        # Timeout value
          Resp    => [],        # Last response text
          Code    => 0,         # Last response code
          Debug   => 0          # Output debug information
         };

   bless $me, $pkg;

   select((select($sock), $| = 1)[$[]);

   $me->response();
  }
 }

 $me;
}

##
## User interface methods
##

=item * debug( [1|0] )

Turn the printing of debug information on/off for this object. If no
argument is given then the current state is returned. Otherwise the
state is changed and the previous state returned.

=cut

sub debug {
 my $me = shift;
 my $debug = $me->{Debug};
 
 $me->{Debug} = 0 + shift if(@_);

 $debug;
}

=item * quit

Send the QUIT command to the remote FTP server and close the socket connection.

=cut

sub quit {
 my $me = shift;

 return undef unless($me->QUIT);

 close($me->{SOCK});
 delete $me->{SOCK};

 return 1;
}

=item * ascii/ebcdic/binary/byte

Put the remote FTP server ant the FTP package into the given mode
of data transfer.

=cut

sub ascii  { shift->type('A',@_); }
sub ebcdic { shift->type('E',@_); }
sub binary { shift->type('I',@_); }
sub byte   { shift->type('L',@_); }

# Allow the user to send a command directly, BE CAREFUL !!
sub quot  { shift->cmd( uc shift, @_) }

=item * login([user], [password], [account])

Log onto the remote FTP server with the given information or
with the defaults 

     user = anonymous
 password = your email address
  account =

Returns 0 on failure

=cut

sub login {
 my $me = shift;
 my $user = shift || "anonymous";
 my $pass = shift || "-" . $ENV{USER} . "@";
 my $acct = shift || "";
 my $ok;

 $ok = $me->USER($user)
  and $ok == 3 and $ok = $me->PASS($pass)
  and $ok == 3 and $ok = $me->ACCT($acct);

 $ok == 2;
}

sub authorise {
 my($me,$auth,$resp) = @_;
 my $ok;

 carp "Net::FTP::authorise <auth> <resp>\n"
   unless(defined $auth && defined $resp);

 $ok = $me->AUTH($auth)
  and $ok == 3 and $ok = $me->RESP($resp);

 $ok == 2;
}

=item * rename( <oldname>, <newname> )

Rename a file on the remote FTP server from C<oldname> to C<newname>

Returns undef on failure

=cut

sub rename {
 my($me,$from,$to) = @_;

 croak "Net::FTP:rename <from> <to>\n"
   unless(defined $from && defined $to);

 $me->RNFR($from)
  and $me->RNTO($to)
  or return undef;
}

sub get {
 my $me = shift;
 my $remote = shift;
 my $local  = shift;
 my $timeout = $me->{Timeout};
 my($rin,$rout,$len,$but,$partial,$data,$loc);

 $data = $me->retr($remote);

 return undef unless(fileno($data));

 ($local = $remote) =~ s#^.*/## unless(defined $local);

 if(ref($local) && fileno($local)) {
  $loc = $local;
 }
 else {
  $loc = gensym();
  open($loc,">$local") or 
   carp "Cannot open Local file $local: $!\n" and
   return undef;
 }

 $partial = "";

 vec($rin,fileno($data),1) = 1;
 while(1) {
  if(($timeout == 0) || select($rout=$rin, undef, undef, $timeout)) {
   last unless($len=sysread($data,$buf,1024));
   if($me->{Type} eq 'A') { 
    substr($buf,0,0)=$partial;      ## prepend from last sysread
    @buf=split(/\r?(?=\n)/,$buf);   ## break into lines
    $partial = (substr($buf, -1, 1) eq "\n") ? '' : pop(@buf);
    print $loc @buf;
   }
   else {
    last unless ( (syswrite($loc,$buf,$len)==$len) );
   }
  }
  else {
   carp "Net::FTP::get $!";
   return undef;
  }
 }
 print $loc $partial if(length($partial));

 close($loc) unless(ref($local) && fileno($local));
 close($data);
 $me->response() == 2;
}

sub cwd {
 my $me = shift;
 my $dir = shift || "/";

 return ($dir eq "..") ? $me->CDUP() : $me->CWD($dir);
}

sub put        { shift->send("stor",@_) }
sub put_unique { shift->send("stou",@_) }
sub append     { shift->send("appe",@_) }

sub type {
 my $me   = shift;
 my $type = shift;
 my $ok   = 0;

 return $me->{Type} unless defined $type;

 return undef unless($me->TYPE($type,@_));

 $me->{Type} = join(" ",$type,@_);
}

sub nlst { shift->data_cmd("NLST",@_) }
sub list { shift->data_cmd("LIST",@_) }
sub retr { shift->data_cmd("RETR",@_) }
sub stor { shift->data_cmd("STOR",@_) }
sub stou { shift->data_cmd("STOU",@_) }
sub appe { shift->data_cmd("APPE",@_) }

sub port {
 my $me = shift;
 my $port = shift;
 my $ok;

 unless(defined $port) {
  my $listen;

  if(defined $me->{LISTEN}) {
   $listen = $me->{LISTEN};
  }
  else {
   $listen = gensym();
  
   socket($listen, AF_INET, SOCK_STREAM, PROTO_TCP)
     and bind($listen, $me->{CmdName})
     and listen($listen,1)
     or return undef;
  
   select((select($listen), $| = 1)[0]);
  
   $me->{LISTEN} = $listen;
  }
  
  my($fam, $myport, @myaddr) = unpack('S n C C C C x8', getsockname($listen));

  $port = join(',', @myaddr, $myport >> 8, $myport & 0xff);
 }

 $ok = $me->PORT($port);

 $me->{Port} = $port;

 $ok;
}

sub ls  { shift->list_cmd("NLST",@_); }
sub lsl { shift->list_cmd("LIST",@_); }

sub pasv {
 my $me = shift;
 my $hostport;

 return undef unless $me->PASV();

 ($hostport) = $me->message =~ /(\d+(,\d+)+)/;

 $me->{Pasv} = $hostport;
 return $hostport;
}

##
## Communication methods
##

sub cleanup {
 my $me = shift;

 if(defined $me->{LISTEN}) {
  close($me->{LISTEN}) if(ref($me->{LISTEN}) && fileno($me->{LISTEN}));
  undef $me->{LISTEN};
 }
 if(defined $me->{DATA}) {
  close($me->{DATA}) if(ref($me->{DATA}) && fileno($me->{DATA}));
  undef $me->{DATA};
 }

 return shift; # Allow caller to pass return value
}

sub timeout {
 my $me = shift;
 my $timeout = $me->{Timeout};

 $me->{Timeout} = 0 + shift if(@_);

 $timeout;
}

sub send {
 my $me     = shift;
 my $cmd    = shift;
 my $local  = shift;
 my $remote = shift;
 my $infd = 0;
 my($loc,$sock);

 $infd = fileno($local) if(ref($local));

 unless(defined $remote) {
  croak "Must specify remote filename with stream input\n" if($infd);

  ($remote = $local) =~ s%.*/%%;
 }

 $cmd = lc $cmd;

 $sock = $me->$cmd($remote);
 return $me->cleanup() unless fileno($sock);

 if($infd) {
  $loc = $local;
 }
 else {
  $loc = gensym();

  open($loc,"<$local") or 
   carp "Cannot open Local file $local: $!\n" and
   return $me->cleanup();
 }

 if($me->{Type} eq 'A') { # Ascii
  while(<$loc>) {
   s/\n\Z/\r\n/;
   print $sock $_;
  }
 }
 else {
  my($len,$buf);

  do {
   $len = sysread($loc,$buf,1024);
  } while($len && syswrite($sock,$buf,$len) == $len);
 }

 close($loc) unless($infd);

 $me->cleanup();
 $me->response();

 ($remote) = $me->message =~ /unique file name:\s*(\S*)\s*\)/
    if($cmd eq 'stou');

 return $remote;
}

sub accept {
 my $me = shift;
 my $data = gensym();
 
 return undef unless defined $me->{LISTEN};

 unless(accept($data,$me->{LISTEN})) {
  carp "Cannot accept data connetion: $!\n";
  close($data);
  return undef;
 }

 close($me->{LISTEN});
 delete $me->{LISTEN};

 $me->{DATA} = $data;
}

sub message {
 my $me = shift;
 join("\n", @{$me->{Resp}});
}

sub ok {
 my $me = shift;
 my $code = $me->{Code} || 0;

 0 < $code && $code < 400;
}

sub list_cmd {
 my $me = shift;
 my $cmd = lc shift;
 my $data = $me->$cmd(@_);
 my $partial = "";
 my $timeout = $me->{Timeout} || 0;
 my($rin,$rout,$buf,$list);

 $list = [];

 vec($rin,fileno($data),1) = 1;

 while(1) {
  if(($timeout == 0) || select($rout=$rin, undef, undef, $timeout)) {

   last unless($len=sysread($data,$buf,1024));

   substr($buf,0,0)=$partial;      ## prepend from last sysread

   push(@{$list}, split(/\r?\n/,$buf));   ## break into lines

   $partial = (substr($buf, -1, 1) eq "\n") ? ''
                                            : pop(@{$list});
  }
  else {
   carp "Net::FTP::list_cmd Timeout";
   return $me->cleanup();
  }
 }

 push(@{$list}, $partial) if(length($partial));

 $me->cleanup();
 $me->response();

 wantarray ? @{$list} : $list;
}

sub data_cmd {
 my $me = shift;
 my $ok = 1;
 my $pasv = defined $me->{Pasv} ? 1 : 0;
 my $cmd = uc shift;

 $ok = $me->port unless($pasv || defined $me->{Port});
 $ok = $me->$cmd(@_) if($ok);

 return $ok ? ($pasv ? 1 : $me->accept()) : undef;
}

sub cmd {
 my $me = shift;
 my $sock = $me->{SOCK};


 if(scalar(@_)) {     
  my $cmd = join(" ", @_);

  delete $me->{Pasv};
  delete $me->{Port};

  print $sock $cmd,"\r\n";

  printf STDERR "$me>> %s\n", $cmd=~/^(pass|resp)/i ? "$1 ...." : $cmd
     if($me->debug);
 }
 $me->response();                                          
}

sub pasv_wait {
 my $me = shift;
 my $non_pasv = shift;
 my $sock = $me->{SOCK};
 my($rin,$rout,$file);

 vec($rin,fileno($sock),1) = 1;
 while(1) {
  last if select($rout=$rin, undef, undef, 120);
 }

 $me->response();
 $non_pasv->response();

 return undef unless($me->ok() && $non_pasv->ok());

 return $1 if($me->message =~ /unique file name:\s*(\S*)\s*\)/);
 return $1 if($non_pasv->message =~ /unique file name:\s*(\S*)\s*\)/);

 return 1;
}

sub response {
 my $me = shift;
 my $sock = $me->{SOCK};
 my $timeout = $me->{Timeout};
 my($code,@resp,$rin,$rout,$partial,@buf,$buf);

 vec($rin,fileno($sock),1) = 1;
 $more = 0;
 @resp = ();
 $partial = '';

 do {
  if (($timeout==0) || select($rout=$rin, undef, undef, $timeout)) {

   unless(sysread($sock, $buf, 1024)) {
    carp "Unexpected EOF on command channel";
    return undef;
   } 

   substr($buf,0,0) = $partial;    ## prepend from last sysread

   @buf = split(/\r?\n/, $buf);  ## break into lines

   $partial = (substr($buf, -1, 1) eq "\n") ? ''
                                            : pop(@buf); 

   foreach $cmd (@buf) {
    print STDERR "$me<< $cmd\n" if($me->debug);

    ($code,$more) = ($1,$2) if $cmd =~ /^(\d\d\d)(.)/;
    push(@resp,$');
   } 
  } 
  else {
   carp "$me: Timeout" if($me->debug);
   return undef;
  }
 } while(length($partial) || (defined $more && $more eq "-"));

 $me->{Code} = $code;
 $me->{Resp} = [ @resp ];

 substr($code,0,1);
}


##
## RFC959 commands
##

sub no_imp { croak "Not implemented\n"; }

sub ABOR { shift->cmd("ABOR")     == 2}
sub ALLO { no_imp; }
sub DELE { shift->cmd("DELE", @_) == 2}
sub CWD  { shift->cmd("CWD",  @_) == 2}
sub CDUP { shift->cmd("CDUP")     == 2}
sub SMNT { no_imp; }
sub HELP { no_imp; }
sub MODE { no_imp; }
sub NOOP { shift->cmd("NOOP")     == 2}
sub PASV { shift->cmd("PASV")     == 2}
sub QUIT { shift->cmd("QUIT")     == 2}
sub SITE { no_imp; }
sub PORT { shift->cmd("PORT", @_) == 2}
sub SYST { no_imp; }
sub STAT { no_imp; }
sub RMD  { shift->cmd("RMD",  @_) == 2}
sub MKD  { shift->cmd("MKD",  @_) == 2}
sub PWD  { shift->cmd("PWD",  @_) == 2}
sub STRU { no_imp; }
sub TYPE { shift->cmd("TYPE", @_) == 2}

sub APPE { shift->cmd("APPE", @_) == 1}
sub LIST { shift->cmd("LIST", @_) == 1}
sub NLST { shift->cmd("NLST", @_) == 1}
sub REIN { no_imp; }
sub RETR { shift->cmd("RETR", @_) == 1}
sub STOR { shift->cmd("STOR", @_) == 1}
sub STOU { shift->cmd("STOU", @_) == 1}

sub RNFR { shift->cmd("RNFR", @_) == 3}
sub RNTO { shift->cmd("RNTO", @_) == 2}
sub REST { no_imp; }

sub USER { my $ok = shift->cmd("USER",@_);($ok == 2 || $ok == 3) ? $ok : 0;}
sub PASS { my $ok = shift->cmd("PASS",@_);($ok == 2 || $ok == 3) ? $ok : 0;}
sub ACCT { shift->cmd("ACCT", @_) == 2}

sub AUTH { my $ok = shift->cmd("AUTH",@_);($ok == 2 || $ok == 3) ? $ok : 0;}
sub RESP { shift->cmd("RESP", @_) == 2}

=back

=head2 AUTHOR

Graham Barr <Graham.Barr@tiuk.ti.com>

=head2 REVISION

$Revision: 1.2 $

=head2 COPYRIGHT

Copyright (c) 1995 Graham Barr. All rights reserved. This program is free
software; you can redistribute it and/or modify it under the same terms
as Perl itself.

=cut

1;


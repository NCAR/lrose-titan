#!/usr/bin/perl
#
#

$incr = 5;
$max = 200;

$lo = 0;
$hi = $lo+$incr;

while($hi < $max) {
   print("$lo\t$hi\tred\n");
   $lo += $incr;
   $hi += $incr;
}

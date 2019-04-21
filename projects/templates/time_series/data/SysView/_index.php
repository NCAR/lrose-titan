<?php /////////////////////////////////////////////////
// _index.php : Lookup the latest SysView master html file
//  via the _latest_data_info file and forward to it.
//
// F. Hage NCAR/RAP Jan 2002


// Check to make sure the _latest_data_info file is OK.
$error_cond = FALSE;
if(($stat_ret = stat("_latest_data_info")) == FALSE) {
   $error_cond = TRUE;

} else {  // _latest_data_info file does  exist

 // Check to see if file is older than 22 minutes (1320 secs)
 if($stat_ret[8] < (time() - 1320)) $error_cond = TRUE;

  // Open the _latest_data_info file in the local dir.
  $fp =  fopen("_latest_data_info","r");

  $count = 0;
  // Skip over 3 lines - Read the forth
  while($count < 4) {
    $buffer = fgets($fp,256);
     $count++;
  
  }
  fclose($fp);
  // The forth line contains the file name
  $latest_file = $buffer;
}

// No errors found
if($error_cond == FALSE ) { ?>

<HTML>
 <HEAD>
    <meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
    <!-- immediately refresh (forward) to the latest SysView Output -->
    <meta http-equiv="refresh" content="0;URL=<?echo($latest_file);?>">
 </HEAD>

<BODY>

<!-- Slow browsers will flash this briefly -->
<H1> Forwarding to <?php echo($latest_file);?> </H1>
<BODY>

</HTML> 

<?php  // Errors have been found - Do not forward - Display Warnings.
       } else {  ?> 

<HTML>
 <HEAD>
    <meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
    <!-- refresh (forward) to this file after 30 seconds -->
    <meta http-equiv="refresh" content="30;URL=_index.php">
 </HEAD>

<BODY BGCOLOR="red"> <CENTER>

<? // If there is a latest data info file, it's just too old
   if($latest_file) {   ?>

  <H1> Warning: SysView Output Older than Normal. Check the SysView Host </H1>
  <H2> <A HREF="<?echo($latest_file);?>"> Link to Last Sysview Output </A> </H3>

<? // No latest data info file 
   } else { ?>

  <H1> Warning: SysView Output Not Available. Check the SysView Host </H1>

<? }  ?> 
</CENTER>
</BODY>
</HTML> 

<?php } // End of Error Block  ?> 

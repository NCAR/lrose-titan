# Runtime environment for a TITAN project

## Use csh as the login shell

For TITAN projects to work properly, it is important that you use the 
c-shell (csh or tcsh) as your login shell.

You will set up the required environment variables in your .cshrc file.

## Check out lrose-titan and lrose-core

You should check lrose-titan from git into a ```git``` sub-directory in your
home directory.

You should also check out lrose-core.

```
  mkdir ~/git
  cd ~/git
  git clone https://github.com/ncar/lrose-titan 
  git clone https://github.com/ncar/lrose-core 
```

## Installing the TITAN applications

The TITAN applications are part of the LROSE - the Lidar Radar Open Software Environment.

The LROSE core code can be found at [lrose-core](https://github.com/NCAR/lrose-core).

The TITAN applications should be compiled and installed following the
[documentation](https://github.com/NCAR/lrose-core/blob/master/README.md) for the core.

## LROSE scripts

In addition to the TITAN application binaries, there are a number of scripts in LROSE
that are required to run TITAN.

These are found in:

```
  ~/git/lrose-core/codebase/apps/scripts/src
  ~/git/lrose-core/codebase/apps/procmap/src/scripts
```

Support Perl modules for these scripts are found in:

```
  ~/git/lrose-core/codebase/libs/perl5/src/
```

## PATH

In your .cshrc file, you need to set up your ```path``` to include the required scripts.

The following is an example from a .cshrc file, which you can use as a starting point.

```
set path = (.)

if ( -d $PROJ_DIR ) then
  foreach dir ($PROJ_DIR/*)
    if (-d $dir/scripts) then
      set path = ($path $dir/scripts)
    endif
  end
endif

set path = ($path $LROSE_INSTALL_DIR/bin)  

set path = ($path $HOME/git/lrose-core/codebase/apps/scripts/src)  
set path = ($path $HOME/git/lrose-core/codebase/apps/procmap/src/scripts)  

set path = ($path ~/bin \
        ~/anaconda2/bin \
	/usr/local/bin /usr/local/sbin /usr/bin/X11 \
        /usr/sbin /usr/bin /sbin /bin /usr/X11R6/bin \
	/opt/gfortran/irun/bin /opt/spol/bin /opt/local/lrose/bin )
```

## PROJ_DIR

The ```$PROJ_DIR``` environment variable points to the top of your project directory.

Generally this will look something like:

```
  ~/projDir
  ~/projDir/control
  ~/projDir/system/scripts
  ~/projDir/system/params
  ~/projDir/ingest/scripts
  ~/projDir/ingest/params
  ~/projDir/titan/scripts
  ~/projDir/titan/params
  ~/projDir/display/scripts
  ~/projDir/display/params
  etc. etc.
```
## DATA_DIR

The ```$DATA_DIR``` environment variable points to the top of your data directory tree.

## Example .cshrc files

The following .cshrc files are used by the project templates:

```
  ~/git/lrose-titan/projects/single_radar/projDir/system/dotfiles/cshrc
  ~/git/lrose-titan/projects/nexrad_single/projDir/system/dotfiles/cshrc
  ~/git/lrose-titan/projects/nexrad_multiple/projDir/system/dotfiles/cshrc
```


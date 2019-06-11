# TITAN project for single radar test - installation

The project allows you to simulate realtime data from a single radar.

## Setting up your environment

It is important that you use the c-shell (csh or tcsh) as your login shell.

## Check out lrose-titan

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

## Installing the project from the template

Relative to the top of the template, the script is:

```
  projDir/system/scripts/configureProject.py
```

To run it, cd to the ```projDir/system/scripts``` directory, and run it from
there:

```
  cd projDir/system/scripts
  ./configureProject.py
```

## Directories and links

The script creates a number of links, and populates the data tree as
appropriate:

```
  ~/projDir -> ~/git/lrose-titan/projects/nexrad_single/projDir
  ~/.cshrc -> ~/git/lrose-titan/projects/nexrad_single/projDir/system/dotfiles/cshrc
  ~/projDir/data -> /data/titan/data
  ~/projDir/logs -> /data/titan/data/logs
```

Also, configureProject.py will copy the required scripts from lrose-core into
```~/projDir/lrose```. These are required for run-time support.

```
  rsync -av ~/git/lrose-core/codebase/apps/scripts/src/* ~/projDir/lrose/scripts
  rsync -av ~/git/lrose-core/codebase/apps/procmap/src/scripts/* ~/projDir/lrose/scripts
  rsync -av ~/git/lrose-core/codebase/libs/perl5/src/*pm ~/projDir/lrose/libs/perl5
```

## Setting up the environment

The project-specific information is set in the following file:

```
  ~/projDir/system/params/project_info
```

This file sets environment variables. It is sourced by the .cshrc file.

You should edit this file as appropriate.

It is important that you use the c-shell (csh or tcsh) as your login shell.

## Running

After you have made changes, source the .cshrc file:

```
  source ~/.cshrc
```

Then, use ```start_all``` and ```stop_all``` to start and stop the project.

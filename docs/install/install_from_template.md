# Installing a TITAN project from a template

Templates for the scripts and parameter files reside here: in this [lrose-titan
respository](../../projects).

## Check out lrose-titan

You should check lrose-titan from git into a ```git``` sub-directory in your
home directory. You should also check out lrose-core.

```
  mkdir ~/git
  cd ~/git
  git clone https://github.com/ncar/lrose-titan 
  git clone https://github.com/ncar/lrose-core 
```

## Available templates

 The there are 3 main templates available in this lrose-titan repository:

* [Single radar test](../../projects/single_radar) 
* [Single NEXRAD radar](https://github.com/NCAR/lrose-titan/tree/master/projects/nexrad_single) 
* [Multiple NEXRAD radars](https://github.com/NCAR/lrose-titan/tree/master/projects/nexrad_multiple) 

## Installing from a template

In each template there is a script to assist with the install.

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

The script creates a number of links, and populates the data tree as
appropriate.

As an example, for the NEXRAD single project:

```
  ~/projDir -> ~/git/lrose-titan/projects/nexrad_single/projDir
  ~/.cshrc -> ~/git/lrose-titan/projects/system/dotfiles/cshrc
  ~/projDir/data -> /data/titan/data
  ~/projDir/logs -> /data/titan/data/logs

```

Also, configureProject.py will copy the required scripts from lrose-core into
```~/projDir/lrose```.

```
  rsync -av ~/git/lrose-core/codebase/apps/scripts/src/* ~/projDir/lrose/scripts
  rsync -av ~/git/lrose-core/codebase/apps/procmap/src/scripts/* ~/projDir/lrose/scripts
  rsync -av ~/git/lrose-core/codebase/libs/perl5/src/*pm ~/projDir/lrose/libs/perl5
```

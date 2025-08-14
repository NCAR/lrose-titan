# TITAN tutorial for AMS 2025

## Input data

There are 2 cases for use in the Titan tutorial:

* A hail storm in Alberta, observed by the Strathmore radar 40 km east Calgary.
* A derecho event in Ontario, observed by the King City radar 40 km north of Toronto.

Both of these are 10 cm (S-band) Gematronik dual polarization radars.

The data (as a .tgz file) can be downloaded from Mike's Google drive at NCAR:

* [AMS Titan data](https://drive.google.com/drive/folders/1OzjLzsGhSBAKDvFzJeBLGHYW0RlYU0hZ?usp=sharing)

To be consistent, you should create a ```$HOME/data``` directory and copy the .tgz file there.

Then:

```
  tar xvfz ams2025_titan.raw.tgz
```

That will create the following tree:

```
  ~/data/ams2025/ERA5/20220521
  ~/data/ams2025/ERA5/20240806
  ~/data/ams2025/radar/raw/hail/20240806*.h5
  ~/data/ams2025/radar/raw/derecho/20220521*.h5
```

## Output data

After the full analysis has been run, the following derived data directories should exist:

```
  ~/data/ams2025/ERA5/spdb/Strathmore/20240806* (soundings from ERA5)
  ~/data/ams2025/ERA5/spdb/KingCity/20220521* (soundings from ERA5)
  ~/data/ams2025/radar/cfradial/no_qc/Strathmore/20240806/cfrad.20240806*nc (cfradial before QC)
  ~/data/ams2025/radar/cfradial/no_qc/KingCity/20220521/cfrad.20220521*nc (cfradial before QC)
  ~/data/ams2025/radar/cfradial/qc/Strathmore/20240806/cfrad.20240806*nc (cfradial after QC)
  ~/data/ams2025/radar/cfradial/qc/KingCity/20220521/cfrad.20220521*nc (cfradial after QC)
  ~/data/ams2025/radar/cfradial/pid/Strathmore/20240806/cfrad.20240806*nc (cfradial PID)
  ~/data/ams2025/radar/cfradial/pid/Strathmore/20240806/cfrad.20240806*nc (cfradial PID)
  ~/data/ams2025/radar/cart/qc/Strathmore/20240806/ncf_20240806*nc (Cartesian MDC CF-compliant netcdf)
  ~/data/ams2025/radar/cart/qc/KingCity/20220521/ncf_202205216*nc (Cartesian MDC CF-compliant netcdf)
  ~/data/ams2025/titan/storms/Strathmore/20240806* (Titan binary files)
  ~/data/ams2025/titan/storms/KingCity/20220521* (Titan binary files)
  ~/data/ams2025/titan/ascii/Tracks2Ascii.hail.txt (Titan output converted by Tracks2Ascii)
  ~/data/ams2025/titan/ascii/Tracks2Ascii.derecho.txt (Titan output converted by Tracks2Ascii)
  ~/data/ams2025/titan/netcdf/Strathmore/titan_20240806.nc (Titan output converted by Tstorms2NetCDF)
  ~/data/ams2025/titan/netcdf/KingCity/titan_20220521.nc (Titan output converted by Tstorms2NetCDF)
```

## Checking out the project

The Titan project for AMS2025 is stored in the GitHub repo NCAR/lrose-titan.
This is also the location of this README file.

To check it out run:

```
  mkdir -p ~/git
  cd ~/git
  git clone https://github.com/ncar/lrose-titan
```

The structure of the ams2025 part of this repo is as follows:

```
  ~/git/lrose-titan/projects/ams2025/params
  ~/git/lrose-titan/projects/ams2025/scripts
  ~/git/lrose-titan/projects/ams2025/color_scales
  ~/git/lrose-titan/projects/ams2025/maps
```

## Setting up the environment

In the scripts directory you will find the file:

```
  ~/git/lrose-titan/projects/ams2025/scripts/set_env_vars
```

This file setup up the environment, and is sourced by all of the scripts that we run for this project.

The default contents are as follows:

```
  setenv DATA_DIR $HOME/data/ams2025
  setenv PROJ_DIR $HOME/git/lrose-titan/projects/ams2025
```

The default settings work as is, if you have followed these instructions.

If you have a different layout, edit ```set_env_vars``` appropriately.

## Processing steps, running the scripts

You should run the scripts from the script directory:

```
  cd ~/git/lrose-titan/projects/ams2025/scripts
```

### Convert raw HDF5 files with no QC

```
  ./run_RadxConvert.no_qc.hail
  ./run_RadxConvert.no_qc.derecho
```

This converts the raw HDF5 data into cfradial, with no QC steps applied.

We have, however, added the signal-to-noise (SNR) field, as derived from the reflectivity field DBZ. SNR is needed for later QC steps.

You can view the results using HawkEye:

```
  ./run_HawkEye.no_qc.hail
  ./run_HawkEye.no_qc.derecho
```

You will notice that in the derecho case there is considerable interference, leading to radial spikes.

Hail case - no significant interference:

![Alt text](./images/hail.dbz.no_qc.png)

Derecho case - considerable interference:

![Alt text](./images/derecho.dbz.no_qc.png)

### Convert raw HDF5 files with QC

Inspection of the spikes reveals that the sources of the interference are not coherent with the radars:

* SQI (NCP) is low
* SNR is reasonably low

In ```RadxConvert``` we have the option to censor the data fields using threshold applied to the input fields. Specifically we use RadxConvert to remove data at gates for which BOTH:

* SQI (NCP) < 0.2, AND
* SNR < 25 dB


The following runs that step:

```
  ./run_RadxConvert.qc.hail
  ./run_RadxConvert.qc.derecho
```

You can view the results in HawkEye, and compare to the non-QC step above.

```
  ./run_HawkEye.qc.hail
  ./run_HawkEye.qc.derecho
```

Hail case - clean:

![Alt text](./images/hail.dbz.qc.png)

Derecho case - interference largely mitigated:

![Alt text](./images/derecho.dbz.qc.png)

Although not perfect, for the purposes of this project, this censoring QC step is sufficent to ensure that Titan does not produce artifacts.

## Computing PID as an alternative method of censoring

An alternative method for cleaning up interference is to run RadxPid, and censor non-meteorological echoes.

We downloaded the ERA5 reanalysis for these cases, and we can use that to save the model-based soundings:

```
  ./run_Mdv2SoundingSpdb.ERA5.hail
  ./run_Mdv2SoundingSpdb.ERA5.derecho
```

And we can then run RadxPid:

```
  ./run_RadxPid.hail
  ./run_RadxPid.derecho
```

The following shows the PID field for the derecho case:

![Alt text](./images/derecho.pid.png)

The interference is identifed as clutter in this case.

And the following shows the result of using PID to clean up the reflectivity field:

![Alt text](./images/derecho.dbz.censored_by_pid.png)

For this tutorial we will use the QC data created by RadxConvert.

## Transform the polar data to Cartesian, using Radx2Grid.

Titan requires input data in Cartesian coordinates, rather than polar.

To perform this transformation, we run the following:


```
  ./run_Radx2Grid.hail
  ./run_Radx2Grid.derecho
```

On a Linux host, we can run CIDD to view the Cartesian fields, in addition to the polar fields:


```
  ./run_CIDD.hail
  ./run_CIDD.derecho
```

Cartesian DBZ data in CIDD, hail case:

<img src="./images/hail.dbz.cart.cidd.png" alt="Alt text" width="600">

Cartesian DBZ data in CIDD, derecho case:

<img src="./images/derecho.dbz.cart.cidd.png" alt="Alt text" width="600">

On a Mac or Linux we can run Lucid, the replacement for CIDD that is under development:

```
  ./run_Lucid.hail
  ./run_Lucid.derecho
```

Cartesian DBZ data in Lucid, hail case:

<img src="./images/hail.dbz.cart.lucid.png" alt="Alt text" width="600">

Cartesian DBZ data in Lucid, derecho case:

<img src="./images/derecho.dbz.cart.lucid.png" alt="Alt text" width="600">

As mentioned, Lucid is still under development and only some of the functionality is available. You can select fields, zooms and maps. The height selector is functional. The movie control slider works, for selecting different times. However, much of the time controller is not yet working.

## Running Titan

Titan runs on the Cartesian gridded data, using the DBZ field and optionally the VEL field to compute storm rotation.

```
  ./run_Titan.hail
  ./run_Titan.derecho
```

You can view the Titan tracks using Rview, which has a partner application TimeHist:

```
  ./run_Rview.hail
  ./run_Rview.derecho
```

Rview is a display application specifically designed to display Titan. We will need to demonstrate the interactive functionality. Rview on the mac seems to be crashing, so that will need to be debugged.

Rview and TimeHist, hail case:

<img src="./images/Rview.hail.png" alt="Alt text" width="600">

![Alt text](./images/Rview.and.TimeHist.hail.png)

Rview and TimeHist, derecho case:

<img src="./images/Rview.derecho.png" alt="Alt text" width="600">

![Alt text](./images/Rview.and.TimeHist.derecho.png)

## Exporting the Titan tracks using Tracks2Ascii

Tracks2Ascii exports the Titan track data in space-delimited ascii format:

```
  ./run_Tracks2Ascii.hail
  ./run_Tracks2Ascii.derecho
```

## Exporting the Titan tracks using Tstorms2NetCDF

Tstorms2NetCDF exports the Titan track data in NetCDF-4, using groups:

```
  ./run_Tstorms2NetCDF.hail
  ./run_Tstorms2NetCDF.derecho
```

For documentation on the NetCDF data model, see:

* [Titan Data in NetCDF](../../docs/pdf/TitanDataNetCDF.pdf)








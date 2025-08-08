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

## Processing steps

### convert raw HDF5 files with no QC

```
run_RadxConvert.no_qc.hail
run_RadxConvert.no_qc.derecho
```

### convert raw HDF5 files with QC

```
run_HawkEye.no_qc.hail
run_HawkEye.no_qc.derecho
```

```
run_RadxConvert.qc.hail
run_RadxConvert.qc.derecho
```

```
run_HawkEye.qc.hail
run_HawkEye.qc.derecho
```

```
run_Radx2Grid.hail
run_Radx2Grid.derecho
```

```
run_Mdv2SoundingSpdb.ERA5.hail
run_Mdv2SoundingSpdb.ERA5.derecho
```

```
run_RadxPid.hail
run_RadxPid.derecho
```

```
run_CIDD.hail
run_CIDD.derecho
```

```
run_Lucid.hail
run_Lucid.derecho
```

```
run_Titan.hail
run_Titan.derecho
```

```
run_Rview.hail
run_Rview.derecho
```

```
run_Tracks2Ascii.hail
run_Tracks2Ascii.derecho
```

```
run_Tstorms2NetCDF.hail
run_Tstorms2NetCDF.derecho
```






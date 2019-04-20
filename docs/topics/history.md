![header with logo](../images/titan-header_logo.jpg)

[Top](../../README.md)
[Back](./cloud_seeding_analysis.md)
[Fwd](./acknowledgements.md)

# History

TITAN version 1.0 was developed in the early 1980s. The initial goal was to evaulate the effectiveness of a rainfall-enhancement experiment carried out at Nelspruit in the lowveld of the Eastern Transvaal of South Africa. The experiment was funded by the South African Water Research Commission (WRC) and conducted by CloudQuest Corp. CloudQuest and the WRC provided the funding for the early development of TITAN. This original version was written in FORTRAN IV for a Data General Eclipse computer. The radar in use was a PACER-III 5-cm research non-Doppler digital radar built by Colorado International Corporation. Using volume-scan radar data, storms were identified in polar coordinates and tracked using a heuristic algorithm developed by Gordon Mader of the South African Council for Scientific and Industrial Research (CSIR). During the 1980's and early 1990's, TITAN version 1 was used in South Africa to evaluate a number of rainfall-enhancement projects. 

In the early 1990's, the development of TITAN moved to the Research Applications Program (RAP) of the National Center for Atmospheric Research (NCAR) in Boulder, Colorado. Primary funding was provided by the Federal Aviation Administration (FAA). The goal was to adapt TITAN for a thunderstorm forecasting role for aviation. In the late 1990's the statistical package for weather modification evaluation was enhanced in support of the Program for Augmentation of Rainfall in Coahuila, an NCAR project in Mexico.

The original FORTRAN TITAN was rewritten in C (versions 2, 3 and 4), and later migrated to C++ (version 5), on various flavors of UNIX. Currently almost all TITAN installations are run on LINUX. A new tracking algorithm, based on optimization thery, replaced the original. The storm property computations were enhanced. TITAN version 5 was enlarged to include capabilities for longer-term analysis such as storm climatology.

The current version of TITAN is 5. No strict version numbering is followed. Rather, the source code is tagged with the date on which a distribution is made available.

[Top](../../README.md)
[Back](./cloud_seeding_analysis.md)
[Fwd](./acknowledgements.md)


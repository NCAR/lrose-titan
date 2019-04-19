<?php include("../include/begin.php"); ?>
<?php include("./topics.php"); ?>

<!-- Begin main page content. -->
<div id="content">

<h1>Storm climatology</h1>

<h2>Spatial climatology</h2>

<p>
The TrackGridStats application produces analyses of storm tracks over extended periods of time, such as complete seasons or multiple seasons. The output is in the form of 2-D grids which contain information on the spatial variability of various storm properties. 
</p>

<p>
The following figures show some of the properties which may be computed in this way. The properties are  for the month of August 1995 using data from the Front Range NEXRAD near Denver.
</p>

<h4><a name="climo_grid_motion">Spatial climatology of storm volume</a></h4>
<p>This is overlain with the climatology of storm motion.</p>
<img src="./images/climo_grid_motion.png" alt="Sorry, image not available" />

<h4><a name="climo_grid_area">Spatial climatology of storm area</a></h4>
<img src="./images/climo_grid_area.png" alt="Sorry, image not available" />

<h4><a name="climo_grid_precip">Spatial climatology of storm precipitation</a></h4>
<img src="./images/climo_grid_precip.png" alt="Sorry, image not available" />

<h4><a name="climo_grid_duration">Spatial climatology of storm duration</a></h4>
<img src="./images/climo_grid_duration.png" alt="Sorry, image not available" />

<h4><a name="climo_grid_tops">Spatial climatology of storm tops</a></h4>
<img src="./images/climo_grid_tops.png" alt="Sorry, image not available" />

<h4><a name="climo_grid_max_dbz">Spatial climatology of maximum storm refectivity</a></h4>
<img src="./images/climo_grid_max_dbz.png" alt="Sorry, image not available" />

<h2>Aggregate climatology</h2>

<p>
The TracksAscii application produces ASCII tables of storm and track properties, which can then be analyzed by a suitable statistics package. Two categories of property are produced:
</p>

<ul>
<li>Instantaneous storm properties, such as tops</li>
<li>Aggregate track properties, such as duration.</li>
</ul>

<h3>Instantaneous storm properties</h3>

<ul>
<li>Remaining duration (hrs)</li>
<li>Volumetric centroid lat (deg)</li>
<li>Volumetric centroid lon (deg)</li>
<li>Volumetric centroid x (km)</li>
<li>Volumetric centroid y (km)</li>
<li>Volumetric centroid z (km)</li>
<li>Reflectivity-weighted centroid lat (deg)</li>
<li>Reflectivity-weighted centroid lon (deg)</li>
<li>Reflectivity-weighted centroid x (km)</li>
<li>Reflectivity-weighted centroid y (km)</li>
<li>Reflectivity-weighted centroid z (km)</li>
<li>Precipitation centroid lat (deg)</li>
<li>Precipitation centroid lon (deg)</li>
<li>Precipitation centroid x (km)</li>
<li>Precipitation centroid y (km)</li>
<li>Precip area (km2)</li>
<li>Precip orientation (deg T)</li>
<li>Precip major radius (km)</li>
<li>Precip minor radius (km)</li>
<li>Precip flux (m3/s)</li>
<li>Precip rate (mm/hr)</li>
<li>Envelope centroid lat (deg)</li>
<li>Envelope centroid lon (deg)</li>
<li>Envelope centroid x (km)</li>
<li>Envelope centroid y (km)</li>
<li>Envelope area (km2)</li>
<li>Envelope orientation (deg T)</li>
<li>Envelope major radius (km)</li>
<li>Envelope minor radius (km)</li>
<li>Top (km)</li>
<li>Base(km)</li>
<li>Volume (km3)</li>
<li>Mean area (km2)</li>
<li>Mass (ktons)</li>
<li>Tilt angle (deg)</li>
<li>Tilt orientation (deg T)</li>
<li>Max dBZ (dBZ)</li>
<li>Mean dbz (dBZ)</li>
<li>Max dBZ gradient (dBZ/km)</li>
<li>Mean dbz gradient (dBZ/km)</li>
<li>Ht of max dBZ (km)</li>
<li>Vorticity (/s)</li>
<li>Vil from maxZ (kg/m2)</li>
<li>U (km/hr)</li>
<li>V (km/hr)</li>
<li>Dtop/Dt (km/hr)</li>
<li>Dvolume/Dt (km3/hr)</li>
<li>Dprecip_flux/Dt (m3/s2)</li>
<li>Dmass/Dt (ktons/hr)</li>
<li>DdBz_max/Dt (dBZ/hr)</li>
<li>Speed (km/hr)</li>
<li>Dirn (Deg T)</li>
<li>% vol > 40 dBZ</li>
<li>% area > 40 dBZ</li>
<li>% vol > 50 dBZ</li>
<li>% area > 50 dBZ</li>
<li>% vol > 60 dBZ</li>
<li>% area > 60 dBZ</li>
<li>% vol > 70 dBZ</li>
<li>% area > 70 dBZ</li>
<li>Hail-FOKR Cat 0-4</li>
<li>Hail-Waldvogel Prob</li>
<li>Hail-mass aloft ktons</li>
<li>Hail-Vihm kg/m2"</li>
</ul>

<h3>Aggregate track properties</h3>

<ul>
<li>Duration (hr)</li>
<li>Remaining diration at maximum volume (hr)</li>
<li>Mean volume (km3)</li>
<li>Maximum volume (km3)</li>
<li>Mean mass (ktons)</li>
<li>Maximum mass (ktons)</li>
<li>Maximum precip depth, computed using ellipse (mm)</li>
<li>Mean precip depth, computed using ellipse (mm)</li>
<li>Mean precip depth, computed using storm grid points (mm)</li>
<li>Mean precip flux (m3/s)</li>
<li>Maximum precip flux (m3/s)</li>
<li>Mean envelope area (km2)</li>
<li>Maximum envelope area (km2)</li>
<li>Mean precip area (km2)</li>
<li>Maximum precip area (km2)</li>
<li>Mean top (km msl)</li>
<li>Maximum top (km msl)</li>
<li>Mean base (km msl)</li>
<li>Maximum base( km msl)</li>
<li>Mean dBZ</li>
<li>Maximum dBZ</li>
<li>Radar estimated rain volume (m3)</li>
<li>Area time integral (km2.hr)</li>
<li>Swath area computed using ellipse (km2)</li>
<li>Swath area computed using storm grid points (km2)</li>
<li>Mean speed (km/hr)</li>
<li>Mean direction (deg T)</li>
</ul>

<p>
The following figures demonstrate some of the ways in which this data may be analyzed. The data for this analysis was obtained from the Mile High radar, near Denver, for the summer seasons 1991 through 1993.
</p>

<h4><a name="climo_precip_area_lognormal">Lognormal fit to precipitation area</a></h4>
<img src="./images/climo_precip_area_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_precip_flux_lognormal">Lognormal fit to precipitation flux</a></h4>
<img src="./images/climo_precip_flux_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_swath_area_lognormal">Lognormal fit to swath area</a></h4>
<img src="./images/climo_swath_area_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_tops_lognormal">Lognormal fit to storm tops</a></h4>
<img src="./images/climo_tops_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_max_speed_lognormal">Lognormal fit to maximum speed</a></h4>
<img src="./images/climo_max_speed_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_max_dbz_lognormal">Lognormal fit to maximum reflectivity</a></h4>
<img src="./images/climo_max_dbz_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_ati_lognormal">Lognormal fit to area time integral (ATI)</a></h4>
<img src="./images/climo_ati_lognormal.png" alt="Sorry, image not available" />

<h4><a name="climo_duration_pdf">Exponential fit to duration > 15 min</a></h4>
<img src="./images/climo_duration_pdf.png" alt="Sorry, image not available" />

<h4><a name="climo_rerv_vs_ati">Radar estimated rain volume vs. Area time integral</a></h4>
<img src="./images/climo_rerv_vs_ati.png" alt="Sorry, image not available" />

<h4><a name="climo_vol_vs_refl">Volume vs. mean reflectivity</a></h4>
<img src="./images/climo_vol_vs_refl.png" alt="Sorry, image not available" />

<h4><a name="climo_precip_area_vs_vol">Precipitaiton area vs. volume</a></h4>
<img src="./images/climo_precip_area_vs_vol.png" alt="Sorry, image not available" />

<!-- div#content :: End main page content. -->
</div>

<?php include("../include/end.php"); ?>


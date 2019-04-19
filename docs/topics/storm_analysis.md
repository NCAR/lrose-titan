<?php include("../include/begin.php"); ?>
<?php include("./topics.php"); ?>

<!-- Begin main page content. -->
<div id="content">

<h1>Storm analysis</h1>

<h2>Spatial storm properties</h2>

<p>
Storm tracks may be presented in geographical view in a number of ways, depending upon the need. The following plots were produced using the Rview display application.
</p>

<h4><a name="rview_current_polygons">Current storm polygons</a></h4>
<p>A simple plot showing the current location of the storms represented as polygons.</p>
<img src="./images/rview_current_polygons.png" alt="Sorry, image not available" />

<h4><a name="rview_past_forecast_polygons">Recent past and forecast as polygons</a></h4>
<p>This shows the current storm location in cyan, the recent (30-min) past in yellow and the 30-min forecast in red. This can get a little cluttered, so the figure below this one uses ellipses instead of polygons.</p>
<img src="./images/rview_past_forecast_polygons.png" alt="Sorry, image not available" />

<h4><a name="rview_past_forecast_ellipses">Recent past and forecast as ellipses</a></h4>
<p>This shows the current storm location in cyan, the recent (30-min) past in yellow and the 30-min forecast in red. This is less cluttered than the previous figure because of the use of ellipses instead of polygons.</p>
<img src="./images/rview_past_forecast_ellipses.png" alt="Sorry, image not available" />

<h4><a name="rview_past_future_ellipses_single">Full track as ellipses</a></h4>
<p>This shows an entire track for analysis, using ellipses to represent storm location. The current location is in cyan, the past in yellow and the future in green. The 'future' locations would not be there in real-time of course, but for analysis purposes it is useful to show an entire track.</p>
<img src="./images/rview_past_future_ellipses_single.png" alt="Sorry, image not available" />

<h4><a name="rview_past_future_ellipses_filled_single">Full track as filled ellipses</a></h4>
<p>Similar to the previous figure, except using filled ellipses of alternating brightness. The current location is in cyan, the past in yellow and the future in green. Filling the ellipses provides a result which is easier on the eye while revealing the complexity of the track.</p>
<img src="./images/rview_past_future_ellipses_filled_single.png" alt="Sorry, image not available" />

<h4><a name="rview_all_vectors_day">All tracks in a day, as vectors</a></h4>
<p>All of the tracks for a single day, represented as vectors. This is useful for categorizing days, based on aggregate storm movement, for climatological purposes.</p>
<img src="./images/rview_all_vectors_day.png" alt="Sorry, image not available" />

<h4><a name="rview_all_vectors_ellipses_filled_day">All tracks in a day, as filled ellipses</a></h4>
<p>All of the tracks for a single day, represented as filled ellipses. This is useful for categorizing days, based on aggregate storm movement, for climatological purposes.</p>
<img src="./images/rview_all_vectors_ellipses_filled_day.png" alt="Sorry, image not available" />

<h2>Storm time histories</h2>

<h4><a name="time_hist">Time history of volume, area, mass, precip flux and vil</a></h4>
<p>Time history of storm properties. Volume (gray), area (cyan), mass (magenta),  precipitation flux (green) and VIL (yellow).</p>
<img src="./images/time_hist.png" alt="Sorry, image not available" />

<h4><a name="time_ht_maxz">Time-height profile of max dBZ</a></h4>
<p>Top and base are in yellow, the Z-weighted centroid is in cyan and the height of max echo is in blue, along with the maximum value.</p>
<img src="./images/time_ht_maxz.png" alt="Sorry, image not available" />

<h4><a name="time_ht_meanz">Time-height profile of mean dBZ</a></h4>
<p>Top and base are in yellow, the Z-weighted centroid is in cyan and the height of max echo is in blue, along with the maximum value.</p>
<img src="./images/time_ht_meanz.png" alt="Sorry, image not available" />

<h4><a name="time_ht_percent_mass">Time-height profile of vertical distribution of mass</a></h4>
<p>This colors show the percentage of mass at each height in the storm, with time.</p>
<img src="./images/time_ht_percent_mass.png" alt="Sorry, image not available" />

<h4><a name="time_ht_rotation">Time-height profile of storm rotation</a></h4>
<p>The is dependent on the availability of Doppler velocity. It shows the estimated rotation of the storm about its centroid, at each height and time. Contiguous regions of red or blue indicate significant rotation, as in a supercell. A meso-cyclone will only be shown if it is colocated with  the storm centroid.</p>
<img src="./images/time_ht_rotation.png" alt="Sorry, image not available" />

<h4><a name="hail_stats">Time history of hail metric</a></h4>
<p>Shown are the FOKR (gray), WaldVogel probability (cyan), hail mass (green) and vertically integrated hail mass (magenta).</p>
<img src="./images/hail_stats.png" alt="Sorry, image not available" />

<h4><a name="refl_dist_vol">Time history of reflectivity distribution</a></h4>
<p>This shows the distribution of reflectivity in the storm volume, with time. The height of each color shows the percentage of the storm volume which contains reflectivity in that color interval.</p>
<img src="./images/refl_dist_vol.png" alt="Sorry, image not available" />

<!-- div#content :: End main page content. -->
</div>

<?php include("../include/end.php"); ?>


<?php include("../include/begin.php"); ?>
<?php include("./topics.php"); ?>

<!-- Begin main page content. -->
<div id="content">

<h1>Short-term forecasting</h1>

<h2>Extrapolation forecasts</h2>
<p>
In formulating the storm forecast algorithm, we make the following simplifying assumptions based on observations of typical storm behavior:
</p>

<ul>
<li>A storm tends to move along a straight line;</li>
<li>Storm growth or decay tends to follow a linear trend;</li>
<li>Random departures from the above behavior occur.</li>
</ul>

<p>
As as result, TITAN relies purely on extrapolation for forecasting. A weighted linear fit is performed to the time-history of the storm property for which a forecast is required. The following figure shows a typical linear fit for forecast parameter p.
</p>

<h4><a name="forecast_fit">Weighted linear fit to storm time history</a></h4>
<img src="./images/forecast_fit.png" alt="Sorry, image not available" />

<p>
Linear trend forecasts are made for the following storm properties:
</p>

<ul>
<li>Projected area centroid (X,Y)</li>
<li>Volumetric centroid Z</li>
<li>Reflectivity-weighted centroid Z</li>
<li>Top</li>
<li>Max dBZ</li>
<li>Volume</li>
<li>Precipitation flux</li>
<li>Mass</li>
<li>Projected area</li>
<li>Speed</li>
<li>Direction</li>
</ul>

<h2>Handling mergers and splits</h2>
<p>
The forecast depends on the recent storm history. Therefore, when a merger or split occurs, the history must be combined or split accordingly.
</p>

<h3>Forecasts for X,Y - location, speed and direction</h3>

<p>
Consider the merger depicted in the following figure. The positional history of the merged track is a combination of the histories of the three parent tracks. First, the parent track histories are translated in (x, y) so that their forecast positions coincide with the centroid after the merger. These translated histories are then combined as a weighted average, where the weights are the ratio of the storm volume for each parent to the sum of the volumes of all parents. The weights change at each time in the history, depending on the size history of each of the parents.
</p>

<h4><a name="merger_translation">Handling (x,y) time history in a merger</a></h4>
<img src="./images/merger_translation.png" alt="Sorry, image not available" />

<p>In the case of a split, the history of each child is a copy of the history of the parent, translated to coincide with the centroid of that child - see the figure below. The translated histories are only used for forecasts; they do not affect the statistical analysis of storm properties.
</p>

<h4><a name="split_translation">Handling (x,y) time history in a split</a></h4>
<img src="./images/split_translation.png" alt="Sorry, image not available" />

<h3>Forecasts for storm size - area, volume, mass etc.</h3>

<p>
In the merger case, the history of a parameter is computed as the sum of the histories of the parents. In the split case, the history for a child is computed as the history for the parent scaled by the ratio of the volume of that child storm to the sum of the volumes of all of the children.
</p>

<h2>Forecast examples</h2>

<p>
The following figure shows a 30-minute forecast of storm location, presented as a series of forecasts at 6 minute intervals. The storm speed is also shown in km/hr. Growing storms have increasing forecast areas while decaying storms have decreasing forecast areas.
</p>

<h4><a name="forecast_location">Storm speed/direction/location forecast</a></h4>
<img src="./images/forecast_location.png" alt="Sorry, image not available" />

<p>
The following figure shows a time-series plot of storm mass (magenta), area (cyan) and and volume (gray) for a particular storm track. The red lines are the 30-minute forecast for each property. Since this is an analysis example, the remaining history of the storm track is also shown, although that would not be the case in a real-time situation.
</p>

<h4><a name="forecast_mass_area_vol">Storm mass/area/volume forecast</a></h4>
<img src="./images/forecast_mass_area_vol.png" alt="Sorry, image not available" />

<!-- div#content :: End main page content. -->
</div>

<?php include("../include/end.php"); ?>


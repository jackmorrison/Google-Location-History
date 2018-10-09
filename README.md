# Places I've Visited Interactive World Map

This project involves creating a world map to display everywhere that I have visited in a different way to sticking pins onto a wall.

The project is based on Geoff Boeing's blog post [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/) and GitHub repo [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/).

The location history was extracted from Google Maps in JSON format, this data ranges from 2014 to 2018 and contains over 1 million co-ordinates (1,083,365 rows).

The data was clustered using the DBSCAN algorithm, which groups data points (latitude and longitudes) together if they are within a certain distance of eachother. The clustered data set was then reverse geocoded using the Google Maps Geocoding API and mapped using Leaflet an opensource Javascript library. The interactive map can be viewed by clicking [here](https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html) or on the images below.

<p align="center">
  <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map-Thailand.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Thailand-Summer-2017.jpg" alt="Thailand Map" width="425" height="510">
  </a>

  <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map-Toronto.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Toronto-Summer-2016.jpg" alt="Toronto Map" width="425" height="510">
  </a>
</p>

<p align=center>
<a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html">
  <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Full-Map-1.jpg" alt="Leaflet Map">
</a>
</p>

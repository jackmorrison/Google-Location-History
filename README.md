# Interactive World Map of Places I've Visited

This project involves creating a world map to display everywhere that I have visited in a more interactive and digital way than sticking pins onto a wall.

The project is based on Geoff Boeing's blog post [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/) and GitHub repo [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/).

The location history was extracted from Google Maps in JSON format, this data ranges from 2014 to 2018 and contains over 1 million co-ordinates (1,083,365 rows).

The data was clustered using the DBSCAN algorithm, which groups data points (latitude and longitudes) together if they are within a certain distance of eachother. The clustered data set (3,312 rows) was then reverse geocoded using the Google Maps Geocoding API and mapped using Leaflet, an open-source Javascript interactive maps library. The interactive map can be viewed by clicking [here](https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html) or on the images below.

I then broke down the data by year to highlight places visited across Ireland (and places lived in).

<p align="center">
  
  <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Ireland-by-Year.gif" alt="Ireland by Year" height="846" width="650">
  
</p>

<p align="center">
  <b> Toronto Summer 2016 & Thailand Summer 2017 </b>
</p>

<p align="center">
    <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map-Toronto.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Toronto-Summer-2016.jpg" alt="Toronto Map" width="400" height="480">
  
  </a>
  <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map-Thailand.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Thailand-Summer-2017.jpg" alt="Thailand Map" width="400" height="480">

  </a>
</p>

Two of my most boring visits may include **Keflavik** and **Paris** where I stopped for 1 hour layovers... 

<p align="center">
    <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Iceland-2016-2.jpg" alt="Iceland">
  
  </a>
  </p>
  <p align="center">
  <a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html">
    <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Paris-2017-1.jpg" alt="Paris">

  </a>
  </p>

All countries visited are highlighted on the map below which can be clicked for more detail.

<p align=center>
<a href="https://rawgit.com/jackmorrison/Google-Location-History/master/Leaflet/Map.html">
  <img src="https://raw.githubusercontent.com/jackmorrison/Location-History/master/Images/Full-Map-1.jpg" alt="Leaflet Map">
</a>
</p>

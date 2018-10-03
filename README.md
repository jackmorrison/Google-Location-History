# Google Location History Visualisation

This project involves visualising my location history data downloaded from Google Maps. The project is based on Geoff Boeing's blog post [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/) and GitHub Repo [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/).

I used this project as an introduction to Python and data analytics. 

The project began by extracting my location history from Google Maps, this data ranges from 2014 to 2018 and contains over 1 million co-ordinates (1,083,365 rows). Once the data was extracted in JSON format it was loaded into a DataFrame and the co-ordinates were plotted onto a world map  using BaseMap, the resulting map is displayed below.

![alt text](https://github.com/jackmorrison/Google-Location-History/blob/master/Images/World%20Map.png "World Map")

From the image, it is visible that most of the location history points are placed in Ireland. It is also visible that there are a number of points marked in places which I have not visited (for example in Turkey and the Ivory Coast) for which I would take a guess are incorrect GPS assignments or connections to VPN's based in these areas. 

As the majority of the location points are in Ireland I focused the next steps on only displaying only the country of Ireland, the resulting map is displayed below.
<p align="center">
  <img src="https://github.com/jackmorrison/Google-Location-History/blob/master/Images/IrelandMap.png">
</p>




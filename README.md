# Google Location History Visualisation

This project involves visualising my location history data downloaded from Google Maps. The project is based on Geoff Boeing's blog post [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/) and GitHub Repo [here](https://geoffboeing.com/2016/06/mapping-everywhere-ever-been/).

I used this project as an introduction to Python and data analytics. 

The project began by extracting my location history from Google Maps, this data ranges from 2014 to 2018 and contains over 1.5 million co-ordinates. Once the data was extracted in JSON format I loaded it into a DataFrame and mapped all of the co-ordinates onto a world map which is displayed below.

![alt text](https://github.com/jackmorrison/Google-Location-History/blob/master/Images/World%20Map.png "World Map")

As most of the data contained in the dataset would be set in Ireland, I then adjusted the parameters of the script to display the country of Ireland and then map all co-ordinates onto this area. The below image was then produced. 





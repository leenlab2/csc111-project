# Trip Planner - Paris
## 1. Problem Description and Research Question
The tourism industry is quite a lucrative one, with approximately 1.4 billion people travelling internationally per year (Roser, 2017), which is almost 17.7\% of the entire population of the world. Thanks to its wide array of tourist destinations, the majority of international travelers tend to head to Europe (Roser, 2017). France, in particular, is visited by almost 90 million tourists every year, which is more than 10\% of worldwide total tourist market (Statista Research Department, 2020). The capital, Paris, receives the majority of these tourists, hosting 34.5 million tourists in 2019. This makes France the most visited country in the world (Statista Research Department, 2020).

Each one of those millions of travelers has to go through the arduous task of arranging a schedule for their visit. Planning a trip involves considering a numerous number of factors, from the reviews on a certain restaurant to when a particular landmark is open for visitation. Even after the specific locations are chosen, you need to craft the optimum route in order to hit all the attractions you want to see. This also involves choosing which form of public transit would be best to use to get to those locations. Thus, a lot of work goes into planning a single day, let alone an entire trip. 

All in all, it is a very tedious and complicated process, therefore designing a program for it would be very useful to those who want to travel. There are many programs that help with travelling, but most of them are specific to an area of travel, such as hotels, flights, and sightseeing. They do not have a way to account for all these categories at once in the planning process. A program for that would be very useful. Hence, we set out to explore **how we can generate a possible itinerary for tourists visiting Paris, France based on geographical location and community reviews.**

## 2. Dataset Description
### 2.1 Raw Data
The raw datasets consist of 2 csv files and an txt file.
`paris-attraction.csv` and `paris-restaurant.csv` where extracted from Tourpedia (Tourpedia, 2013). However both provided inconsistent data, by omitting information and after a certain number of rows. The data provided on each column changed from (address, category, id etc) to (id, name, address, etc), which would result in complications when reading the data, hence, we decided to use the latter half of the data-set. The data was converted through `attraction_cleaner.py` , `attraction_review_addition.py`, `restaurants_cleaner.py` and `hotel_cleaner.py`, incorporating data from Google Places API for reviews and opening times were needed (*Google Places API Overview*, n.d.). The hotel data is gathered using Google Places API. This data is filtered by those with ratings higher than 3/5 to save computational resources.

1. `paris-attraction.csv` and `paris-restaurant.csv`: contains id, name, address, category, city, latitude, longitude, and urls representing api calls.

The subway station data was extracted from `metro_paris.txt` from the Paris Metro Project (BTajini, 2017). This file is split into parts, where the first 377 lines represent the station names and ids, and the latter half representing the edges between them. That section holds three numbers, the first two of which correspond to id numbers of the stations connected by that edge. The processing of this data is handled in `metro_lines_cleaner.py`. The Position Stack API was used in `paris_metro_line_coordinates.py` to find their geographical coordinates (*API Documentation*, n.d.).

### 2.2 Processed Data
The output of this functions was stored as the processed csv datasets of: `paris_metro_lines.csv`, `paris_metro_stations.csv`, `paris-attractions-final.csv`, `paris-hotel.csv` and `paris-restaurant-organized-final.csv`.

The columns used are as follows:
1. `paris-attraction-final.csv`: name, latitude, longitude, and opening times where each column is as Sunday-open, Sunday-close, Monday-open, Monday-close, etc...
2. `pairs-hotel.csv`: name, latitude, longitude
3. `paris-restaurant-organized-final.csv`: name, latitude, longitude, rating, opening times (same as previous)
4. `paris_metro_lines.csv`: edge vertex 1, edge vertex 2
5. `paris_metro_stations.csv`: id, name, latitude, longitude

## 3. How to Run the Program
### 3.1 Running the Files For Main Program
Simply run `main.py`, and an input pop-up window should open:
![image](https://user-images.githubusercontent.com/74102544/130708000-0b72f789-155d-4bca-b826-d4cb88b1ddf2.png)
Choose a hotel from the drop down list. Input Leave time and Return time in YYYY-MM-DD HH:MM. They should occur on the same day, and an invalid date would cause an error message.
![image](https://user-images.githubusercontent.com/74102544/130708069-f0e1fbe7-5846-492d-8ec8-882e2d9c81b9.png)
Click on Submit and **then on Close** for the program to upload the information inputted. If the input was invalid you need to click Submit again. Console messages should be printed displaying where in the process the program is. At the end, two pop ups will apear, a graph over a map, and a schedule. Rerun the program to generate another schedule.

![image](https://user-images.githubusercontent.com/74102544/130708184-374720b0-eab4-493b-b799-a10d8e3850b1.png)
![image](https://user-images.githubusercontent.com/74102544/130708192-cfcd662f-10b7-44d2-8a31-3cf54c7ee0be.png)

## References
Abdul Bari. (2018, February 10). *3.6 Dijkstra Algorithm - Single Source Shortest Path - Greedy Method* [Video]. Youtube. (https://www.youtube.com/watch?v=XB4MIexjvY0)

Amos, D. (2020, November 07). *Python GUI Programming With Tkinter*. (https://realpython.com/python-gui-tkinter/)

*API Documentation* (n.d.). positionstack. Retrieved April 16, 2021 from (https://positionstack.com/documentation)

BTajini (2017, February 7), *Paris-Metro-Project* [dataset]. (https://github.com/BTajini/Paris-Metro-Project/blob/master/Data/metro_paris.txt)

*Google Places API Overview*. (n.d.). Google Maps Platform. Retrieved April 16, 2021 from (https://developers.google.com/maps/documentation/places/web-service/overview)

Matplotlib development team. (n.d.). *Matplotlib: Visualization with Python*. Matplotlib. Retrieved April 16, 2020 from (https://matplotlib.org/)

Roser, M. (2017, April 24). *Tourism*. Our World in Data. (https://ourworldindata.org/tourism)

Statista Research Department. (2020, April 27). *Number of tourist arrivals in Paris hotels 2011-2019*. Statista. (www.statista.com/statistics/468164/number-tourist-arrivals-hotels-paris/)

Tourpedia (2013), *paris-attraction* [dataset], *paris-restaurant* [dataset], *paris-accomodation* [dataset]. OpeNER Project. (http://tour-pedia.org/about/datasets.html)

Veness, Chris (n.d.). *Calculate distance, bearing and more between Latitude/Longitude points*. Movable Type Scripts. Retrieved April 16, 2021 from (https://www.movable-type.co.uk/scripts/latlong.html)

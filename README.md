###Playing around with votings statistics from the 2016 US presidential eleciton###

The electoral college directs a lot of focus to "red states" and "blue states", but I was curious what patterns emerged at the county level. Specifically, I wanted to test the urban-rural divide narrative by seeing how the population of a county correlated with voting patterns.

![My image](https://github.com/anbrjohn/Misc/blob/master/votingresults.png)

(Data sources are attriburted in the code)

The plot above shows the percentage of votes in a county for the Republicans (red) vs. Democrats (blue). A polynomial regression line is fit to the data to highlight the general pattern; namely, that for an average US county, roughly two-thirds of the votes go to the GOP for counties of populations up to 100,000. However, after around 1,000,000 people, they tend to rapidly become Democrat-majority. 
However, the graph clearly shows some outliers. Below are the top-20 most unexpected counties for each party, given this model.

**Top 20 unexpectedly pro-GOP counties:**

 | Location | Population | Percent for GOP 
--- | --- | --- | --- 
1| Maricopa County, AZ        |Population: 4,009,412  |Percent for GOP: 49.13%
2| Harris County, TX          |Population: 4,336,853  |Percent for GOP: 41.83%
3|  Orange County, CA	        |Population: 3,114,363 	|Percent for GOP: 43.28%
4|  San Diego County, CA	    |Population: 3,211,252 	|Percent for GOP: 38.24%
5|  Riverside County, CA	    |Population: 2,292,507 	|Percent for GOP: 45.28%
6|  Tarrant County, TX	      |Population: 1,911,541 	|Percent for GOP: 52.15%
7|  Cook County, IL	          |Population: 5,240,700 	|Percent for GOP: 21.42%
8|  Miami-Dade County, FL	    |Population: 2,617,176 	|Percent for GOP: 34.09%
9|  San Bernardino County, CA	|Population: 2,088,371 	|Percent for GOP: 42.41%
10| Roberts County, TX	      |Population: 831 	      |Percent for GOP: 95.27%
11| Dallas County, TX	        |Population: 2,480,331 	|Percent for GOP: 34.89%
12| Clark County, NV	        |Population: 2,027,868 	|Percent for GOP: 41.75%
13| King County, TX	          |Population: 285 	      |Percent for GOP: 93.71%
14| Suffolk County, NY	      |Population: 1,499,738 	|Percent for GOP: 52.48%
15| Grant County, NE	        |Population: 633 	      |Percent for GOP: 93.15%
16| Hayes County, NE	        |Population: 976 	      |Percent for GOP: 92.35%
17| Motley County, TX	        |Population: 1,196 	    |Percent for GOP: 92.1%
18| Glasscock County, TX	    |Population: 1,251 	    |Percent for GOP: 91.86%
19| Shackelford County, TX	  |Population: 3,375 	    |Percent for GOP: 91.74%
20| Blount County, AL	        |Population: 57,872 	  |Percent for GOP: 89.85%


**Top 20 unexpectedly pro-DEM counties:**

 | Location | Population | Percent for DEM 
--- | --- | --- | --- 
1|  Petersburg city, VA	      |Population: 32,538 	  |Percent for DEM: 87.52%
2|  Jefferson County, MS	    |Population: 7,629 	    |Percent for DEM: 86.47%
3|  Claiborne County, MS	    |Population: 9,253   	  |Percent for DEM: 85.41%
4|  Greene County, AL	        |Population: 8,744 	    |Percent for DEM: 82.39%
5|  Macon County, AL	        |Population: 19,688   	|Percent for DEM: 82.73%
6|  Holmes County, MS	        |Population: 18,428 	  |Percent for DEM: 82.61%
7|  Charlottesville city, VA	|Population: 44,349   	|Percent for DEM: 80.43%
8|  Menominee County, WI	    |Population: 4,317 	    |Percent for DEM: 78.42%
9|  Noxubee County, MS	      |Population: 11,089   	|Percent for DEM: 78.19%
10| Zavala County, TX	        |Population: 12,156 	  |Percent for DEM: 77.67%
11| Starr County, TX	        |Population: 61,963   	|Percent for DEM: 79.09%
12| Jim Hogg County, TX	      |Population: 5,245 	    |Percent for DEM: 77.16%
13| Clayton County, GA	      |Population: 264,220   	|Percent for DEM: 85.06%
14| Allendale County, SC	    |Population: 9,839 	    |Percent for DEM: 76.08%
15| Falls Church city, VA	    |Population: 13,508 	  |Percent for DEM: 75.78%
16| Hancock County, GA	      |Population: 8,879 	    |Percent for DEM: 75.45%
17| Bullock County, AL	      |Population: 10,639 	  |Percent for DEM: 75.09%
18| Maverick County, TX	      |Population: 55,932 	  |Percent for DEM: 76.52%
19| Brooks County, TX	        |Population: 7,237 	    |Percent for DEM: 74.61%
20| Tunica County, MS	        |Population: 10,560 	  |Percent for DEM: 74.42%

###Observations:###
In general, an outlier is a county with a very large population that still had a large GOP voting base or a small county that had a relatively large Democrat vote. It's worth noting that this model still suggests that there should be around one-third of the vote for the Democrats even in the smallest of counties. That is why very small counties like Roberts County, TX still made the list if they voted almost entirely Republican.

Additionally, although the "deep south" is associated with being very conservative politically, multiple small counties in Alabama and Mississippi made the list for voting unexpectedly Democrat. Other regions such as the Rockies and the Midwest, which also have many small-population counties, nevertheless strayed less from the norm than these. This dichotomy is likely due to demographic differences.

Interestingly, many of the unexpected counties for both parties are from Texas. This suggests that some factor(s) other than population is affecting voting patterns there. Also, this model is probably overly simplified, especially the quadratic regression.

###Map:###

![My image](https://github.com/anbrjohn/Misc/blob/master/newmap.png)

I also generated a heatmap in makemap.py. Note again that the colors correspond to unexpected voting patterns given the population of the county, not the actual outcome. Compared to this [map](https://en.wikipedia.org/wiki/United_States_presidential_election,_2016#/media/File:United_States_presidential_election_results_by_county,_2016.svg) there are many similar patterns but some differences. For example, boroughs in Alaska that voted majority Republican should have voted by an even larger margin given this model, so they show up as blue on this map. The same is true in reverse for the tip of Florida, which voted majority Democrat, but not by as large as margin as expected.
States with more white and pale shades of blue and red vote more "expectedly" given the population of their counties. However, the large amount of dark blue and dark red counties suggests belies the notion that votes for the two main political parties is falls only along the urban-rural divide.

#! usr/bin/env python3
# -*- coding: UTF-8 -*- #

# Andrew Johnson
# February 12, 2017

import matplotlib.pyplot as plt
import numpy as np

# 2016 County-Level Election Data from:
# https://github.com/tonmcg/County_Level_Election_Results_12-16/blob/master/2016_US_County_Level_Presidential_Results.csv
with open("counties.txt") as f:
    voting = f.readlines()
    voting = voting[1:]
voting = [x.split(",") for x in voting]
# FIPS code, state abbreviation, county name, percent voting DEM, percent voting GOP
voting = {int(x[-1]): [x[-3], x[-2], float(x[4]), float(x[5])] for x in voting}

# County Population (as of 2013!) data from:
# https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents
with open("population.txt") as f:
    pop = f.readlines()
    pop = pop[4:]
pop = [x.split("\t") for x in pop]
# FIPS code: state, county name, population
pop = {int(x[0]): [x[2], x[1], int(x[3].replace(",",""))] for x in pop}

for county in pop:
    try:
        voting[county].append(pop[county][-1])
    except: #1 or 2 counties lack appropriate data
        pass

data = list(voting.values())
data = [x[::-1] for x in data if len(x)==5]
data.sort()

population = [x[0] for x in data]
gop = [x[1] for x in data]
dem = [x[2] for x in data]

# Plot county points
plt.plot(population,dem, "bo")
plt.plot(population,gop, "ro")
plt.xscale('log')

# Calculate and plot 2nd order polynomial regression curve
x_line = population[:-2]
polynomial_degree = 2
gop_func = np.poly1d(np.polyfit(population, gop, deg=polynomial_degree))
dem_func = np.poly1d(np.polyfit(population, dem, deg=polynomial_degree))
plt.plot(x_line, gop_func(x_line), "r-", linewidth=5)
plt.plot(x_line, dem_func(x_line), "b-", linewidth=5)

plt.xscale('log')
plt.xlabel("County Population")
plt.ylabel("% Votes for Each Party")
plt.title("US 2016 Presidential Election\nCounty-level Voting Results")
plt.ylim(0, 1.0)
plt.show()

# Figure out the counties that diverge most from the regression curve's prediction
for county in data:
    population = county[0]
    gop = county[1]
    dem = county[2]
    gop_diff = gop_func(population) - gop
    dem_diff = dem_func(population) - dem
    county.append(gop_diff)
    county.append(dem_diff)
gop_diff = sorted(data, key=lambda x:x[-2])
dem_diff = sorted(data, key=lambda x:x[-1])

print("Top 20 unexpectedly pro-GOP counties:")
for i in range(20):
    county = gop_diff[i]
    print('{}, {}\t Population:{} \tPercent for GOP: {}%'.format(county[3], 
          county[4], "{:,}".format(county[0]), round(county[1]*100, 2)))
print("\n")

print("Top 20 unexpectedly pro-DEM counties:")
for i in range(20):
    county = dem_diff[i]
    print('{}, {}\t Population:{} \tPercent for GOP: {}%'.format(county[3], 
          county[4], "{:,}".format(county[0]), round(county[2]*100, 2)))

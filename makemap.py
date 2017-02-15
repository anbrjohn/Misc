#! usr/bin/env python3
# -*- coding: UTF-8 -*- #

# Andrew Johnson
# February 15, 2017

"""
Given dem_diff list from votingstats.py,
creates a heap map (svg) of US counties,
"""

from bs4 import BeautifulSoup

# Assign each county to a category for how unexpectedly +DEM or +GOP it is
cat = 7 # Number of categories
category = 1
for i in range(len(dem_diff)):
    dem_diff[i].append(category)
    if i != 0:
        if i % int(len(dem_diff)/(cat)) == 0:
            category += 1
        if category > cat:
            category = cat

cat_dict = {} # {FIPS : catagory]
for county in dem_diff:
    cat_dict[county[-4]] = county[-1]

# Open blank US county map
# From: https://commons.wikimedia.org/wiki/File:USA_Counties_with_FIPS_and_names.svg
with open('USA_Counties.svg', 'r') as f:
    us_map = f.read()
soup = BeautifulSoup(us_map, selfClosingTags=['defs','sodipodi:namedview'])
paths = soup.findAll('path') # Get all counties

# Formatting stuff
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
# Map colors, from dark blue to white to dark red
colors = ['#2166ac', '#67a9cf', '#d1e5f0', '#f7f7f7', '#fddbc7', '#ef8a62', '#b2182b']

# Color the counties based on category
for path in paths:
    fips = path['id']
    if fips not in ["State_Lines", "separator"]: # Leave state boundaries as is
        try:
            color = colors[cat_dict[int(fips)]-1]
        except:
            continue     
        path['style'] = path_style + color

with open("newmap.svg", "w") as f:
    f.write(soup.prettify())

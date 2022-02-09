from sys import argv
from bs4 import *
from statistics import mean
from math import cos, radians

script, filename = argv


#get coordinate arrays from xml
def get_coordinates(soup):
    points_list = soup.find_all("Point")
    longitudes = []
    latitudes = []

    for element in points_list:
        coordinate = element.coordinates
        content = coordinate.contents
        content = content[0]
        #this is kinda criss-crossed due to the weird lat, long format of the kml file
        longitude, latitude, height = content.split(",")
        longitude = float(longitude)
        latitude = float(latitude)
        #print(longitude)
        longitudes.append(longitude)
        #print(latitude)
        latitudes.append(latitude)

    return longitudes, latitudes


#calculate the mean coordinates and then merge them into a string
def mean_coordinates(all_long, all_lat):
    long_mean = mean(all_long)
    lat_mean = mean(all_lat)
    final_coordinates = f"The mean coordinates are:{lat_mean}, {long_mean}"
    return final_coordinates

def latitude_weighting(all_long, all_lat):
    weighted_long_arr = []
    i = 0
    for x in all_long:
        weighted_long = all_long[i] * abs(cos(radians(all_lat[i])))
        weighted_long_arr.append(weighted_long)
        i += 1
    return weighted_long_arr

def weighted_mean_coordinates(all_long, all_lat):
    all_weighted_long = latitude_weighting(all_long, all_lat)
    long_mean = mean(all_weighted_long)
    lat_mean = mean(all_lat)
    final_coordinates = f"The weighted mean coordinates are:{lat_mean}, {long_mean}"
    return final_coordinates

#open file and feed to parser
xml = open(filename)
soup = BeautifulSoup(xml, "xml")
xml.close()

#run all the magic
all_long, all_lat = get_coordinates(soup)
mean_point = mean_coordinates(all_long, all_lat)
print (mean_point)
weighted_mean_point = weighted_mean_coordinates(all_long, all_lat)
print(weighted_mean_point)

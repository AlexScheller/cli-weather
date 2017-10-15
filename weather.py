#!/usr/bin/python3

# weather.py queries the open-weather-map api (https://openweathermap.org/api)
# to output weather data to the console.

# Alex Scheller, August 2017

import sys
import json
import argparse
import datetime
import requests

# The default city id to search for. A list of them can be found
# here: http://openweathermap.org/help/city_list.txt.
DEFAULT_CITY_ID = "5809844" # Seattle

# Yields your public facing ip and the city associated with
# it - mileage may vary.
def locate_city_by_ip():
	try:
		public_ip_url = "http://httpbin.org/ip"
		res_ip = json.loads(requests.get(public_ip_url).text)["origin"]
		city_url = "http://ipapi.co/" + res_ip + "/json/"
		located_city = json.loads(requests.get(city_url).text)["city"]
		yield located_city
		yield res_ip
	except:
		print("Error locating city by ip: ", sys.exc_info()[0])

# Using the specified flags, this function requests weather data
# from the owm api.
def get_weather_json(flags):
	# your api key goes here
	api_key = "your-key-here"
	units = "imperial"
	if flags.metric:
		units = "metric"
	params = {"appid": api_key, "units": units}
	if flags.iplocate:
		params["q"], res_ip = locate_city_by_ip()
		print("Best guess for city from public ip: " + res_ip)
	# if a search string is specified, the "iplocate" flag order is ignored.
	if flags.search:
		params["q"] = flags.search
	else:
		params["id"] = DEFAULT_CITY_ID
	api_url = "http://api.openweathermap.org"
	api_target = "/data/2.5/weather"
	weather_response = requests.post(api_url + api_target, params=params)
	return json.loads(weather_response.text)

# Converts the json response to a readable string 
def process_weather_json(flags, weather_json):
	delimiter = "\n"
	if flags.oneline:
		delimiter = ", "
	city_name = weather_json["name"]
	temp = weather_json["main"]["temp"]
	weather_description = weather_json["weather"][0]["description"]
	ret = city_name + ":"
	if flags.oneline:
		ret += " "
	else:
		ret += "\n"
	ret += str(temp) + " degrees" + delimiter +  weather_description
	if flags.windspeed or flags.everything:
		ret += delimiter + "wind " + str(weather_json["wind"]["speed"])
		if flags.metric:
			ret += " m/s "
		else:
			ret += " mi/h "
		if "deg" in weather_json["wind"]:
			ret += str(weather_json["wind"]["deg"]) + " degrees"
	if flags.pressure or flags.everything:
		if flags.metric:
			ret += delimiter + "pressure " + str(weather_json["main"]["pressure"]) + " hPa/mb"
		else:
			# constant to convert from hectopascals(milibars) to atmospheres.
			# by default the owm api returns hectopascals.
			HP_TO_ATM = 0.000986923
			pressure = str(round(weather_json["main"]["pressure"] * HP_TO_ATM, 3))
			ret += delimiter + "pressure " + pressure + " atm"
	if flags.humidity or flags.everything:
		ret += delimiter + "humidity " + str(weather_json["main"]["humidity"]) + "%"
	if flags.time or flags.everything:
		date = weather_json["dt"]
		time_collected = datetime.datetime.fromtimestamp(date).strftime("%H:%M:%S %Y-%m-%d")
		ret += "\ntime and date collected: " + time_collected
	return ret

# Setup for the various flags accepted by the program.
def parse_flags():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--search", type=str, help="allows searching for a city by name [city[,country]], squelches iplocate")
	parser.add_argument("-ip", "--iplocate", help="searches for weather based on location determined by public ip address", action="store_true")
	parser.add_argument("-m", "--metric", help="specifies metric", action="store_true")
	parser.add_argument("-p", "--pressure", help="displays pressure at sea level", action="store_true")
	parser.add_argument("-ph", "--humidity", help="displays percent humidity", action="store_true")
	parser.add_argument("-ws", "--windspeed", help="displays wind speed", action="store_true")
	parser.add_argument("-ol", "--oneline", help="displays results on a single line", action="store_true")
	parser.add_argument("-e", "--everything", help="displays everything", action="store_true")
	parser.add_argument("-t", "--time", help="displays time and date of data collection", action="store_true")
	return parser.parse_args()

def main():
	try:
		flags = parse_flags()
		print(process_weather_json(flags, get_weather_json(flags)))
	except:
		print("failed to return weather info")

main()

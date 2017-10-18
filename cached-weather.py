#!/usr/bin/python3

import os
import time
import subprocess

# the structure of the weather-cache file
# is one line consisting of the time of last update,
# and another line consisting of the last weather
# string

home_path = "/home/alex/"

def curr_time():
	return int(round(time.time() * 1000))

def update_cache_and_display(weather_file):
	# print("updating cache")
	time_line = str(curr_time())
	weather = subprocess.Popen([home_path + "PathApps/weather.py", "-ol"], stdout=subprocess.PIPE)
	weather_line = weather.stdout.read().decode("utf-8").rstrip()
	weather_file.write(time_line + "\n")
	weather_file.write(weather_line)
	# print("(new) " + weather_line)
	print(weather_line)
	weather_file.close()

def main():
	if os.path.isfile(home_path + ".weather-cache"):
		weather_file = open(home_path + ".weather-cache", 'r+')
		lines = weather_file.read().splitlines()
		five_min_millis = 300000
		curr_time_millis = curr_time()
		cache_time = int(lines[0])
		if (cache_time + five_min_millis) < curr_time_millis:
			# print("more than five minutes")
			# it's been five minutes, update the cache
			weather_file.seek(0)
			weather_file.truncate()
			update_cache_and_display(weather_file)
		else:
			# has been less than five minutes since last query,
			# return cached result
			# print("less than five minutes, reading from cache")
			# print("(cache) " + lines[1])
			print(lines[1])
			weather_file.close()
	else:
		# if there is no cache file, update the cache
		update_cache_and_display(open(home_path + ".weather-cache", 'w'))

main()
# Weather

A simple script for getting weather info from the command line.

NOTE: without supplying a key obtained from [here](https://openweathermap.org/appid) to "your-key-here" this script fails to run. Additionally, the "home_path" variable in "cached-weather.py" should be set to your home, not mine.

If you want to call it anywhere and without prefixing it with "python", make sure you have python3 and the requests module installed then:

1. change `api_key = "your-key-here"` to your actual key
1. `chmod +x weather.py`
2. add this line to your .bashrc or .bash_profile
	`export PATH=/my/directory/with/pythonscript:$PATH`

These steps are covered [here](https://stackoverflow.com/questions/15587877/run-a-python-script-in-terminal-without-the-python-command)

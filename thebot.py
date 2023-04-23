import requests
import datetime
import pytz

# API key for OpenWeatherMap
API_KEY = "aefa79abe1501dc2a523113d7b54d582"

# function to convert UNIX timestamp to local time
def convert_time(timestamp, timezone):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone(timezone))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# get user input for date range and zipcode
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
zipcode = input("Enter your zipcode: ")

# create a list of dates within the range
date_list = []
current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
while current_date <= end_date:
    date_list.append(current_date.strftime("%Y-%m-%d"))
    current_date += datetime.timedelta(days=1)

# iterate through each date and get weather forecast
for date in date_list:
    # create API request URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={zipcode},us&appid={API_KEY}&units=imperial"
    
    # make API request and extract relevant data
    response = requests.get(url).json()
    weather_desc = response['weather'][0]['description']
    high_temp = response['main']['temp_max']
    low_temp = response['main']['temp_min']
    sunrise_time = convert_time(response['sys']['sunrise'], response['timezone'])
    sunset_time = convert_time(response['sys']['sunset'], response['timezone'])
    
    # print out results for each date
    print(f"Date: {date}")
    print(f"Weather Forecast: {weather_desc}")
    print(f"High Temperature: {high_temp} F")
    print(f"Low Temperature: {low_temp} F")
    print(f"Sunrise Time: {sunrise_time}")
    print(f"Sunset Time: {sunset_time}")
    print("===================================")

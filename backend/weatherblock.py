import pgeocode
import requests
import pyzipcode
import datetime
import pytz

weathercodes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    51: "Light Rain Showers",
    53: "Moderate Rain Showers",
    55: "Heavy Rain Showers",
    61: "Light Rain",
    62: "Moderate Rain",
    63: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Moderate Freezing Rain",
    71: "Light Snow Showers",
    73: "Moderate Snow Showers",
    75: "Heavy Snow Showers",
    95: "Thunderstorm",
    95: "Thuderstorm with Hail",
    99: "Thunderstorm with Hail",
}

def get_date_range(start_date, end_date):
    date_range = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)
    return date_range

def unix_convert(unix_time):
    # Convert Unix timestamp to datetime object
    dt = datetime.datetime.fromtimestamp(unix_time)
    
    # Convert to 12-hour time format
    am_pm = "AM" if dt.hour < 12 else "PM"
    hour = dt.hour % 12
    if hour == 0:
        hour = 12
    minute = str(dt.minute).zfill(2)
    return f"{hour}:{minute} {am_pm}"

def date_format_from_american(date_str):
    # Extract month, day, and year components from input string
    month = date_str[0:2]
    day = date_str[2:4]
    year = date_str[4:]
    
    # Format date components as "yyyy-mm-dd"
    date_formatted = f"{year}-{month}-{day}"
    return date_formatted

def date_format_from_iso(date_str):
    # Extract year, month, and day components from input string
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:]
    
    # Format date components as "mm-dd-yyyy"
    date_formatted = f"{month}-{day}-{year}"
    return date_formatted

def zipcode_to_timezone(zipcode):
    # Get latitude and longitude for the ZIP code
    location = pyzipcode.ZipCodeDatabase().get(zipcode)
    # Get timezone for the latitude and longitude
    timezone = pytz.timezone(pytz.country_timezones('us')[0])  # assume ZIP code is in the US
    print(timezone)
    timezone_name = timezone.zone
    
    # Return the timezone name
    return timezone_name


zipcode = input("Enter your zipcode: ")
start = date_format_from_american(input("Enter the start date of your production (mmddyyyy): "))
end = date_format_from_american(input("Enter the end date of your production(mmddyyyy): "))
timezone = "America%2FLos_Angeles"
nomi = pgeocode.Nominatim("us")
latitude = nomi.query_postal_code(zipcode).latitude
longitude = nomi.query_postal_code(zipcode).longitude
date_range = get_date_range(start, end)
timezone = zipcode_to_timezone(zipcode)

response = requests.get(
    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1&start_date={start}&end_date={end}&timezone={timezone}&timeformat=unixtime"
).json()

def print_weather_block():
    print("===================================")
    for day in range (0, len(date_range)):
        print(f"Date: {date_format_from_iso(date_range[day])}")
        print(f"Weather Forecast: {weathercodes[response['daily']['weathercode'][day]]}")
        print(f"High Temperature: {response['daily']['temperature_2m_max'][day]} F")
        print(f"Low Temperature: {response['daily']['temperature_2m_min'][day]} F")
        print(f"Sunrise Time: {unix_convert(response['daily']['sunrise'][day])}")
        print(f"Sunset Time: {unix_convert(response['daily']['sunset'][day])}")
        print("===================================")

print_weather_block()


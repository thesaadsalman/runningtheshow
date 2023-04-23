import pgeocode
import requests

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

nomi = pgeocode.Nominatim("us")


zipcode = input("Enter your zipcode: ")
start = input("Enter the start date of your production (yyyy-mm-dd): ")
end = input("Enter the end date of your production(yyyy-mm-dd): ")
timezone = "America%2FLos_Angeles"

latitude = nomi.query_postal_code(zipcode).latitude
longitude = nomi.query_postal_code(zipcode).longitude

api_response = requests.get(
    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1&start_date={start}&end_date={end}&timezone={timezone}"
)

print(api_response.json())

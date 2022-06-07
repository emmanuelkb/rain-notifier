import requests
import os
from requests.auth import HTTPBasicAuth

weather_api_base_url = "https://api.openweathermap.org/data/2.5/onecall"
request_params = {
    "lat": "5.651656",
    "lon": "-0.160459",
    "exclude": "daily,current",
    "appid": os.environ.get("open_weather_api_key")
}

twilio_api_base_url = "https://api.twilio.com/2010-04-01/Accounts/AC3528cafcdd1aaf6477d291d6bfdeaa22/Messages.json"

response = requests.get(url=weather_api_base_url, params=request_params)
response = response.json()
hourly_for_next_2_days = response['hourly']
hourly_for_next_24_hours = hourly_for_next_2_days[:24]

rain_flag = 0
for hour in hourly_for_next_24_hours:
    if hour['weather'][0]['id'] < 600:
        rain_flag += 1

if rain_flag:
    msg = "High chances of rain today. Stay Safe!"
else:
    msg = "No rain today. Enjoy!"

twilio_body = {"Body": msg,
               "To": os.environ.get("To"),
               "From": os.environ.get("From")}

auth = HTTPBasicAuth('AC3528cafcdd1aaf6477d291d6bfdeaa22', os.environ.get('twilio_api_key'))

print(requests.post(url=twilio_api_base_url, data=twilio_body, auth=auth))

import os
import re
import requests
from datetime import date

# scrape today's page (for yesterday's weather)
today = date.today()
month = today.strftime("%B").lower()
day = today.day
year = today.year
hyslop_url = f'https://agsci.oregonstate.edu/weather/{month}-{day}-{year}'
r = requests.get(hyslop_url)

# extract values from results
regex = r"Ending at Observaton Max:.*?field-item\s.*?>(.*?)</div>"
matches = re.finditer(regex, r.text, re.MULTILINE)
for matchNum, match in enumerate(matches):
    max_temp = match.group(1)

regex = r"Ending at Observaton Min:.*?field-item\s.*?>(.*?)</div>"
matches = re.finditer(regex, r.text, re.MULTILINE)
for matchNum, match in enumerate(matches):
    min_temp = match.group(1)

regex = r"Rain \(in\):.*?field-item\s.*?>(.*?)</div>"
matches = re.finditer(regex, r.text, re.MULTILINE)
for matchNum, match in enumerate(matches):
    rain = match.group(1)

# create pushover notification
title = f"yesterday's max temp was {max_temp}°F"
msg = f"""Max Temp: {max_temp}°F
Min Temp: {min_temp}°F
Rain: {rain} inches
URL: {hyslop_url}
"""
r = requests.post('https://api.pushover.net/1/messages.json', data = {
    'token': os.environ['HYSLOP_PUSHOVER_APP_KEY'],
    'user': os.environ['PUSHOVER_USER_KEY'],
    'message': msg,
    'title': title,
    'url': os.getenv(hyslop_url),
    'device': os.environ['PUSHOVER_DEVICE']
})

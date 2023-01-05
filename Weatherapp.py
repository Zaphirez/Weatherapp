# Importing
import math
import requests

Country_Code = ''
City_Name = ''


def separate_letters_and_numbers(lst):
    global Country_Code
    global City_Name
    for i in lst:
        if i.isnumeric():
            Country_Code += i
        elif i.isalpha():
            City_Name += i
        else:
            return 'Wrong Format'


# My API Key get yours at the Website
apikey = "5df8688079f04145cb27c689c826c670"

# Getting Long and Lat
input_Parameters = input("Input your City Name and Country Code separated by a Comma: ")
split_input_Parameters = input_Parameters.split(", ")
separate_letters_and_numbers(split_input_Parameters)
loc = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={City_Name}, {Country_Code}&limit=5&appid={apikey}")
data = loc.json()
lat = data[0]['lat']
lon = data[0]['lon']

# Getting Weather information
request_weather = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric")
data_w = request_weather.json()
# print(data_w) #DEBUG

# Getting data and Storing it to Variables
w = data_w['weather'][0]['main']
desc = data_w['weather'][0]['description']
Temp = data_w['main']['temp']
fTemp = data_w['main']['feels_like']
mTemp = data_w['main']['temp_min']
maxTemp = data_w['main']['temp_max']
wind_s = math.ceil(
    int(data_w['wind']['speed']) * 1.852)  # Rounding the Numbers also Converting it to km/h del if miles
wind_d = int(data_w['wind']['deg'])  # Needing int for later
hum = data_w['main']['humidity']

# Output
print(f"The current Weather is: {w} \n"
      f"Further info: {desc} \n"
      f"Current Temperature is: {Temp}°C \n"
      f"It Feels like: {fTemp}°C \n"
      f"Minimum Temperature is: {mTemp}°C \n"
      f"Maximum Temperature is: {maxTemp}°C \n"
      f"Humidity is: {hum}% \n"
      f"Wind Speed is: {wind_s}km/h")

# Making 360° also North, and yes you could just print out North but ist more fun this way :)
if wind_d == 360:
    wind_d = 0
# Getting the Wind Directions
if wind_d == 0:
    print(f"Wind Direction is North \n")
elif 0 <= wind_d <= 90:
    print(f"Wind Direction is NE \n")
elif wind_d == 90:
    print(f"Wind Direction is East \n")
elif 90 <= wind_d <= 180:
    print(f"Wind Direction is SE \n")
elif wind_d == 180:
    print(f"Wind Direction is South \n")
elif 180 <= wind_d <= 270:
    print(f"Wind Direction is SW \n")
elif wind_d == 270:
    print(f"Wind Direction is West \n")
elif 270 <= wind_d <= 359:
    print(f"Wind Direction is North West \n")

input("Press Enter to Exit")
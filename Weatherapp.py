# Importing
import customtkinter
import math
import requests

# Global Variables
w = ''
desc = ''
Temp = 0
fTemp = 0
mTemp = 0
maxTemp = 0
wind_s = 0
hum = 0
wind_cd = ''
wind_d = 0
APIKEY = ''
System = ''
City_Info = ''
Country_Code = ''
City_Name = ''
lat = 0
lon = 0
output = ''


# -------------------- FUNCTIONS --------------------

# Function for getting individual Pieces of the input so it doesn't matter which way you input the Country Code and Name
def separate_letters_and_numbers(lst):
    global Country_Code
    global City_Name
    for i in lst:
        if i.isnumeric():
            Country_Code += i
        elif i.isalpha() or " " in i:
            City_Name += i
    if City_Name == '':
        print("Something Went wrong!")
    if Country_Code == '':
        print("Something went wrong!")


# Getting Coords
def get_coords(a, b):
    split_str = a.split(", ")
    separate_letters_and_numbers(split_str)
    # print(f"http://api.openweathermap.org/geo/1.0/direct?q={City_Name},{Country_Code}&limit=5&appid={b}")
    loc = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={City_Name},{Country_Code}&limit=5&appid={b}")
    data = loc.json()
    # print(data) # This is just for me, so I can edit this later if there will be changes in the API Call
    global lat
    lat += data[0]['lat']
    # print(lat)
    global lon
    lon += data[0]['lon']
    # print(lon)


# Getting Weather information
def get_weather_data(a, b, c, d):
    request_weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={a}&lon={b}&appid={c}&units={d}")
    data_w = request_weather.json()
    # print(data_w) # This is just for me, so I can edit this later if there will be changes in the API Call

    # Getting data and Storing it to Variables
    global w
    global desc
    global Temp
    global fTemp
    global mTemp
    global maxTemp
    global wind_s
    global hum
    global wind_cd
    global wind_d
    w += data_w['weather'][0]['main']
    desc += data_w['weather'][0]['description']
    Temp += data_w['main']['temp']
    fTemp += data_w['main']['feels_like']
    mTemp += data_w['main']['temp_min']
    maxTemp += data_w['main']['temp_max']
    wind_s += math.ceil(
        int(data_w['wind']['speed']))  # Rounding the Numbers also Converting it to km/h del if you want miles
    wind_d += int(data_w['wind']['deg'])  # Needing int for later
    hum += data_w['main']['humidity']
    # Making 360° = 0, and yes you could just print out North but its more fun this way :)
    if wind_d == 360:
        wind_d -= wind_d
    # Getting the Wind Directions
    if wind_d == 0:
        wind_cd += 'North'
    elif 0 <= wind_d <= 90:
        wind_cd += 'North East'
    elif wind_d == 90:
        wind_cd += 'East'
    elif 90 <= wind_d <= 180:
        wind_cd += 'South East'
    elif wind_d == 180:
        wind_cd += 'South'
    elif 180 <= wind_d <= 270:
        wind_cd += 'South West'
    elif wind_d == 270:
        wind_cd += 'West'
    elif 270 <= wind_d <= 359:
        wind_cd += 'North West'


def reset_variables():
    global Country_Code
    global City_Name
    global lat
    global lon
    global w
    global desc
    global Temp
    global fTemp
    global mTemp
    global maxTemp
    global wind_s
    global hum
    global wind_cd
    global wind_d
    global System
    global APIKEY
    global City_Info
    global output
    w = ''
    desc = ''
    Temp = 0
    fTemp = 0
    mTemp = 0
    maxTemp = 0
    wind_s = 0
    hum = 0
    wind_cd = ''
    wind_d = 0
    APIKEY = ''
    System = ''
    City_Info = ''
    Country_Code = ''
    City_Name = ''
    lat = 0
    lon = 0
    output = ''


# ------------------   GUI   ------------------------

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")
root.title("Weather-App")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Weather-App", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="API Key", show="*")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Postal Code, City Name")
entry2.pack(pady=12, padx=10)

dropdown = customtkinter.CTkComboBox(master=frame, values=["Metric", "Imperial"])
dropdown.pack(pady=12, padx=10)


def get_info():
    global APIKEY
    global System
    global City_Info
    global output
    APIKEY += entry1.get()
    City_Info += entry2.get()
    System += dropdown.get().lower()
    if APIKEY == '':
        APIKEY += '5df8688079f04145cb27c689c826c670'
    # print(APIKEY)
    # print(System)
    # print(City_Info)
    # print("Ready!")
    get_coords(City_Info, APIKEY)
    get_weather_data(lat, lon, APIKEY, System)
    if System == "metric":
        output = (
                f"The current Weather is: {w} \n" +
                f"Further info: {desc} \n" +
                f"Current Temperature is: {Temp}°C \n" +
                f"It Feels like: {fTemp}°C \n" +
                f"Minimum Temperature is: {mTemp}°C \n" +
                f"Maximum Temperature is: {maxTemp}°C \n" +
                f"Humidity is: {hum}% \n" +
                f"Wind Speed is: {wind_s}km/h \n" +
                f"Wind Direction is: {wind_cd}")
    else:
        output = (f"The current Weather is: {w} \n" +
                  f"Further info: {desc} \n" +
                  f"Current Temperature is: {Temp}°F \n" +
                  f"It Feels like: {fTemp}°F \n" +
                  f"Minimum Temperature is: {mTemp}°F \n" +
                  f"Maximum Temperature is: {maxTemp}°F \n" +
                  f"Humidity is: {hum}% \n" +
                  f"Wind Speed is: {wind_s}mp/h \n" +
                  f"Wind Direction is: {wind_cd}")


def gui_output(a):
    output_window = customtkinter.CTkToplevel(root)
    output_window.title("Weatherdata")
    output_window.geometry("500x350")

    output_label = customtkinter.CTkLabel(master=output_window, text="This is the current Weather Information!")
    output_label.pack(pady=12, padx=10)
    output_label1 = customtkinter.CTkLabel(master=output_window, text=a)
    output_label1.pack(pady=12, padx=10)


def output_command():
    get_info()
    gui_output(output)
    reset_variables()


button = customtkinter.CTkButton(master=frame, text="Get Info", command=output_command)
button.pack(pady=12, padx=10)

root.mainloop()

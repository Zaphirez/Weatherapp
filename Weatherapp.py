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
def separate(lst):
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
def get_coords(city_information_combined, key):
    split_str = city_information_combined.split(", ")
    separate(split_str)
    # print(f"http://api.openweathermap.org/geo/1.0/direct?q={City_Name},{Country_Code}&limit=5&appid={b}")
    loc = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={City_Name},{Country_Code}&limit=5&appid={key}")
    data = loc.json()
    # print(data) # Printing the Data for looking into API Problems
    global lat
    lat += data[0]['lat']
    # print(lat) # Same Here
    global lon
    lon += data[0]['lon']
    # print(lon) # Same Here


# Getting Weather information
def get_weather_data(latitude, longitude, key, sys):
    request_weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}&units={sys}")
    data_w = request_weather.json()
    # print(data_w) # Also for Debugging

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
        int(data_w['wind']['speed']))
    wind_d += int(data_w['wind']['deg'])  # Needing int for later
    hum += data_w['main']['humidity']

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
    elif wind_d == 360:
        wind_cd += 'North'


# Resets Variables
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

# Basic Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Main Window
root = customtkinter.CTk()
root.geometry("500x350")
root.title("Weather-App")

# Frame for Centering and for the looks
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Headline
label = customtkinter.CTkLabel(master=frame, text="Weather-App", font=("Roboto", 24))
label.pack(pady=12, padx=10)

# Input for API KEY censoring it because why not
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="API Key", show="*")
entry1.pack(pady=12, padx=10)

# Input for City Information
entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Postal Code, City Name")
entry2.pack(pady=12, padx=10)

# Choice between Metric and Imperial System
dropdown = customtkinter.CTkComboBox(master=frame, values=["Metric", "Imperial"])
dropdown.pack(pady=12, padx=10)


# Gets the Weather information and saves it to the output variable used for the Output Window
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
    # print(APIKEY) # DEBUGGING
    # print(System) # DEBUGGING
    # print(City_Info) # DEBUGGING
    # print("Ready!") # DEBUGGING
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


# Used for storing the open windows
open_windows = []


# Makes the Output window as a TopLevel text is used from the variable or Text passed to the Function
def gui_output(a):
    global open_windows
    output_window = customtkinter.CTkToplevel(root)
    output_window.title("Weatherdata")
    output_window.geometry("500x350+500+100")

    output_label = customtkinter.CTkLabel(master=output_window, text="This is the current Weather Information!")
    output_label.pack(pady=12, padx=10)
    output_label1 = customtkinter.CTkLabel(master=output_window, text=a)
    output_label1.pack(pady=12, padx=10)
    open_windows.append(output_window)


# Function for making multiple Commands possible per Button
def output_command():
    get_info()
    gui_output(output)
    reset_variables()


# Closes all the open windows except for the main Window
def close_all():
    global open_windows
    for i in open_windows:
        i.destroy()
    open_windows = []


# Button for Making the Output Window
button = customtkinter.CTkButton(master=frame, text="Get Info", command=output_command)
button.pack(pady=12, padx=10)

# Button for Closing all the Open Windows
button1 = customtkinter.CTkButton(master=frame, text="Close All", command=close_all)
button1.pack(pady=12, padx=10)

root.mainloop()

from tkinter import *
import requests
import json
import datetime as DT
from PIL import Image, ImageTk, ImageEnhance

class WeatherApp:
    def icon_path(self, result):
        weather_main_description = {
            "Clear": "clear-sky.png",
            "Clouds": "cloud.png",
            "Rain": "cloudy(1).png",
            "Snow": "snowy.png",
            "Drizzle": "drizzle.png",
            "Mist": "fog.png",
            "Thunderstorm": "thunderstorm(1).png"
        }        
        if result in weather_main_description:
            print(f"Found \n {weather_main_description[result]}")
            return weather_main_description[result]
        else:
            print(f"Not found \n {result} \n {weather_main_description[result]}")
            return weather_main_description["Clear"]

    def forecast_details_function(self, city_name):
        self.load_forecast_details = PhotoImage(file="forecast.png")
        self.forecast_details = self.bg_canvas.create_image(23, 370, image=self.load_forecast_details, anchor="nw")
        API_KEY = "01d72715cf3a04f79d478fbb7c83dcfb"
        city_name = city_name
        URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&cnt=4"

        api_response = requests.get(URL)
        api_result = api_response.json()
        # print(json.dumps(api_result, indent=4))

        self.forecast_icons = {}

        for i in api_result['list']:
            j = api_result['list'].index(i)
            x = (120 * (j + 1)) + 9
            y = 400
            self.bg_canvas.create_text(x, y, text=f"{i['dt_txt'][11:16]}", fill="white", font=("Oswald", 14))
            x = (130 * (j + 1)) - 60
            icon_name = f"icon{j}"
            y = 405
            self.forecast_icons[icon_name] = PhotoImage(file=self.icon_path(i['weather'][0]['main'])).subsample(5)
            self.bg_canvas.create_image(x, y, image=f"{self.forecast_icons[icon_name]}", anchor='nw')
            x = 125 * (j + 1)
            y = 525
            to_cel = int(i['main']['temp']) - 273.15
            self.bg_canvas.create_text(x, y, text=f"{round((to_cel), 1)}",fill="white", font=('Ariel', 14))

    def display_false(self):
        todays_date = DT.date.today()
        city_name = self.city_entry.get()
        self.city_name = city_name
        if city_name != "":
            api_key = "85971a067dd524d514061870d1d1502c"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

            response = requests.get(url)
            result = response.json()
            # print(json.dumps(result, indent=4))
            print(f"{result['weather'][0]['main']}, \n{result['weather'][0]['description']}")

            self.display_city = self.bg_canvas.create_text(150, 100, text=f"{result['name']}", fill="white", font=("Ariel", 30, 'bold'))
            day_names = {
                0: "Monday",
                1: "Tuesday",
                2: "Wednesday",
                3: "Thursday",
                4: "Friday",
                5: "Saturday",
                6: "Sunday",
            }
            today = DT.datetime.today()
            print(day_names[today.weekday()])
            self.display_day = self.bg_canvas.create_text(150, 130, text=f"{day_names[today.weekday()]}, {DT.datetime.now().date()}", fill="white", font=("Verdana", 9, 'bold'))

            temp_to_celsuis = int(result["main"]['temp']) - 273.15
            self.temp = self.bg_canvas.create_text(150, 220, text=f"{round((temp_to_celsuis), 1)}", fill="white", font=("Oswald", 65, 'bold'))
            min_temp_to_celsuis = int(result["main"]['temp_min']) - 273.15
            self.max_temp = self.bg_canvas.create_text(100, 275, text=f"{round((min_temp_to_celsuis), 1)}", fill="white", font=("Oswald", 15))
            max_temp_to_celsuis = int(result["main"]['temp_max']) - 273.15
            self.min_temp = self.bg_canvas.create_text(200, 275, text=f"{round((max_temp_to_celsuis), 1)}", fill="white", font=("Oswald", 15))

            self.load_icon = PhotoImage(file=f"{self.icon_path(result['weather'][0]['main'])}").subsample(2)
            self.create_icon = self.bg_canvas.create_image(370, 100, image=self.load_icon, anchor="nw")
            self.weather_description_forecast = self.bg_canvas.create_text(150, 300, text=f"{result['weather'][0]['description']}", fill="white", font=("Verdana", 16))    

            self.forecast_details_function(self.city_name)

            self.load_more_details = PhotoImage(file="more_details.png")
            self.more_weather_details = self.bg_canvas.create_image(23, 560, image=self.load_more_details, anchor="nw")
            self.weather_description_description = self.bg_canvas.create_text(312, 590, text=f"Description:     \t\t{result['weather'][0]['description']}", fill="white", font=("Verdana", 16)) 
            self.weather_description_wind = self.bg_canvas.create_text(261, 625, text=f"Wind Speed:   \t\t{result['wind']['speed']}", fill="white", font=("Verdana", 16)) 
            self.weather_description_humidity = self.bg_canvas.create_text(250, 657, text=f"Humidity:  \t\t{result['main']['humidity']}", fill="white", font=("Verdana", 16)) 
            self.weather_description_pressure = self.bg_canvas.create_text(265, 690, text=f"Pressure: \t\t\t{result['main']['pressure']}", fill="white", font=("Verdana", 16)) 
            self.weather_description_visibility = self.bg_canvas.create_text(273, 723, text=f"Viibility:\t\t\t{result['visibility']}", fill="white", font=("Verdana", 16)) 
            self.weather_description_sea_level = self.bg_canvas.create_text(265, 760, text=f"Sea Level:\t\t\t{result['main']['sea_level']}", fill="white", font=("Verdana", 16)) 
            print(self.displaying)
            self.displaying = True
            print(self.displaying)

    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("650x850+600+100")
        image_background = Image.open("background2.png")
        self.image_bg = ImageTk.PhotoImage(image_background)


        self.bg = PhotoImage(file = "background5.png") 

        self.bg_canvas = Canvas(self.root, width=650, height=850)
        self.bg_canvas.pack(fill=BOTH, expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.oval_canvas1 = self.bg_canvas.create_oval(60, 70, 100, 20, fill="white", outline="")
        self.oval_canvas2 = self.bg_canvas.create_oval(480, 70, 520, 20, fill="white", outline="")
        self.rect_canvas = self.bg_canvas.create_rectangle(80, 70, 500, 20, fill="white", outline="")

        self.displaying = False

        def search_city_temp():
            if self.displaying == True:
                elements_to_delete = [
                    self.display_city,
                    self.display_day,
                    self.temp,
                    self.max_temp,
                    self.min_temp,
                    self.create_icon,
                    self.weather_description_forecast,
                    self.more_weather_details,
                    self.weather_description_description,
                    self.weather_description_wind,
                    self.weather_description_humidity,
                    self.weather_description_pressure,
                    self.weather_description_visibility,
                    self.weather_description_sea_level,
                ]
                for element in elements_to_delete:
                    self.bg_canvas.delete(element)
                print(self.displaying)
                self.displaying = False
                print(self.displaying)
                self.display_false()
            else:       
                self.display_false()
                
        def future_forecast():
                api_key = "85971a067dd524d514061870d1d1502c"
                url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"

                response = requests.get(url)
                result = response.json()
                print(json.dumps(result, indent=4))

                for i in result['list']:
                    if str(i["dt_txt"][:10]) == str(todays_date):
                        print("COMPATIBLE")
                    else:
                        print(i["dt_txt"][:10])
                        print(str(i["dt_txt"][:10]), str(todays_date))               

        self.city_entry = Entry(self.root, text="", width=29, bg="white", fg="black", font=("poppins", 18), justify="left", highlightthickness=0, borderwidth=0)
        self.city_entry.place(x=70, y=29)
        self.city_entry.focus()
        self.city_entry_btn = Button(self.root, text="Search", bg="white", fg="black", font=("Ariel", 10), command=lambda: search_city_temp())
        self.city_entry_btn.place(x=550, y=30)



def main():
    root = Tk()
    classInstance = WeatherApp(root)
    root.mainloop()     

if __name__ == "__main__":
    main()

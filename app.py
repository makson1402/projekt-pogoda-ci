from flask import Flask, render_template, request
import datetime
import requests
import logging
import sys

app = Flask(__name__)

# Konfiguracja autora
AUTHOR_INFO = {
    "imie_nazwisko": "Maksym Shylepnytskyi",
    "port": 5000
}

# Logowanie informacji przy starcie
print(f"--- LOGI STARTOWE ---")
print(f"Data uruchomienia: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Autor programu: {AUTHOR_INFO['imie_nazwisko']}")
print(f"Port TCP: {AUTHOR_INFO['port']}")
print(f"---------------------------")
sys.stdout.flush()

# Dane miasta do wyboru
LOCATIONS = {
    "Polska": ["Warszawa", "Krakow", "Wroclaw"],
    "Niemcy": ["Berlin", "Monachium"],
    "USA": ["New York", "Los Angeles"]
}

# Koordynaty miast
COORDS = {
    "Warszawa": (52.23, 21.01), "Krakow": (50.06, 19.94), "Wroclaw": (51.10, 17.03),
    "Berlin": (52.52, 13.40), "Monachium": (48.13, 11.58),
    "New York": (40.71, -74.00), "Los Angeles": (34.05, -118.24)
}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    selected_city = None
    if request.method == 'POST':
        selected_city = request.form.get('city')
        lat, lon = COORDS.get(selected_city, (52.23, 21.01))
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                weather = response.json().get('current_weather')
        except Exception as e:
            print(f"Błąd API: {e}")

    return render_template('index.html', locations=LOCATIONS, weather=weather, city=selected_city)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=AUTHOR_INFO['port'])
# =========================================
# app.py (Two-Route Version)
# =========================================
import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Application Setup ---
app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# --- Route for the Home Page (shows the form ) ---
@app.route('/')
def index():
    """Renders the main page with the city search form."""
    return render_template('index.html')

# --- Route for Displaying the Weather ---
@app.route('/weather', methods=['POST'])
def get_weather():
    """
    Processes the form submission, fetches API data, and renders the
    weather results page.
    """
    city = request.form.get('city')
    error = None
    weather_data = None

    # --- Input Validation ---
    if not city:
        error = "Please enter a city name."
        return render_template('index.html', error=error)
    
    # --- API Key Check ---
    if not API_KEY:
        app.logger.error("OpenWeatherMap API key is not configured.")
        error = "Server configuration error: API key is missing."
        # Render the weather page with an error, as the user already submitted
        return render_template('weather.html', error=error)

    # --- API Call ---
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        
        # --- Handle API Response ---
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1), # m/s to km/h
                'feels_like': round(data['main']['feels_like']),
                'pressure': data['main']['pressure']
            }
        elif response.status_code == 404:
            error = f"City '{city}' not found. Please go back and try again."
        else:
            # For other API errors (500, 401, etc.)
            error = "Weather service is currently unavailable. Please try again later."
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Network error occurred: {e}")
        error = "Network error. Could not connect to the weather service."

    # Render the results on the dedicated weather.html page
    return render_template('weather.html', weather=weather_data, error=error, city=city)

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)

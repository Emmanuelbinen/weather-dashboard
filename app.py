from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

#Thi is our openweathermap API key
API_KEY = "de2d5eeb5277d4a6e3fe79fb9d6c67ea"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    
    # OpenWeatherMap API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        # Make the API request
        response = requests.get(url)
        data = response.json()
        
        # Check if city was found
        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'feels_like': round(data['main']['feels_like']),
                'pressure': data['main']['pressure']
            }
            return render_template('index.html', weather=weather_data)
        else:
            error = "City not found. Please try again."
            return render_template('index.html', error=error)
            
    except Exception as e:
        error = "Something went wrong. Please try again."
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
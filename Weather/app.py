from flask import Flask, request, jsonify, render_template, make_response
import requests, time

app = Flask(__name__)

API_KEY = 'd4ee3f3370c3c8823b5e72b88a33ac19'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return render_template('index.html', error='Please enter the correct city name')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('index.html', error=f'Unable to obtain weather data for {city}, please ensure the city name is correct')

    data = response.json()
    weather = {
        'City': city.title(),
        'Temperature': f"{round(data['main']['temp'])}°C",
        'Description': data['weather'][0]['description'].capitalize(),
        'Humidity': f"{data['main']['humidity']}%",
        'Pressure': f"{data['main']['pressure']} hPa",
        'Wind Speed': f"{data['wind']['speed']} m/s",
        'Cloudiness': f"{data['clouds']['all']}%",
        'Sunrise': time.strftime('%H:%M:%S', time.localtime(data['sys']['sunrise'])),
        'Sunset': time.strftime('%H:%M:%S', time.localtime(data['sys']['sunset'])),
        'Visibility': f"{data.get('visibility', 'N/A')} meters",
        'Wind Direction': f"{data['wind']['deg']} degrees",
        'Max Temperature': f"{round(data['main']['temp_max'])}°C",
        'Min Temperature': f"{round(data['main']['temp_min'])}°C",
        'Feels Like': f"{round(data['main']['feels_like'])}°C"
    }
    response = make_response(jsonify(weather))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(debug=True)

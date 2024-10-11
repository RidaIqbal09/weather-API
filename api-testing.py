from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


app = Flask(__name__)


# Get API key from .env
API_KEY = os.getenv('WEATHER_API_KEY')


# Define a route for searching weather by city and country
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    country = request.args.get('country')


    if not city or not country:
        return jsonify({'error': 'City and country parameters are required'}), 400


    # Make API request to weather service
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric'
    response = requests.get(url)


    if response.status_code != 200:
        return jsonify({'error': 'Location not found or service unavailable'}), response.status_code


    data = response.json()


    # Extract temperature from the response
    temperature = data['main']['temp']


    # Return the temperature in Celsius
    return jsonify({
        'city': city,
        'country': country,
        'temperature': f'{temperature}°C'
    })


if __name__ == '__main__':
    app.run(debug=True)

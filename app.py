import os
from dotenv import load_dotenv
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


# Create the database tables
db.create_all()
# Class for location
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

#app route for city routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        if new_city: #if new city is not false or empty, add city to db
            add_city = City(name=new_city)

            db.session.add(add_city)
            db.session.commit()
    #else if city is GET request, query all (get all)
    cities = City.query.all()
    #get city from this url
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c894c181252e4d55a49fc2e87a6c2cf4'
    #inititialize where to store the data for later
    weather_data = []

    #iterate over
    for city in cities:
        # make a requests
        req = requests.get(url.format(city.name)).json()
        #data to be collected
        weather = {
            'city' : city.name,
            'temperature' : req['main']['temp'],
            'description' : req['weather'][0]['description'],
            'icon' : req['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('home.html', weather_data=weather_data)
if __name__ == '__main__': 
    db.create_all()
    app.run(debug=True)
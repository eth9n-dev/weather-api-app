from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main_page():
    # API KEY
    key = 'f5e13fbda78847db87d62048231612'

    # API Endpoint
    URL = 'http://api.weatherapi.com/v1/current.json'
    
    if request.method == 'POST':
        if request.form['zipcode']:
            location = request.form['zipcode']
            PARAMS = {'key': key, 'q': location, 'aqi': 'no'}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

            if r.status_code == 200:
                city = data['location']['name']
                state = data['location']['region']
                local_time = data['location']['localtime']
                temperature_f = data['current']['temp_f']
                temperature_c = data['current']['temp_c']
                condition = data['current']['condition']['text']

                return render_template("weather.html", city=city, state=state, local_time=local_time, temperature_f=temperature_f, temperature_c=temperature_c,
                                       condition=condition) 

            else:
                print('Error, Status Code: ' + str(r.status_code))

    return render_template("home.html")

    app = main_page()
    app.run(host="127.0.0.1", port=5000, debug=True)

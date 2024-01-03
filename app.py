from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
load_dotenv()

@app.route("/", methods=['GET', 'POST'])
def main_page():
    # API KEY
    key = os.getenv('API_KEY')

    # API Endpoint
    URL = os.getenv('API_ENDPOINT')
    
    if request.method == 'POST':
        if request.form['zipcode']: # Ensure we receive a valid location to send to the API
            location = request.form['zipcode']
            PARAMS = {'key': key, 'q': location, 'aqi': 'no'}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

            if r.status_code == 200: # Valid response
                city = data['location']['name']
                state = data['location']['region']
                local_time = data['location']['localtime']
                temperature_f = data['current']['temp_f']
                temperature_c = data['current']['temp_c']
                condition = data['current']['condition']['text']
                
                # weather condition checks
                if 'snow' in condition:
                    return render_template("snow.html", city=city, state=state, local_time=local_time, temperature_f=temperature_f, temperature_c=temperature_c,
                                       condition=condition) 
                
                if 'rain' in condition:
                    return render_template("rain.html", city=city, state=state, local_time=local_time, temperature_f=temperature_f, temperature_c=temperature_c,
                                       condition=condition)
                
                else:
                    return render_template("fallback.html", city=city, state=state, local_time=local_time, temperature_f=temperature_f, temperature_c=temperature_c,
                                       condition=condition)

            else:
                print('Error, Status Code: ' + str(r.status_code))
                return render_template("home.html", error=True)

    return render_template("home.html")

    app = main_page()
    app.run(host="127.0.0.1", port=5000, debug=True)


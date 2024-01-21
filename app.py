from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd

model = pickle.load((open("model.pkl", "rb")))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        dep_date = request.form.get('Dep_Time')

        day = int(pd.to_datetime(dep_date, format='%Y-%m-%dT%H:%M').day)
        month = int(pd.to_datetime(dep_date, format='%Y-%m-%dT%H:%M').month)

        dep_hour = int(pd.to_datetime(dep_date, format='%Y-%m-%dT%H:%M').hour)
        dep_min = int(pd.to_datetime(dep_date, format='%Y-%m-%dT%H:%M').minute)

        arrival_date = request.form.get('Arrival_Time')

        arrival_hour = int(pd.to_datetime(arrival_date, format='%Y-%m-%dT%H:%M').hour)
        arrival_min = int(pd.to_datetime(arrival_date, format='%Y-%m-%dT%H:%M').hour)

        dur_hour = abs(arrival_hour - dep_hour)
        dur_min = abs(arrival_min - dep_min)

        Total_stops = int(request.form["stops"])

        airline = request.form.get('airline')
        airlineCheck={'IndiGo':3.0, 'Air India':1.0, 'Jet Airways':4.0, 'SpiceJet':8.0,
       'Multiple carriers':6.0, 'GoAir':2.0, 'Vistara':10.0, 'Air Asia':0.0,
       'Vistara Premium economy':11.0, 'Jet Airways Business':5.0,
       'Multiple carriers Premium economy':7.0, 'Trujet':9.0}

        source = request.form["Source"]
        sourceCheck={'Banglore':0.0, 'Kolkata':3.0, 'Delhi':2.0, 'Chennai':1.0, 'Mumbai':4.0}


        destination = request.form["Destination"]
        destinationCheck={'New Delhi':5.0, 'Banglore':0.0, 'Cochin':1.0, 'Kolkata':4.0, 'Delhi':2.0, 'Hyderabad':3.0}


        prediction = model.predict(
            [[airlineCheck[airline],sourceCheck[source],destinationCheck[destination],Total_stops,8.0, day, month, dep_hour, dep_min, arrival_hour, arrival_min, dur_hour, dur_min]])
        '''prediction = model.predict(
            [[1.0,0.0,5.0,0,24,3,22,20,1,10,2,50]])'''
        output = round(prediction[0], 2)
        print(output)
        return render_template('home.html', prediction_text=f"Your Flight price is Rs. {output}")


app.run(debug=True)
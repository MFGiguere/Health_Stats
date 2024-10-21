"""
source .venv/Scripts/activate
export FLASK_DEBUG=1
flask run
"""

from flask import Flask, render_template, make_response
import csv, re
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def data_wrangle():
    df = pd.read_csv('strava_activities.csv')
    # distance to numeric format
    df['distance'] = pd.to_numeric(df['distance']) 
    # distance to km
    df['distance'] = df['distance']/1000 
    df['elapsed_time'] = df['elapsed_time']/(60*60)
    df['speed'] = df['distance']/df['elapsed_time']
    # start_date_local to date format
    df['start_date_local'] = pd.to_datetime(df['start_date_local'])
    df.replace("VirtualRide", "Ride")
    df.replace("VirtualRun", "Run")
    df.loc[~df["type"].isin(['Ride', 'Run', 'Swim']), "type"] = "Other"

    df.loc[(df['start_date_local'] >= '2024-01-01')]

    df = df.set_index('start_date_local')
    summed_df = df.groupby([pd.Grouper(freq='ME'), 'type']).sum()\
                .reset_index().pivot(index='start_date_local', columns='type', values='elapsed_time')

    summed_df = df.groupby([pd.Grouper(freq='ME'), 'type'])['speed'].mean()\
            .reset_index().pivot(index='start_date_local', columns='type', values='speed')

    summed_df.plot()
    plt.show()




"Create some categories and basic work"
category = ["Health", "Sports", "Socio-demographic", "Nutrition", "Social habits"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html', category=category)

@app.route('/admin')
def admin():
    data = "import something from csv"
    return render_template(f'admin.html', category=category)

@app.route('/<cat>')
def display(cat):
    data = "import something from csv"
    return make_response(render_template(f'category.html', cat=cat, category=category))

if __name__ == '__main__':
   app.run(debug=True)   
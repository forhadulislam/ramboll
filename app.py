from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__, static_url_path='')

data = None

def loadCSV():
    data = pd.read_csv("../waltti.csv", low_memory=False)
    data = data.reindex(columns=['stopid', 'Alue', 'productnumber1' ])
    return data
    
data = loadCSV()
    
@app.route("/")
def home():
    return render_template('index.html' )

@app.route("/api/v1/get-stopid")
def getStopid():
    stops = data.loc[~data['stopid'].duplicated()]
    out = stops.to_json(orient='records')[1:-1].replace('},{', '} {')
    return out
    
@app.route("/api/v1/get-card")
def getCard():
    stops = data.loc[~data['stopid'].duplicated()]
    out = stops.to_json(orient='records')[1:-1].replace('},{', '} {')
    return out

if __name__ == "__main__":
    app.run()
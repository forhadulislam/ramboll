from flask import Flask, render_template, jsonify, Response
import pandas as pd
import numpy as np
import json

app = Flask(__name__, static_url_path='')
JSON = "application/json"
data = None

def loadCSV():
    data = pd.read_csv('../waltti.csv', quotechar='"', low_memory=False)
    data.loc[:, 'lat'] = 0
    data.loc[:, 'lng'] = 0
    data = data.reindex(columns=['lineid','stopid', 'lat', 'lng', 'variation', 'zone', 'age_group' ])
    data.assign(price = lambda x: 0)    
    return data
    
data = loadCSV()

# Loading the Stops
stdata = pd.read_csv('stops.txt', quotechar='"', delimiter=',', low_memory=False)
stdata = stdata.reindex(columns=['stop_id','stop_lat', 'stop_lon'])


# Appending latitude and longitudes to the Main DataFrame
for i, row in stdata.iterrows(): 
    stop_id = int(row['stop_id']) 
    data.loc[(data.stopid == stop_id), 'lat'] = row['stop_lat'] 
    data.loc[(data.stopid == stop_id), 'lng'] = row['stop_lon']    

# Loading Passenger CSV
pdata = pd.read_csv('data/passengersbusstops.csv', delimiter=';', low_memory=False)
pdata = pdata.reindex(columns=['stopid','Freq'])
pdata.loc[:, 'lat'] = 0
pdata.loc[:, 'lng'] = 0
    
@app.route("/")
def home():    
    lines = data.loc[~data['lineid'].duplicated()]
    ageGroups = data.loc[~data['age_group'].duplicated()]
    outd = lines.to_dict(orient="index")
    outAgeGroups = ageGroups.to_dict(orient="index")
    
    return render_template('index.html', ageGroups=outAgeGroups, outd=outd )
    
@app.route("/markers")
def marker():
    outd = ""
    return render_template('markers.html', outd=outd )
    
@app.route("/passengersbusstops")
def passengersBusStops():    
    
    for i, row in stdata.iterrows(): 
        stop_id = int(row['stop_id']) 
        pdata.loc[(pdata.stopid == stop_id), 'lat'] = row['stop_lat'] 
        pdata.loc[(pdata.stopid == stop_id), 'lng'] = row['stop_lon']
    
    out = pdata.to_dict(orient="index")
    
    output = []
    
    for a in out:
        output.append(out[a])
    
    return Response(json.dumps(output), 200, mimetype=JSON)

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

@app.route("/api/v1/get/<variation>/<zone>")
def getData(variation, zone):
    filter = data[(data["zone"] == int(zone)) & (data["variation"] == str(variation))]
    out = filter.to_json(orient='records')[1:-1].replace('},{', '} {')  
    
    return out
  
# Get all the lines
@app.route("/api/v1/get/lines")
def getLines():
    lines = data.loc[~data['lineid'].duplicated()]
    out = lines.to_json(orient='records')    
    
    return Response(json.dumps(out), 200, mimetype=JSON)
    
@app.route("/api/v1/get/line-routes/<lineid>")
def getLineRoutes(lineid):
    filter = data[(data["lineid"] == int(lineid))]
    filterout = filter.loc[~filter['stopid'].duplicated()]
    filterout = filterout.reindex(columns=['lat', 'lng'])
    filterout.loc[:, 'users'] = 0
    for i, row in stdata.iterrows():
        stop_id = int(row['stop_id']) 
        data.loc[(data.stopid == stop_id), 'lat'] = row['stop_lat'] 
        data.loc[(data.stopid == stop_id), 'lng'] = row['stop_lon']    
    
    
    out = filterout.to_dict(orient="index")
    
    output = []
    
    for a in out:
        output.append(out[a])
    
    return Response(json.dumps(output), 200, mimetype=JSON)
    #return render_template('data.html', out=output )
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
from flask import Flask, render_template, jsonify, Response
import pandas as pd
import numpy as np
import json

app = Flask(__name__, static_url_path='')
JSON = "application/json"
data = None

def loadCSV():
    data = pd.read_csv('../waltti.csv', quotechar='"', low_memory=False)
    data = data.reindex(columns=['lineid','stopid', 'Alue', 'productnumber1', 'variation', 'zone' ])
    data.assign(price = lambda x: 0)
    return data
    
data = loadCSV()
    
@app.route("/")
def home():
    
    #stops = data.loc[~data['stopid'].duplicated()]
    #stopsJSON = stops.to_json(orient='records')[1:-1]
    lines = data.loc[~data['lineid'].duplicated()]
    #out = lines.to_json(orient='records')[1:-1].replace('},{', '} {')  
    #out = lines.to_json(orient='records')   
    #out = json.dumps(out)
    out= lines.to_html()
    outd= lines.to_dict(orient="index")
    
    return render_template('index.html', lines=out, outd=outd )

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
    #out = lines.to_json(orient='records')[1:-1].replace('},{', '} {')  
    out = lines.to_json(orient='records')    
    
    return Response(json.dumps(out), 200, mimetype=JSON)
    
@app.route("/api/v1/get/line-routes/<lineid>")
def getLineRoutes(lineid):
    filter = data[(data["zone"] == int(zone)) & (data["variation"] == str(variation))]
    out = filter.to_json(orient='records')[1:-1].replace('},{', '} {')
    
if __name__ == "__main__":
    app.run()
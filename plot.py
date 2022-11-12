import pandas as pd
import numpy as np
import plotly.express as px

with open("data/einwohnerzahlen_quartier.csv", 'r') as f:
    einwohnerzahlen = pd.read_csv(f, sep=';')

with open("data/sensor_quartier.csv", 'r') as f:
    sensorposition = pd.read_csv(f, sep=';')

with open("data/glassammelstellen.csv", 'r') as f:
    glassammelstellen = pd.read_csv(f, sep=';')

data = pd.merge(einwohnerzahlen, sensorposition, on='quartier')
count = data['quartier'].value_counts().to_dict()
data['quartier_count'] = data['quartier'].map(count)
data['einwohner_norm'] = (data['einwohner'] / data['quartier_count'])
data = pd.merge(data, glassammelstellen, on='sensorname')
data['score'] = data['einwohner_norm'] / data['menge']

fig = px.density_mapbox(data, lat='lat', lon='lon', z='score',
                        mapbox_style="stamen-terrain")

fig.show()

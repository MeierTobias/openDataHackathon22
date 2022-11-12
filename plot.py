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
data['score'] = data['einwohner_norm'] / data['menge'] * 1000
data['score'] = np.log10(data['score']) * 1000

fig = px.density_mapbox(data, lat='lat',
                        lon='lon',
                        z='score',
                        zoom=12.5,
                        radius=150,
                        opacity=0.6,
                        color_continuous_scale='Portland',
                        mapbox_style="stamen-terrain")
fig.update(layout_coloraxis_showscale=False)
fig.show()


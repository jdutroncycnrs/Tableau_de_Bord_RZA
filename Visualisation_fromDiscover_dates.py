import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import plotly.io as pio


if not os.path.exists(r"data\visualisations\images"):
    os.mkdir(r"data\visualisations\images")

### Récupération des variables
data = pd.read_csv("data\Enregistrements_220424_dates.csv")

data_dates=data[["createDate","_id"]]
data_dates.rename(columns={"createDate":"Date"}, inplace=True)
nb_enregistrements = len(data_dates)
data_dates.dropna(subset="Date" ,inplace=True)

data_dates['Date'] = pd.to_datetime(data_dates['Date'], format='mixed', utc=True)
data_dates.sort_values(by="Date", inplace=True)

data_dates.set_index('Date', inplace=True)
data_dates['unite']=1
data_dates['compte']=data_dates['unite'].cumsum()
nb_enregistrements_visu = len(data_dates)

data_dates_resampled =data_dates.resample(rule="ME").size()


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=data_dates.index, y=data_dates['compte'], name="Cumul d'enregistrements"),secondary_y=False)
fig.add_trace(go.Bar(x=data_dates_resampled.index, y=data_dates_resampled.values, name="Nombre d'enregistrements"),secondary_y=True)
fig.update_layout(title_text=f"évolution temporelle des enregistrements ({nb_enregistrements_visu} /{nb_enregistrements} records)", font_size = 20, showlegend=False)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Nombre cumulé d'enregistrements",title_font=dict(color='Blue'),secondary_y=False)
fig.update_yaxes(title_text="Nombre d'enregistrements",title_font=dict(color='red'),secondary_y=True)
pio.write_image(fig, r"data\visualisations\images", format='png')
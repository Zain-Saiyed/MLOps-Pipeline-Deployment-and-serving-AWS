import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import json
import sys
import os

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from credentials import *

def get_model_metrics_data():
    api_url = API_URL + '/get-latest-staged-model'
    print("api_url",api_url)
    payload = {'flag' : 'all'}
    response = requests.post(api_url, json=payload)
    return response.json()

json_response = json.loads(get_model_metrics_data()['body'])
print(json_response)
st.title('Model Evaluation Dashboard')
json_data=[]
for entry in json_response:
    if entry.get('timestamp') == None:
        entry['timestamp'] = pd.NaT
    else:
        json_data.append(entry)

df = pd.json_normalize(json_data)  
df.columns = [col.split('.')[-1] if '.' in col else col for col in df.columns]

# Convert 'timestamp' column format to readable
df['timestamp'] = pd.to_datetime(df['timestamp'].astype(str), format='%d%m%Y%H%M%S%f').dt.strftime('%d-%m-%Y %H:%M')

df = df.sort_values('timestamp')

st.write(df)

metrics_to_plot = ['auc_roc', 'f1_score', 'accuracy', 'precision', 'recall']  

fig = px.line(df, x='model_id', y=metrics_to_plot, title='Comparison of Metrics Over Time',
              category_orders={"model_id": df.sort_values("timestamp")["model_id"].values})

fig.update_xaxes(title='Model ID')
fig.update_yaxes(title='Value')

# plot figure
st.plotly_chart(fig)
import streamlit as st
import requests
import json
import os, sys

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from credentials import *


def start_training():
    api_url = API_URL+'/start-model-training'
    print("api_url",api_url)
    response = requests.post(api_url)
    print(response.text)
    return response.json()

def get_latest_deployed_model_metrics():
    api_url = API_URL+'/get-latest-staged-model'
    print("api_url",api_url)
    payload = {'flag' : 'latest-staged'}
    response = requests.post(api_url, json=payload)
    print(response.text)
    return json.loads(response.json()['body'])[0]

def accept_reject_model(flag,timestamp):
    api_url = API_URL+'/'+flag+'-staged-model'
    print("api_url",api_url)
    payload = {'timestamp' : timestamp}
    response = requests.post(api_url, json=payload)
    print(response.text)
    return json.loads(response.json()['body'])

st.title('Model Training Pipeline Dashboard')

start_training_flag = False

response = get_latest_deployed_model_metrics()
print(response)
if response["approved"] == False :#and response["training_complete"] == True and (response["timestamp"] != None or response["timestamp"] != "") :
    st.write("Model Details:")
    st.write(response)
    if response["training_complete"] == True:
        if st.button("Accept"):
            response = accept_reject_model("accept", str(response["timestamp"]))
            st.write(response)

        if st.button("Reject"):
            response = accept_reject_model("reject", str(response["timestamp"]))
            st.write(response)
    else:
        st.error("Model training in progress!!")
        st.info('Please wait until Model completes Training to Accept or Reject the Model.')

else:
    col1, col2 = st.columns([1, 1])   
    with col1:
        st.write("Initiate Model Training process:")

    with col2:
        if st.button("START TRAINING"):
            start_training_flag = True

    if start_training_flag:
        training_status = start_training()
        print(training_status)

        if "errorMessage" in training_status.keys():
            if "cannot find the requested image" in training_status["errorMessage"].lower():
                st.error("Please wait until the ECR repository with the training image is initialised before starting Training job!")
        else:
            st.write("Model Training Started")
            training_status = json.loads(training_status['body'])
            st.write("Status    : "+str(training_status['message']))
            st.write("Timestamp : "+str(training_status['timestamp']))

    
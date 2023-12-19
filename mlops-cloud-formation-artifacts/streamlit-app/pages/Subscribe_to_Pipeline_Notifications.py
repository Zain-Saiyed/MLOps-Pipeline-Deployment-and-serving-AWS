import streamlit as st
import requests
import logging 
import json
import os, sys

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from credentials import *

def add_developer_to_get_notiifcations(email_id):
    api_url = API_URL+'/subscribe-user'
    print("api_url",api_url)
    payload = {
        'email_id' : email_id
    }
    try: 
        response = requests.post(api_url, json=payload)
        print(response)
        logging.error(response.json())
        if response.status_code == 200 and json.loads(response.json())["body"]["status"]:
            st.write("")
            st.write('<span style="color:green">User added to notification list successfully!</span>', unsafe_allow_html=True)
        else:
            st.write("")
            st.write('<span style="color:red">Unable to add User! User either already subscribed.</span>', unsafe_allow_html=True)
    except Exception as e:
        print(e)
        st.write("Unable to add User's email ID at the moment. Please try again later!")

st.title('Add Developer email ID for Model Pipeline Notifications:')
st.write("Please enter the User's email ID to Model Pipeline Notifications mailing list.")

user_email = st.text_input('Enter email ID:')

if st.button('Add Email ID'):
    if user_email:
        add_developer_to_get_notiifcations(user_email)
    else:
        st.warning('Please enter a valid email ID!')
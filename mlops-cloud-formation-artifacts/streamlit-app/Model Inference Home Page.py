import streamlit as st
import requests
import io
import base64
from PIL import Image
import uuid
from credentials import *
import json

def get_label(prediction):
    if prediction > 0.5:
        return 'Recyclable'
    else:
        return 'Organic'

def get_probability(prediction_score):
    if prediction_score > 0.5:
        return str(round(prediction_score*100))
    else:
        return str(round((1-prediction_score)*100))

def predict_image(image):
    # Convert image to bytes
    # Reference: https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    api_url = API_URL+'/upload-image-to-s3'
    print("api_url",api_url)
    # Encode the image bytes to base64
    encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')
    # Prepare the payload
    payload = {
        'base64_image' : encoded_image,
        'uuid_key'     : str(uuid.uuid4())
    }
    # Make a POST request to the API endpoint
    response = requests.post(api_url, json=payload)

    label = ""
    # Check the response
    if response.status_code == 200:
        print('Image prediction successful!')
        # print('Prediction Response:', response.json())
        api_url  = API_URL+'/predict'
        print("api_url",api_url)
        response_json = json.loads(response.json())

        key_value = response_json['key']

        # Make a POST request to the API endpoint
        response = requests.post(api_url, json= { 'key' : key_value })
        print(type(response.json()))
        response = response.json()
        if isinstance(response,str):
            response = json.loads(response)

        if "errorType" in response.keys():
            if response["errorType"] == "ValidationError":
                label = None
        else:
            label = get_label(float(response['prediction_result']))+"[ "+get_probability(float(response['prediction_result']))+" % ]"

    else:
        print('Failed to predict image. Status code:', response.status_code)
        print('Error:', response.text)
        label = ""

    return label

# Streamlit app
st.title('Waste Classification - AWS Sagemaker')
st.write('Upload an image for prediction:')

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', width=250, output_format='JPEG')

    # Make prediction when the 'Predict' button is clicked
    if st.button('Predict'):
        prediction = predict_image(image)
        if prediction == None:
            st.error("Please wait until the Model is deployed to the endpoint. Unable to predict image when no Model endpoint deployed.")
        else:
            # Display prediction result
            st.markdown(f'<div style="display: flex; align-items: center;">'
                f'<span style="font-size: 25px;">Prediction:</span>'
                f'<p style="font-size: 80px; margin-left: 10px;">{prediction}</p>'
                f'</div>', unsafe_allow_html=True)

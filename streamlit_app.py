import streamlit as st
import requests

# Set the URL of your FastAPI application
API_URL = "https://api-nvaa.onrender.com/predict"  # Update with your FastAPI URL

# Set the title for the Streamlit app
st.title("Reg Model")

# Input fields for user to enter data using sliders
appearance = st.slider("Select appearance", min_value=0, max_value=101, value=25)
highest_value = st.slider("Select highest Value", min_value=10000, max_value=32000000, value=5_000)

# Button to trigger the prediction
if st.button("Predict Cluster"):
    # Prepare data to send to the FastAPI backend
    input_data = {
        "appearance": appearance,
        "highest_value": highest_value
    }
    
    try:
        # Make a POST request to the FastAPI endpoint
        response = requests.post(API_URL, json=input_data)
        response_data = response.json()
        
        # Debug: Print the full response content
        # st.write(f"Response Content: {response_data}")
        
        # Check the response status
        if response.status_code == 200:
            if 'sale_price_category' in response_data:
                cluster = response_data['sale_price_category']
                st.success(f"The predicted is : {cluster}")
            else:
                st.error("Key 'sale_price_category' not found in the response.")
        else:
            st.error("Error in prediction. Please check your input and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

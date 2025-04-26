# app.py
import streamlit as st
import requests

st.title("Water Potability Prediction App")

st.write("Enter the water properties below to predict if it is potable (safe to drink) or not:")

ph = st.number_input('pH Value', min_value=0.0, max_value=14.0, step=0.01)
hardness = st.number_input('Hardness', min_value=0.0)
solids = st.number_input('Solids', min_value=0.0)
chloramines = st.number_input('Chloramines', min_value=0.0)
sulfate = st.number_input('Sulfate', min_value=0.0)
conductivity = st.number_input('Conductivity', min_value=0.0)
organic_carbon = st.number_input('Organic Carbon', min_value=0.0)
trihalomethanes = st.number_input('Trihalomethanes', min_value=0.0)
turbidity = st.number_input('Turbidity', min_value=0.0)

hardness_ph_interaction = hardness * ph
hardness_Chloramines_Interaction = hardness * chloramines
hardness_Chloramines_Sum = hardness + chloramines
hardness_Chloramines_Difference = hardness - chloramines

if ph < 6.9:
    neutral = 0
    basic = 0
elif 6.9 <= ph <= 7.1:
    neutral = 1
    basic = 0
else:
    neutral = 0
    basic = 1

if st.button('Predict Potability'):
    input_data = {
        "ph": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "Organic_carbon": organic_carbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity,
        "hardness_ph_interaction": hardness_ph_interaction,
        "hardness_Chloramines_Interaction": hardness_Chloramines_Interaction,
        "hardness_Chloramines_Sum": hardness_Chloramines_Sum,
        "hardness_Chloramines_Difference": hardness_Chloramines_Difference,
        "neutral": neutral,
        "basic": basic
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        result = response.json()
        if result['prediction'] == 1:
            st.success('The water is potable (safe to drink).')
        else:
            st.error('The water is not potable (not safe to drink).')
    except Exception as e:
        st.error(f"Error: {e}")

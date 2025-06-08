import streamlit as st
import numpy as np
import pandas as pd
import joblib
import datetime

st.set_page_config(page_title="PET Bottle Demand Predictor", layout="wide")

st.markdown(
    """
    <style>
    body {background-color: #0d47a1; color: white;}
    .stApp {background-color: #0d47a1; color: white;}
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label, .stRadio label {color: white !important;}
    .stButton>button {background-color: white !important; color: #0d47a1 !important; font-weight: bold;}
    .st-bb, .st-cb {color: white !important;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧪 PET Bottle Demand Predictor")

# Load model and preprocessor
model = joblib.load("best_model.pkl")  # Should include preprocessing pipeline

# Region selection
region = st.selectbox("Region", ["South America", "Europe", "North America", "Asia"])

# Blowing Plant based on Region
blowing_plant_map = {
    "South America": ["Port Santos", "Port Balboa"],
    "Europe": ["Antwerp"],
    "North America": ["Los Angeles", "Port of Montreal"],
    "Asia": ["Busan", "Tokyo", "Shangai"]
}
blowing_plant = st.selectbox("Blowing Plant", blowing_plant_map[region])

# Country based on Region
country_map = {
    "South America": ["Brazil", "Panama", "Argentina"],
    "Europe": ["Belgium", "France", "Germany"],
    "North America": ["USA", "Canada", "Mexico"],
    "Asia": ["South Korea", "Japan", "China", "India"]
}
country = st.selectbox("Country", country_map[region])

# Bottle features
pet_capacity = st.selectbox("PET Bottle Capacity", [
    "33cl", "56.8cl", "24 oz", "16 oz", "15cl", "25cl", "10.5 oz", "330ml", "50cl",
    "12 oz", "11 oz", "10 oz", "270ml", "19 oz", "25 oz", "500ml", "44cl", "355ml",
    "8 oz", "8 oz sleek", "310ml", "9 oz", "32 oz", "12 oz sleek"
])

pet_type = st.selectbox("Type", ["Slim", "Embossed", "Sleek", "Standard", "Big Can"])

weight = st.slider("PET Bottle Weight (grams)", min_value=2.5, max_value=27.55, step=0.1)

# Restrict date input between 2020 and 2025
date = st.date_input(
    "Date of Requirement",
    value=datetime.date(2023, 1, 1),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date(2025, 12, 31)
)
year = date.year
month = date.month
day = date.day

# Prediction
if st.button("Predict Volume (Million Pieces)"):
    input_data = {
        "Region": [region],
        "Blowing plant": [blowing_plant],
        "Country": [country],
        "PET bottle capacity": [pet_capacity],
        "Type": [pet_type],
        "PET bottle weight (grams)": [weight],
        "Year": [year],
        "Month": [month],
        "Day": [day]
    }

    input_df = pd.DataFrame(input_data)
    prediction = model.predict(input_df)
    st.success(f"📦 Predicted Demand: **{prediction[0]:.2f} Million Pieces**")

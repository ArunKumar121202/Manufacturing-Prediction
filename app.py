import streamlit as st
import numpy as np
import pandas as pd
import joblib

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
model = joblib.load("best_model.pkl")  # Should include preprocessor
# (Make sure your model pipeline is saved using joblib.dump(pipeline, "best_model_pipeline.pkl"))

# Input fields
region = st.selectbox("Region", ["South America", "Europe", "North America", "Asia"])

blowing_plant_map = {
    "South America": ["Port Santos", "Port Balboa"],
    "Europe": ["Antwerp"],
    "North America": ["Los Angeles", "Port of Montreal"],
    "Asia": ["Busan", "Tokyo", "Shangai"]
}
blowing_plant = st.selectbox("Blowing Plant", blowing_plant_map[region])

country = st.text_input("Country")  # Allow user to enter any country

pet_capacity = st.selectbox("PET Bottle Capacity", [
    "33cl", "56.8cl", "24 oz", "16 oz", "15cl", "25cl", "10.5 oz", "330ml", "50cl",
    "12 oz", "11 oz", "10 oz", "270ml", "19 oz", "25 oz", "500ml", "44cl", "355ml",
    "8 oz", "8 oz sleek", "310ml", "9 oz", "32 oz", "12 oz sleek"
])

pet_type = st.selectbox("Type", ["Slim", "Embossed", "Sleek", "Standard", "Big Can"])

weight = st.slider("PET Bottle Weight (grams)", min_value=2.5, max_value=27.55, step=0.1)

date = st.date_input("Date of Requirement")
year = date.year
month = date.month
day = date.day

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

    input_df = np.array(pd.DataFrame(input_data))

    # Prediction
    prediction = model.predict(input_df)
    st.success(f"📦 Predicted Demand: **{prediction[0]:.2f} Million Pieces**")

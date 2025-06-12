import streamlit as st
import numpy as np
import pandas as pd
import joblib
import datetime

# Page config
st.set_page_config(page_title="PET Bottle Demand Predictor", layout="wide")

# Dummy credentials (you can replace with a proper auth system later)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful! ✅")
            st.rerun()  # ✅ Updated here
        else:
            st.error("Invalid username or password ❌")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.rerun()  # ✅ Updated here

# Logged-in view
def demand_predictor():
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

    # Logout button
    st.button("Logout", on_click=logout)

    # Load model
    model = joblib.load("best_model.pkl")  # Your pre-trained pipeline

    # Input UI
    region = st.selectbox("Region", ["South America", "Europe", "North America", "Asia"])

    blowing_plant_map = {
        "South America": ["Port Santos", "Port Balboa"],
        "Europe": ["Antwerp"],
        "North America": ["Los Angeles", "Port of Montreal"],
        "Asia": ["Busan", "Tokyo", "Shangai"]
    }
    blowing_plant = st.selectbox("Blowing Plant", blowing_plant_map[region])

    country_map = {
        "South America": ["Brazil", "Panama", "Argentina"],
        "Europe": ["Belgium", "France", "Germany"],
        "North America": ["USA", "Canada", "Mexico"],
        "Asia": ["South Korea", "Japan", "China", "India"]
    }
    country = st.selectbox("Country", country_map[region])

    pet_capacity = st.selectbox("PET Bottle Capacity", [
        "33cl", "56.8cl", "24 oz", "16 oz", "15cl", "25cl", "10.5 oz", "330ml", "50cl",
        "12 oz", "11 oz", "10 oz", "270ml", "19 oz", "25 oz", "500ml", "44cl", "355ml",
        "8 oz", "8 oz sleek", "310ml", "9 oz", "32 oz", "12 oz sleek"
    ])

    pet_type = st.selectbox("Type", ["Slim", "Embossed", "Sleek", "Standard", "Big Can"])

    weight = st.slider("PET Bottle Weight (grams)", min_value=2.5, max_value=27.55, step=0.1)

    date = st.date_input(
        "Date of Requirement",
        value=datetime.date(2023, 1, 1),
        min_value=datetime.date(2019, 1, 3),
        max_value=datetime.date(2023, 12, 31)
    )

    year, month, day = date.year, date.month, date.day

    if st.button("Predict Volume (Million Pieces)"):
        input_df = pd.DataFrame({
            "Region": [region],
            "Blowing plant": [blowing_plant],
            "Country": [country],
            "PET bottle capacity": [pet_capacity],
            "Type": [pet_type],
            "PET bottle weight (grams)": [weight],
            "Year": [year],
            "Month": [month],
            "Day": [day]
        })

        prediction = model.predict(input_df)
        st.success(f"📦 Predicted Demand: **{prediction[0]:.2f} Million Pieces**")

# App control
if st.session_state.logged_in:
    demand_predictor()
else:
    login()

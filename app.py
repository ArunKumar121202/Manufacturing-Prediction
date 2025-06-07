import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page setup
st.set_page_config(page_title="PET Bottle Demand Predictor", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    body {background-color: #263238; color: white;}
    .stApp {background-color: #263238; color: white;}
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stRadio label, .st-bb, .st-cb {color: white !important;}
    .stButton>button {background-color: white !important; color: #263238 !important; font-weight: bold;}
    .welcome-text {color: #ffca28; font-weight: bold; font-size: 18px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Dummy credentials
USER_CREDENTIALS = {"Arun": "Loginpage@123"}

# Login function
def login():
    st.title("🔐 Login to Access the Demand Predictor")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.success(f"✅ Welcome, {username}!")
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state["logged_in"] = False
    st.success("You have been logged out")

# Session check
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.title("📦 PET Bottle Demand Predictor")

    if st.button("Logout"):
        logout()

    # Load model and preprocessor
    model = joblib.load("best_pet_demand_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")

    # Inputs
    st.subheader("📥 Enter Feature Values")
    region = st.selectbox("Region", ["North", "South", "East", "West"])  # Adjust based on training data
    country = st.selectbox("Country", ["India", "Nepal", "Sri Lanka"])  # Adjust as needed
    pet_capacity = st.selectbox("PET Bottle Capacity", ["500ml", "1L", "2L"])
    pet_weight = st.number_input("PET Bottle Weight (grams)", min_value=5.0, max_value=100.0, step=1.0)
    bottle_type = st.selectbox("Bottle Type", ["Carbonated", "Non-Carbonated"])
    plant = st.selectbox("Blowing Plant", ["Plant A", "Plant B", "Plant C"])  # Example entries
    year = st.selectbox("Year", [2023, 2024, 2025])
    month = st.selectbox("Month", list(range(1, 13)))
    day = st.selectbox("Day", list(range(1, 32)))

    # Create DataFrame
    input_df = pd.DataFrame([{
        "Region": region,
        "Country": country,
        "PET bottle capacity": pet_capacity,
        "PET bottle weight (grams)": pet_weight,
        "Type": bottle_type,
        "Blowing plant": plant,
        "Year": year,
        "Month": month,
        "Day": day
    }])

    # Prediction
    if st.button("Predict Demand"):
        X_transformed = preprocessor.transform(input_df)
        prediction = model.predict(X_transformed)
        st.success(f"📈 Predicted Volume: **{prediction[0]:.2f} Million Pieces**")

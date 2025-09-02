import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clustering", page_icon="⚓", layout="wide")

# --- LOAD CSS ---
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
.stSlider > label {
    color: white !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 style='text-align: center;'>⚓ ShipSmart Clustering</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Group ships with similar metrics for performance insights.</p>", unsafe_allow_html=True)
st.sidebar.markdown("""<div class="sidebar-title"> <h4> 🚢 ShipSmart</h4>""", unsafe_allow_html=True)

# --- LOAD MODEL, SCALER, FEATURES, MEDIANS ---
try:
    kmeans = load("models/Clustering.pkl")
    scaler = load("models/scaler.pkl")
    num_features = load("models/features.pkl")          # list of numeric features
    feature_medians = load("models/feature_medians.pkl") # dict of median values
except Exception as e:
    st.error(f"Error loading models: {e}")

# --- INPUT SLIDERS ---
st.subheader("Enter Ship Details")
col1, col2 = st.columns(2)

with col1:
    Speed = st.slider("Speed (knots)", 10.0, 25.0, 20.0)
    Distance = st.slider("Distance Traveled (nm)", 50.0, 2000.0, 500.0)
    Cargo = st.slider("Cargo Weight (tons)", 50.0, 2000.0, 1000.0)
    Operational_Cost = st.slider("Operational Cost (USD)", 10097.0, 499735.0, 100000.0)
    Revenue = st.slider("Revenue per Voyage (USD)", 50352.0, 999812.0, 200000.0)

with col2:
    Turnaround = st.slider("Turnaround Time (hours)", 12.0, 72.0, 48.0)
    Engine_Power = st.slider("Engine Power (kW)", 502.0, 2999.0, 5000.0)
    Draft = st.slider("Draft (meters)", 5.0, 15.0, 10.0)
    Weekly_Voyage = st.slider("Weekly Voyage Count", 1, 9, 5)
    Avg_Load = st.slider("Average Load (%)", 50.0, 100.0, 50.0)

# --- PREDICT BUTTON ---
# --- PREDICT BUTTON (Centered + Dark Orange Gradient) ---
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
clicked = st.button("Predict Cluster", key="predict")
st.markdown("""
<style>
/* Center the button container */
div.stButton {
    display: flex;
    justify-content: center;  /* horizontal center */
    margin-top: 20px;
}

/* Style the button */
div.stButton > button:first-child {
    all: unset;
    cursor: pointer;
    padding: 18px 40px;       /* bigger size */
    border-radius: 12px;      /* slightly rounded corners */
    font-weight: bold;
    font-size: 28px;          /* extra large text */
    color: white !important;
    background: linear-gradient(135deg, #FF8C00, #FF4500);  /* dark orange gradient */
    text-align: center;
    transition: 0.3s;
}

/* Hover effect */
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #b34700, #802600);
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Prediction logic ---
if clicked:
    # Create input dataframe
    input_df = pd.DataFrame([{
        "Speed_Over_Ground_knots": Speed,
        "Distance_Traveled_nm": Distance,
        "Cargo_Weight_tons": Cargo,
        "Turnaround_Time_hours": Turnaround,
        "Engine_Power_kW": Engine_Power,
        "Draft_meters": Draft,
        "Operational_Cost_USD": Operational_Cost,
        "Revenue_per_Voyage_USD": Revenue,
        "Weekly_Voyage_Count": Weekly_Voyage,
        "Average_Load_Percentage": Avg_Load
    }])

    # Derived features
    input_df["Avg_Speed"] = input_df["Distance_Traveled_nm"] / (input_df["Turnaround_Time_hours"] + 1e-6)
    input_df["Cargo_per_nm"] = input_df["Cargo_Weight_tons"] / (input_df["Distance_Traveled_nm"] + 1e-6)

    # Fill missing numeric features with median
    for col in num_features:
        if col not in input_df.columns:
            input_df[col] = feature_medians.get(col, 0)

    # Scale and predict
    input_scaled = scaler.transform(input_df[num_features])
    pred_cluster = kmeans.predict(input_scaled)[0]



    # --- Cluster descriptions ---
    cluster_summary = {
        0: "🚀 High Efficiency: Faster voyages with lower operational costs per nautical mile.",
        1: "⚖️ Medium Efficiency: Moderate speed, cargo load, and costs.",
        2: "🐢 Low Efficiency: Slower voyages, higher costs, less cargo carried."
    }

    # --- Friendly names ---
    cluster_names = {
        0: "High Performer 🚀",
        1: "Balanced Performer ⚖️",
        2: "Needs Improvement 🐢"
    }

    # Personalized predicted descriptions
    pred_description = {
        0: "Your ship is performing at top efficiency! Fast voyages with lower operational costs per nautical mile.",
        1: "Your ship is doing well with a balanced performance. Speed, cargo, and costs are all moderate.",
        2: "Your ship is on the slower side. Voyages take longer and operational costs are higher per mile. There’s room for optimization!"
    }

    # --- SHOW RESULT CARD ---
    st.subheader("Predicted Cluster")
    st.markdown(f"""
    <div class="card">
        <h3>⚓ {cluster_names[pred_cluster]}</h3>
        <p>{pred_description[pred_cluster]}</p>
    </div>
    """, unsafe_allow_html=True)


    # --- CLUSTER OVERVIEW ---
    st.markdown("---")
    st.subheader("Cluster Overview")
    col0, col1, col2 = st.columns(3)
    col0.markdown(f"<div class='card blue'><div style='font-size:18px; font-weight:700;'>{cluster_names[0]}</div><p>{cluster_summary[0]}</p></div>", unsafe_allow_html=True)
    col1.markdown(f"<div class='card green'><div style='font-size:18px; font-weight:700;'>{cluster_names[1]}</div><p>{cluster_summary[1]}</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card orange'><div style='font-size:18px; font-weight:700;'>{cluster_names[2]}</div><p>{cluster_summary[2]}</p></div>", unsafe_allow_html=True)

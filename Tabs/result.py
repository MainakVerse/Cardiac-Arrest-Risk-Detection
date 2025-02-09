import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to visualize health metrics
def app():
    st.title("📊 Patient Health Metrics Dashboard")

    # Set global style for neon-like effect
    plt.style.use("dark_background")

    # Simulated glucose level data (With & Without Medication)
    days = np.arange(1, 31)
    glucose_no_med = np.random.normal(loc=180, scale=20, size=len(days))
    glucose_with_med = glucose_no_med - np.random.normal(loc=40, scale=10, size=len(days))
    
    # Line chart: Glucose trend with & without medication
    fig, ax = plt.subplots()
    ax.set_facecolor("black")
    ax.plot(days, glucose_no_med, marker='o', linestyle='-', label='Without Medication', color='#FF00FF')  # Neon pink
    ax.plot(days, glucose_with_med, marker='s', linestyle='--', label='With Medication', color='#00FFFF')  # Neon cyan
    ax.set_title("Heart Attack Trend", color='white')
    ax.set_xlabel("Days", color='white')
    ax.set_ylabel("Heart Attacks", color='white')
    ax.legend()
    st.pyplot(fig)

  
# Run the dashboard
if __name__ == "__main__":
    app()
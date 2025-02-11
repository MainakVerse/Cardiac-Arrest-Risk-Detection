import streamlit as st
import datetime

# Function to check last restart time
@st.cache_resource(ttl=8)  # Auto-refresh after 24 hours
def last_restart_time():
    return datetime.datetime.now()

def display_restart_info():
    st.write(f"⏳ **Last Restart:** {last_restart_time()}")

    # Manual restart button
    if st.button("Restart Now"):
        st.cache_resource.clear()  # Clear cache to force restart
        st.experimental_rerun()

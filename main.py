import streamlit as st
from web_functions import load_data
from auto_restart import display_restart_info
from Tabs import diagnosis, home, result,  kc, talk2doc

# Configure the app
st.set_page_config(
    page_title = 'Cardiac Arrest Risk Prediction System',
    page_icon = '💔',
    layout = 'wide',
    initial_sidebar_state = 'auto'
)

Tabs = {
    "Home":home,
    "Ask Queries":talk2doc,
    "Diagnosis":diagnosis,
    "Result":result,
    "Knowledge Center":kc
}

st.sidebar.title('Navigation')

page = st.sidebar.radio("Page", list(Tabs.keys()))
st.sidebar.info('Made with 💙 by Mainak')
display_restart_info()
st.write("This app will automatically reset every 24 hours! ⏳")
df, X, y = load_data()

if page in ["Diagnosis"]:
    Tabs[page].app(df, X, y)
else:
    Tabs[page].app()

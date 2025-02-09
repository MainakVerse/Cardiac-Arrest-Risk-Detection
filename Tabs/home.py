import streamlit as st
import PIL

def app():
    st.title('Cardiac Risk Health Care Program')
    st.image('./images/cardiac.png')

    
    st.markdown(
    """## Cardiac Arrest: A Vital Overview

Cardiac arrest, an abrupt cessation of cardiac activity, can evoke apprehension. Understanding its pathophysiology and imperative interventions for patients in distress is paramount. Upon the onset of cardiac arrest, blood flow to the body and brain diminishes rapidly. Early recognition and management improve survival chances. Automated External Defibrillators (AEDs) administer life-saving shocks, returning erratic heartbeats to a normal rhythm. 

Driven by cutting-edge technology, artificial intelligence offers immense potential in safeguarding cardiac health. With groundbreaking algorithms, AI can analyze data swiftly to determine subtleties often difficult for doctors, recognizing unusual rhythms in electrocardiograms before events escalate into with cardiac arrest. Utilizing complex modeling, AI foreputs both refined prognostic assessments and efficient incident response capabilities enabling the provision of primoires ensuring optimal patient well-being among those at peril through mitigatory preventative checkups unaware of concealed underlying contexts accentuated these enhancements
    """, unsafe_allow_html=True)
    
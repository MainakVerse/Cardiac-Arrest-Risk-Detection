import streamlit as st

def app():
    st.markdown('''<h1><center>Heart Health Knowledge Centre</center></h1>''', unsafe_allow_html=True)
    
    # Paragraph 1: Heart Attack Risk Detection
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("./images/1.png", caption="Heart Attack Risk Detection", width=200)
    with col2:
        st.markdown('''
            The heart attack risk assessment system is a sophisticated, data-driven platform that evaluates cardiovascular health using clinical data. By employing advanced machine learning algorithms, the system analyzes critical health indicators including blood pressure, cholesterol levels, heart rate, ECG readings, and other cardiovascular markers to assess the risk of heart attack. The system can identify various cardiac conditions and risk levels, from early warning signs to immediate threats. This automated analysis ensures swift risk assessment, allowing for preventive intervention. The platform is designed for easy use, enabling patients to input their medical test results and receive a detailed risk analysis within moments.
        ''')

    # Paragraph 2: Cardiac Care Recommendations
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('''
            Beyond risk assessment, the system delivers personalized cardiac care recommendations based on individual risk factors. These recommendations encompass heart-healthy diet plans, appropriate exercise programs, medication schedules, and essential lifestyle changes tailored to each patient's cardiac health status. The system generates comprehensive cardiac health reports in PDF format, which can be easily shared with cardiologists and healthcare providers. This feature ensures continuous monitoring and management of heart health, enabling patients to actively participate in their cardiac care journey.
        ''')
    with col2:
        st.image("./images/2.png", caption="Cardiac Care Recommendations", width=200)

    # Paragraph 3: CardioBot Assistant
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("./images/3.png", caption="CardioBot Assistant", width=200)
    with col2:
        st.markdown('''
            A key feature of the system is CardioBot, an intelligent medical chatbot specialized in cardiovascular health. CardioBot draws from an extensive database of cardiac knowledge to address queries about heart attack symptoms, risk factors, emergency response procedures, and treatment options. Using advanced natural language processing (NLP), the chatbot provides clear, accurate information about cardiovascular health concerns. Whether users need information about warning signs, medication interactions, or lifestyle modifications, CardioBot offers round-the-clock support with evidence-based guidance.
        ''')

    # Paragraph 4: CardioTrends Analytics
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('''
            The system features CardioTrends, an advanced analytics module that visualizes heart attack statistics and trends. Through interactive dashboards, CardioTrends presents data on cardiovascular disease prevalence, risk factor distribution, and mortality rates across different populations and regions. This tool is invaluable for medical researchers, public health officials, and healthcare providers in understanding cardiovascular disease patterns. By presenting complex cardiac health data in an accessible format, CardioTrends facilitates evidence-based decision-making in cardiac care and prevention strategies.
        ''')
    with col2:
        st.image("./images/4.png", caption="CardioTrends Analytics", width=200)

    # Paragraph 5: Streamlit Integration
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("./images/5.png", caption="Streamlit Integration", width=200)
    with col2:
        st.markdown('''
            Developed using Streamlit, the heart attack care system provides an intuitive and responsive user interface. Streamlit's robust framework enables seamless integration of predictive models, statistical visualizations, and interactive features, making advanced cardiac care accessible to all users. The platform is web-based, ensuring widespread accessibility across different devices. By combining sophisticated risk assessment, personalized recommendations, and interactive tools like CardioBot and CardioTrends, this system represents a comprehensive approach to cardiovascular health management, supporting both patients and healthcare providers in preventing and managing heart disease.
        ''')

# Run the app
if __name__ == "__main__":
    app()
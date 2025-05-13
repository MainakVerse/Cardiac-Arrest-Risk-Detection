import streamlit as st
from web_functions import predict
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io
import os
import csv
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

load_dotenv()

# Load API Key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing! Add it to Streamlit secrets.")

genai.configure(api_key=GEMINI_API_KEY)

def app(df, X, y):
    """This function creates the Streamlit app with tabs."""
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px;
        color: #0000cc; /* Neon cyan text color */
        
    }
</style>

""", unsafe_allow_html=True)
    # Create two tabs
    tab1, tab2, tab3 = st.tabs(["Diagnosis 🩺", "Medication 💊", "Data Source 🛢️"])

    # First Tab: Prediction Page
    with tab1:
        st.title("Diagnosis Page")
        st.write("The aim is to detect the different types of diabetes and the risk of onset from the clinical test data. This makes the detection process extremely fast and feature-rich augmenting treatment experience and ease of access for both patient and physician")
        st.subheader("Select Values:")

        colA, colB = st.columns(2)
        with colA:
            Gender = st.slider("Gender [0: Female | 1: Male | 2: Trans]", int(df["Gender"].min()), int(df["Gender"].max()))
            Chain_smoker = st.slider("Chain_smoker [0: No | 1: Yes]", int(df["Chain_smoker"].min()), int(df["Chain_smoker"].max()))
            Consumes_other_tobacco_products = st.slider("Consumes other tobacco products? [0: No | 1: Yes]", int(df["Consumes_other_tobacco_products"].min()), int(df["Consumes_other_tobacco_products"].max()))
            HighBP = st.slider("Hypertension [0: No | 1: Yes]", int(df["HighBP"].min()), int(df["HighBP"].max()))
            Obese = st.slider("Obesity Issues? [0: No | 1: Yes]", int(df["Obese"].min()), int(df["Obese"].max()))
            Diabetes = st.slider("Diabetes Occurences? [0: No | 1: Yes]", int(df["Diabetes"].min()), int(df["Diabetes"].max()))
            
        with colB:
            Metabolic_syndrome = st.slider("Metabolic Syndromes? [0: No | 1: Yes]", int(df["Metabolic_syndrome"].min()), int(df["Metabolic_syndrome"].max()))
            Use_of_stimulant_drugs = st.slider("Use of Stimulant Drugs? [0: No | 1: Yes]", int(df["Use_of_stimulant_drugs"].min()), int(df["Use_of_stimulant_drugs"].max()))
            Family_history = st.slider("Family History of Heart Attack? [0: No | 1: Yes]", int(df["Family_history"].min()), int(df["Family_history"].max()))
            History_of_preeclampsia = st.slider("History of Preeclampsia? [0: No | 1: Yes]", int(df["History_of_preeclampsia"].min()), int(df["History_of_preeclampsia"].max()))
            CABG_history = st.slider("CABG History? [0: No | 1: Yes]", int(df["CABG_history"].min()), int(df["CABG_history"].max()))
            Respiratory_illness = st.slider("Any Respiratory Illnesses? [0: No | 1: Yes]", int(df["Respiratory_illness"].min()), int(df["Respiratory_illness"].max()))

            # Create a list to store all the features
        features = [Gender,Chain_smoker,Consumes_other_tobacco_products,HighBP,Obese,Diabetes,Metabolic_syndrome,Use_of_stimulant_drugs,Family_history,History_of_preeclampsia,CABG_history,Respiratory_illness]

        # Create a DataFrame to store slider values
        slider_values = {
            "Feature": ["Gender","Chain_smoker","Consumes_other_tobacco_products","HighBP","Obese","Diabetes","Metabolic_syndrome","Use_of_stimulant_drugs","Family_history","History_of_preeclampsia","CABG_history","Respiratory_illness"],
            "Value": [Gender,Chain_smoker,Consumes_other_tobacco_products,HighBP,Obese,Diabetes,Metabolic_syndrome,Use_of_stimulant_drugs,Family_history,History_of_preeclampsia,CABG_history,Respiratory_illness]
        }
        slider_df = pd.DataFrame(slider_values)

        # Create a button to predict
        if st.button("Predict"):
            # Get prediction and model score
            prediction, score = predict(X, y, features)
            
           
            # Store prediction result
            prediction_result = ""
            
            # Print the output according to the prediction
            if prediction == 1:
                prediction_result = "The person has a high risk of cardiac arrest. Take care!"
                st.warning(prediction_result)
           
            else:
                prediction_result = "The person has low risk of cardiac arrest."
                st.success(prediction_result)

            # Print the score of the model
            model_accuracy = f"The model used is trusted by doctors and has an accuracy of {round((score * 100), 2)}%"
            st.sidebar.write(model_accuracy)

            # Store these in session state for PDF generation
            st.session_state['prediction_result'] = prediction_result
            st.session_state['model_accuracy'] = model_accuracy

        # Display the slider values in a table
        st.subheader("Selected Values:")
        st.table(slider_df)

        # Download section
        st.subheader("Download Test Report")
        user_name = st.text_input("Enter your name (required for download):")

        if user_name:
            col1, col2 = st.columns(2)

            # PDF Download Button
            with col1:
                try:
                    # Generate PDF
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Add title
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, txt="Cardiac Arrest Risk Assessment Report", ln=True, align='C')
                    pdf.ln(10)

                    # Add user name and timestamp
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=f"User Name: {user_name}", ln=True)
                    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                    pdf.ln(10)

                    # Add prediction result if available
                    if 'prediction_result' in st.session_state:
                        pdf.set_font("Arial", 'B', 12)
                        pdf.cell(200, 10, txt="Prediction Result:", ln=True)
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=st.session_state.get('prediction_result', ''), ln=True)
                        pdf.ln(5)

                    # Add model accuracy if available
                    if 'model_accuracy' in st.session_state:
                        pdf.set_font("Arial", 'B', 12)
                        pdf.cell(200, 10, txt="Model Accuracy:", ln=True)
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=st.session_state.get('model_accuracy', ''), ln=True)
                        pdf.ln(10)

                    # Add the measurements table
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(200, 10, txt="Measurements:", ln=True)
                    pdf.set_font("Arial", size=12)
                    
                    # Create the data table
                    for index, row in slider_df.iterrows():
                        pdf.cell(100, 10, txt=f"{row['Feature']}:", ln=False)
                        pdf.cell(100, 10, txt=f"{str(row['Value'])}", ln=True)

                    # Create a temporary file path
                    temp_file = f"temp_{user_name}_report.pdf"
                    
                    # Save PDF to a temporary file
                    pdf.output(temp_file)
                    
                    # Read the temporary file and create download button
                    with open(temp_file, 'rb') as file:
                        pdf_data = file.read()
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_data,
                            file_name=f"{user_name}_cardiac_arrest_risk_report.pdf",
                            mime="application/pdf",
                        )
                    
                    # Import os and remove the temporary file
                    
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

                except Exception as e:
                    pass
                try:
                    # Generate PDF
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Add title
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, txt="Cardiac Arrest Risk Assessment Report", ln=True, align='C')
                    pdf.ln(10)

                    # Add user name and timestamp
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=f"User Name: {user_name}", ln=True)
                    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                    pdf.ln(10)

                    # Add prediction result if available
                    if 'prediction_result' in st.session_state:
                        pdf.set_font("Arial", 'B', 12)
                        pdf.cell(200, 10, txt="Prediction Result:", ln=True)
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=st.session_state.get('prediction_result', ''), ln=True)
                        pdf.ln(5)

                    # Add model accuracy if available
                    if 'model_accuracy' in st.session_state:
                        pdf.set_font("Arial", 'B', 12)
                        pdf.cell(200, 10, txt="Model Accuracy:", ln=True)
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=st.session_state.get('model_accuracy', ''), ln=True)
                        pdf.ln(10)

                    # Add the measurements table
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(200, 10, txt="Measurements:", ln=True)
                    pdf.set_font("Arial", size=12)
                    
                    # Create the data table
                    for index, row in slider_df.iterrows():
                        pdf.cell(100, 10, txt=f"{row['Feature']}:", ln=False)
                        pdf.cell(100, 10, txt=f"{str(row['Value'])}", ln=True)

                    # Save to bytes
                    pdf_output = io.BytesIO()
                    pdf.output(pdf_output)
                    pdf_bytes = pdf_output.getvalue()
                    
                    # Create download button
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"{user_name}_cardiac_arrest_risk_report.pdf",
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.success("Your report is generated")

            # CSV Download Button
            with col2:
                try:
                    # Convert DataFrame to CSV
                    csv_buffer = io.StringIO()
                    slider_df.to_csv(csv_buffer, index=False)
                    
                    # Create download button
                    st.download_button(
                        label="Download CSV Data",
                        data=csv_buffer.getvalue(),
                        file_name=f"{user_name}_cardiac_arrest_risk_data.csv",
                        mime="text/csv",
                    )
                except Exception as e:
                    st.error(f"Error generating CSV: {str(e)}")
        else:
            st.info("Please enter your name to enable downloads.")


    with tab2:
        
            def get_gemini_medication_recommendation(disease_type, patient_data):
                prompt = f"""
                You are a medical expert. Based on the following disease diagnosis, suggest the appropriate medications, their dosage, and additional lifestyle recommendations:
                
                **Disease Type**: {disease_type}
                
                **Patient Data**:
                {patient_data}
                
                Provide a clear and structured recommendation including:
                - Medication name
                - Recommended dosage
                - Special precautions
                - Any additional lifestyle suggestions
                """
                
                model = genai.GenerativeModel("gemini-2.0-flash")  # Using Gemini Pro for text-based generation
                response = model.generate_content(prompt)
                
                return response.text

            # Streamlit UI
            st.title("Medication Recommendations")
            st.markdown(
                """
                    <p style="font-size:25px">
                        Upload your patient data to get medication recommendations.
                    </p>
                """, unsafe_allow_html=True
            )

            # File uploader for CSV files
            uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

            if uploaded_file is not None:
                try:
                    df_original = pd.read_csv(uploaded_file)

                    # Display original data
                    st.subheader("Original Data:")
                    st.dataframe(df_original)

                    if df_original.shape[1] < 2:
                        st.error("CSV file must have at least two columns: parameters and values")
                        st.stop()

                    # Convert the uploaded data into a structured format
                    df_processed = pd.DataFrame([
                        {param: value for param, value in zip(df_original.iloc[:, 0], df_original.iloc[:, 1])}
                    ])

                    # Display transformed data
                    st.subheader("Transformed Data:")
                    st.dataframe(df_processed)

                    # Required columns check
                    required_columns = [
                        "Gender","Chain_smoker","Consumes_other_tobacco_products","HighBP","Obese","Diabetes","Metabolic_syndrome","Use_of_stimulant_drugs","Family_history","History_of_preeclampsia","CABG_history","Respiratory_illness"
                    ]
                    
                    missing_columns = [col for col in required_columns if col not in df_processed.columns]
                    
                    if missing_columns:
                        st.error(f"Missing required columns: {', '.join(missing_columns)}")
                        st.write("Your CSV should have these parameters in the first column:")
                        st.write(required_columns)
                        st.stop()

                    try:
                        # Convert all columns to numeric
                        for col in required_columns:
                            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
                        
                        

                        # Extract features for prediction
                        features = [
                            float(df_processed.iloc[0]['Gender']),
                            float(df_processed.iloc[0]['Chain_smoker']),
                            float(df_processed.iloc[0]['Consumes_other_tobacco_products']),
                            float(df_processed.iloc[0]['HighBP']),
                            float(df_processed.iloc[0]['Obese']),
                            float(df_processed.iloc[0]['Diabetes']),
                            float(df_processed.iloc[0]['Metabolic_syndrome']),
                            int(df_processed.iloc[0]['Use_of_stimulant_drugs']),
                            float(df_processed.iloc[0]['Family_history']),
                            float(df_processed.iloc[0]['History_of_preeclampsia']),
                            float(df_processed.iloc[0]['CABG_history']),
                            float(df_processed.iloc[0]['Respiratory_illness'])
                            ]

                        # Make prediction
                        prediction, confidence = predict(X, y, features)

                        # Disease mapping
                        disease_type = ""
                        if prediction == 1:
                            disease_type = "High risk of Cardiac Arrest"
                        
                        else:
                            disease_type = "Low risk of Cardiac Arrest"

                        st.subheader("Patient Recommendation:")
                        
                        if disease_type != "Low risk of Cardiac Arrest":
                            st.warning(disease_type)
                            patient_data = df_processed.iloc[0].to_dict()
                            
                            # Call Gemini to generate medication recommendations
                            medication_info = get_gemini_medication_recommendation(disease_type, patient_data)

                            st.info("AI Recommended Medication:")
                            st.write(medication_info)
                        else:
                            st.success("No diabetes detected")
                            st.info("Maintain a healthy lifestyle.")
                        confidence = confidence*100
                        st.write(f"Prediction confidence: {confidence:.2f}")

                    except Exception as e:
                        st.error(f"Error processing the data: {str(e)}")
                        st.write("Please ensure all values are numeric and properly formatted.")

                except Exception as e:
                    st.error(f"Error reading the file: {str(e)}")


                    

                       
    # Second Tab: Data Source Page
    with tab3:
        st.title("Data Info Page")
        st.subheader("View Data")

        # Create an expansion option to check the data
        with st.expander("View data"):
            st.dataframe(df)

        x = len(df)
        st.write('Updated data points:',x)
        st.write('Last Entry:', df.iloc[-1])
        last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"**Last server run:** {last_run_time}")

        # Create a section for columns description
        st.subheader("Columns Description:")

             # Create multiple checkboxes in a row
        col_name, summary, col_data = st.columns(3)

        # Show name of all columns
        with col_name:
            if st.checkbox("Column Names"):
                st.dataframe(df.columns)

        # Show datatype of all columns
        with summary:
            if st.checkbox("View Summary"):
                st.dataframe(df.describe())

        # Show data for each column
        with col_data:
            if st.checkbox("Columns Data"):
                col = st.selectbox("Column Name", list(df.columns))
                st.dataframe(df[col])

       

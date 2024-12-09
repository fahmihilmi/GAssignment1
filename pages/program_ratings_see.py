import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("Upload and Display CSV File")

# File uploader widget to allow CSV file upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if the user has uploaded a file
if uploaded_file is not None:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Display a preview of the dataframe
    st.write("CSV Data Preview:", df.head())

    # Optionally, display full data or other insights
    if st.checkbox('Show full data'):
        st.write(df)

    # Example of additional functionality: summary statistics
    st.write("Summary Statistics:")
    st.write(df.describe())

# import
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our app with custom styling
st.set_page_config(page_title="Data Sweeper", layout='wide')
st.markdown("""
    <style>
        body {
            background-color: yellow;
        }
        .stButton>button {
            background-color: green !important;
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Developer Info
st.image("https://www.facebook.com/photo.php?fbid=355500916727839&set=pb.100068038003092.-2207520000&type=3", width=100)
st.markdown("**Developed by: Altaf Hussain Sajdi**")

st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# Upload files
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Run Button
if st.button("Run Data Processing"):
    st.success("Processing started...")

# Conditions
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show rows 
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Data Summary Statistics
        st.subheader("Summary Statistics")
        if st.checkbox(f"Show Summary Statistics for {file.name}"):
            st.write(df.describe())

        # Data Filtering
        st.subheader("Data Filtering")
        filter_column = st.selectbox(f"Select a column to filter {file.name}", df.columns)
        filter_value = st.text_input(f"Enter a value to filter by in {filter_column}")
        if filter_value:
            filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
            st.write("Filtered Data")
            st.dataframe(filtered_df)

        # Data Cleaning 
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled successfully!")

        # Column Renaming
        st.subheader("Rename Columns")
        rename_col = st.selectbox(f"Select a column to rename in {file.name}", df.columns)
        new_name = st.text_input(f"Enter a new name for {rename_col}")
        if st.button(f"Rename {rename_col}"):
            df.rename(columns={rename_col: new_name}, inplace=True)
            st.success(f"Column renamed to {new_name}!")

        # Data Type Conversion
        st.subheader("Change Data Types")
        convert_col = st.selectbox(f"Select a column to change data type in {file.name}", df.columns)
        new_type = st.selectbox(f"Select new data type for {convert_col}", ["str", "int", "float"])
        if st.button(f"Convert {convert_col} to {new_type}"):
            df[convert_col] = df[convert_col].astype(new_type)
            st.success(f"Column {convert_col} converted to {new_type}!")

        # Advanced Visualizations
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            chart_type = st.selectbox(f"Select chart type for {file.name}", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
            x_axis = st.selectbox(f"Select X-axis for {file.name}", df.columns)
            y_axis = st.selectbox(f"Select Y-axis for {file.name}", df.columns)

            if chart_type == "Bar Chart":
                st.bar_chart(df[[x_axis, y_axis]])
            elif chart_type == "Line Chart":
                st.line_chart(df[[x_axis, y_axis]])
            elif chart_type == "Scatter Plot":
                st.write("Scatter Plot")
                st.pyplot(df.plot(kind='scatter', x=x_axis, y=y_axis).figure)
            elif chart_type == "Histogram":
                st.write("Histogram")
                st.pyplot(df[x_axis].plot(kind='hist').figure)

        # Convert file CSV 
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ("CSV", "Excel"), key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

# import
import streamlit as streamlit
import pandas as pandas
import os
from io import BytesIO


# sit up our app 
streamlit.set_page_config(page_title="Data sweeper", layout='wide')
streamlit.title("data sweeper")
streamlit.write("transform yiur files between CSV and Excel formats with bult_in data cleaning and visualization!")

# uploadfiles

uploaded_files =streamlit.file_uploader("Upload your files (CSV or Excel):" , type =[ "csv","xlsx"],
accept_multiple_files=true)

# condiions

if uploaded_files:
    for file in uploaded_files:
        file_ext=os.path.splitext(file.name) [-1]. lower()


        if file_ext==".CSV":
            df=pandas.read_CSV(file)
            elif file_ext==".xlsx":
                df = pandas.read_excel(file)
            else:
                streamlit.erorr(f"Unsupported file type: {file_ext} ")
                condiions


        # display info

        streamlit.write(f"**File Name:**{file.name}")
        streamlit.write(f"**File Name:**{file.size/1024}")

        


import streamlit as st 
import pandas as pd 
import os 
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
       background-color: black;
       color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper Sterling Integrator By Sheheryar Khan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization – created for quarter 3!")

# File uploader (corrected file types: "csv" instead of "cvs")
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ext}")  # Corrected f-string
            continue

        # File details
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            # Fixed typo: st.colums -> st.columns
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        # Select columns to keep (replaced st.writeselect with st.multiselect)
        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", options=df.columns.tolist(), default=df.columns.tolist())
        df = df[selected_columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            # Plotting the first two numeric columns (if available)
            numeric_df = df.select_dtypes(include='number')
            if numeric_df.shape[1] >= 2:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.write("Not enough numeric columns for visualization.")

        # Conversion options
        st.subheader("Conversion Option")
        # Corrected f-string and radio options: using "CSV" instead of "cvs"
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Renamed variable to "buffer" for consistency
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Fixed method name: to_csv, not to.csv
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"  # Unified variable name to mime_type
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)  # Fixed extra "to": now to_excel
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",  # Fixed "libel" to "label"
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )  

st.success("All files processed successfully!")

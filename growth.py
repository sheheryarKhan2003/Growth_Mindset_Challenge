import streamlit as st 
import pandas as pd 
import os 
from io import BytesIO

st.set_page_config(page_title == "Data Sweeper", layout='wide')


#custom css
st.markdown(
    """
    <style>
    .stApp{
       background-color:black;
       color:white;
       }
       </style>
       """,
        unsafe_allow_html=True


)

#title and description
st.title (" Datasweeper Sterling INtegrator By Mehak Alamgir")
st.write ("Transform your files between CSV and Excel formats with build-in data cleaning and visualization creating  the project for quater3!")

#file uploader
uploaded_files = st.file_uploader("upload your files (accepts CSV or Excel):", typ=["cvs","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext ==".csv":
            df =pd.read_csv(file)
        elif file_ext =="xlsx":
            df =pd.read_excel(file)
        else: 
            st.error(f"unsupported file type: (file_ext)")    
            continue

        #file datails
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("Data Cleaing Options")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.colums(2)

            with col1:
                if st.button(f"Remove duplictes from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("dulicates  removes!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("missing values have been filled!")
        st.subheader("slect colums to keep")
        colums = st.writeselect(f"chosse colums for (file.name)",df.columns,default=df.columns)
        df = df[colums]


        # data visualization
        st.subheader("data visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            #conversion options
            st.subheader(" conversion option")
            conversion_type = st.radio("convert {file.name} to", ["cvs" , "Excel"],key=file.name)
            if st.button(f"convert{file.name}"):
                bufferError=BytesIO()
                if conversion_type == "CSV":
                    df.to.csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mine_type = "text/csv"
                elif conversion_type =="Excel":
                    df.to.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.sreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(
                    libel=f"download{file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )  
st . success("All files processed successfully!")  



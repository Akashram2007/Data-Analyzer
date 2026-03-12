import streamlit as st
import pandas as pd

def data_summary(data, menu):
    
    st.title(f"{menu}📈")
    st.write("Dataset Size :",data.size)
    st.write("Number of Rows :",data.shape[0])
    st.write("Number of Columns :",data.shape[1])
    st.write("Data Shape :",data.shape)
    
    st.write("### Columns and Data Type:")
    
    dtype = pd.DataFrame({"Columns":list(data.columns),
                            "Data Type":list(data.dtypes)})
    dtype.index = range(1,len(dtype)+1)
    dtype.index.name = "S.No"
    dtype.to_html(index=False,justify="center")
    st.dataframe(dtype,width=550)
    
    st.write("### Uniuqe Value Per Columns :")
    unique = pd.DataFrame({"Columns":list(data.columns),
                            "Counts":list(data.nunique())})
    
    unique.index = range(1,len(unique)+1)
    unique.index.name = "S.No"
    
    st.dataframe(unique,width=550)
    
    st.write("### Descriptive Statistics :")
    st.dataframe(data.describe(),width=550)      
    st.write("### Correlation Matrix :")
    st.dataframe(data.corr(numeric_only=True),width=550)
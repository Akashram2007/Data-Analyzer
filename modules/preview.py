import streamlit as st

def data_preview(data, file, menu):
    st.title(f"{menu}🔍")
    st.success("File Uploaded Sucessfully!")
    st.write("### File Name :",file.name)
    st.write("##### File Preview :")
    st.dataframe(data,width=550)
    st.write("Dataset Size :",data.size)
    st.write("Number of Rows :",data.shape[0])
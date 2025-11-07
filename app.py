import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from io import BytesIO

st.set_page_config(page_title="Data Analyzer",page_icon="🔍")
st.sidebar.title("Data Analyzer")
file = st.sidebar.file_uploader("Upload File",type=["csv","xlsx"],width=400)
menu = st.sidebar.radio("Sections :",options=
["Data Preview","Data Summary","Missing Data/Cleaning","Visualization"])

if file is not None:
    file_type = file.name.split(".")[-1]
    if file_type == "csv":
       data = pd.read_csv(file)
    elif file_type == "xlsx":
        data = pd.read_excel(file)
    else:
        st.error("Unsupported File Type")
    
    data.index = range(1,len(data)+1)
    data.index.name = "S.No"

    #============================DATA PREVIEW============================

    if menu == "Data Preview":
         st.title(f"{menu}🔍")
         st.success("File Uploaded Sucessfully!")
         st.write("### File Name :",file.name)
         st.write("##### File Preview :")
         st.dataframe(data,width=550)
         st.write("Dataset Size :",data.size)
         st.write("Number of Rows :",data.shape[0])
       
    #============================DATA SUMMARY============================

    if menu == "Data Summary":
      
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

    #============================MISSING/CLEANING DATA============================

    if menu == "Missing Data/Cleaning":
       
       st.title(f"{menu}🧹")

       st.write("##### Missing Values :")
       missing_count = pd.DataFrame({"Columns":data.columns,
                                     "Count":list(data.isnull().sum())})
       missing_count.index = range(1,len(missing_count)+1)
       missing_count.index.name = "S.No"
       st.dataframe(missing_count,width=550)
       
       st.write("### Total Missing Value in Dataset : ",missing_count["Count"].sum())

       max_missing = missing_count.sort_values(by="Count",ascending=False).head(1)
       st.write(f"##### Column With Large Percentage of Missing Value :")
       st.dataframe(max_missing,width=550)

       st.write("##### Percentage of Missing Value Per Column :")
       percentage = pd.DataFrame({"Columns":data.columns,
                                  "Percentage":missing_count["Count"]/data.shape[0]*100})
       st.dataframe(percentage,width=550)

       st.header("Cleaning Process")

       if st.button("Drop Missing Data"):
           st.warning("Warning : Dropping Too Many rows may reduce data quality")
           data.dropna(axis=0,inplace=True)
           st.success("Missing values are Removed Sucessfully")
           st.write("Cleaned Dataset :")
           st.dataframe(data,width=550)
           st.write("Data Shape :",data.shape)
           drop_data = data.to_csv(index=False).encode("utf-8")
           st.download_button("Download Data",data=drop_data,
                              mime='text/csv')

       if st.button("Fill Missing Data"):
            filled_data = data.apply(lambda x : x.fillna(x.mean())
                   if x.dtype=="float" else x.fillna(x.value_counts().index[0]))
            st.success("Missing values are Filled With Mean/Mode Sucessfully")
            st.write("Filled Dataset :")
            st.dataframe(filled_data,width=550)
            st.write("Data Shape :",data.shape)
            fill_data = filled_data.to_csv(index=False).encode("utf-8")
            st.download_button("Download Data",
                              data=fill_data,
                              mime='text/csv')
            
     #============================VISUALIZATION============================
    if menu == "Visualization":
      st.title(f"{menu}📊")
      type = st.selectbox("file Mode",["Original","Drop Null Values","Fill Null Values"],width=300) 
      if type == "Original":
         data = data 
      if type == "Drop Null Values":
         data.dropna(axis=0,inplace=True)
      if type == "Fill Null Values":
         data = data.apply(lambda x : x.fillna(x.mean())
                   if x.dtype=="float" else x.fillna(x.value_counts().index[0]))
      st.dataframe(data,width=550,height=250)
      plot = st.selectbox("Select PLot Type",["none","Scatter","Line","Bar","Histogram","Heat map"],width=300)
      columns = data.columns.to_list()
      if plot != "none":
        fig, a = plt.subplots()
        #----------------------------HEAT MAP----------------------------
        if plot == "Heat map":
          st.header("Heat Map")
          corr = data.corr(numeric_only=True)
          sns.heatmap(corr,annot=True,cmap="coolwarm")

        #----------------------------HISTOGRAM PLOT----------------------------
        elif plot == "Histogram":
          st.header(f"{plot} Plot :")
          x = st.selectbox("X axis",columns,width=300)
          plt.xlabel(x)
          bins = int(st.number_input("Enter no of Bins",max_value=20,value=6,width=300))
          color = st.color_picker("Graph colour",width=300,value="#1DB0D6")
          sns.histplot(data[x],bins=bins,color=color)
        else:
          x = st.selectbox("X axis",columns,width=300)
          plt.xlabel(x)
          y = st.selectbox("Y axis",columns,width=300,key="y")   
          plt.ylabel(y)
          color = st.color_picker("Graph colour",width=300,value="#1DB0D6")
        #----------------------------SCATTER PLOT----------------------------
        if plot == "Scatter":
          sns.scatterplot(data=data,x=data[x],y=data[y],color=color)
        
        #----------------------------LINE PLOT----------------------------
        if plot == "Line":
          sns.lineplot(data=data,x=x,y=y,color=color)
          
        #----------------------------BAR PLOT----------------------------
        if plot == "Bar":
          sns.barplot(data=data,x=x,y=y,color=color)

        with st.spinner("Visualizing Your Data..."):
          time.sleep(0.5)
          plt.style.use("default")
          chart = st.pyplot(fig,width=500)
          buf = BytesIO()
          fig.savefig(buf, format="png")
          st.download_button("Download Chart",data = buf.getvalue(),mime="image/png",file_name="chart.png")

else:
  st.title("Data Analyzer")
  st.header("Analyze, Clean, and Visualize Your Data in Seconds")
  st.subheader("Start Exploring Your Data Now!!")
  st.title("🔍📈🧹📊")
  st.error("Upload your File")
  
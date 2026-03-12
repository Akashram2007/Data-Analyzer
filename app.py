import streamlit as st
import pandas as pd

from modules.preview import data_preview
from modules.summary import data_summary
from modules.cleaning import data_cleaning
from modules.visualization import visualization

st.set_page_config(page_title="Data Analyzer",page_icon="🔍")
st.sidebar.title("Data Analyzer")
file = st.file_uploader("Upload File",type=["csv","xlsx"],width=400)
menu = st.sidebar.radio("Sections :",options=
["Data Preview","Data Summary","Missing Data/Cleaning","Visualization"])

if file is not None:
    file_type = file.name.split(".")[-1]
    if file_type == "csv":
       data = pd.read_csv(file)
    elif file_type == "xlsx":
        data = pd.read_excel(file, engine = "openpyxl")
    else:
        st.error("Unsupported File Type")
    
    data.index = range(1,len(data)+1)
    data.index.name = "S.No"

    #============================DATA PREVIEW============================
    
    if menu == "Data Preview":
        data_preview(data,file,menu)
       
    #============================DATA SUMMARY============================

    if menu == "Data Summary":
        data_summary(data,menu)


    #============================MISSING/CLEANING DATA============================

    if menu == "Missing Data/Cleaning":
       data_cleaning(data,menu)

            
     #============================VISUALIZATION============================
    if menu == "Visualization":
<<<<<<< HEAD
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
        fig, a = plt.subplots( figsize = (16,8))
        #----------------------------HEAT MAP----------------------------
        if plot == "Heat map":
          st.header("Heat Map")
          corr = data.corr(numeric_only=True)
          sns.heatmap(corr,annot=True,cmap="coolwarm")

        #----------------------------HISTOGRAM PLOT----------------------------
        elif plot == "Histogram":
           st.header(f"{plot} Plot :")
           x = st.selectbox("X axis", columns, width=300)
           plt.xlabel(x)
           bins = int(st.number_input("Enter no of Bins",max_value=20,value=6,width=300)) 
           color = st.color_picker("Graph colour", width=300, value= "#1DBOD6") 
           sns.histplot(data[x],bins=bins,color=color)
        else:
            x = st.selectbox("X axis", columns, width=300)
            plt.xlabel(x)
            y = st.selectbox("Y axis",columns,width=300,key="y") 
            plt.ylabel(y) 
            color = st.color_picker("Graph colour",width=300,value="#1DBOD6")
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
          plt.xticks(rotation = 45, ha = "right")
          plt.tight_layout()
          chart = st.pyplot(fig, use_container_width=True)
          buf = BytesIO()
          fig.savefig(buf, format="png")
          st.download_button("Download Chart",data = buf.getvalue(),mime="image/png",file_name="chart.png")

=======
        visualization(data,menu)
>>>>>>> fc4050e (spliting modules)
else:
  st.title("Data Analyzer")
  st.header("Analyze, Clean, and Visualize Your Data in Seconds")
  st.subheader("Start Exploring Your Data Now!!")
  st.title("🔍📈🧹📊")
  st.error("Upload your File")
  

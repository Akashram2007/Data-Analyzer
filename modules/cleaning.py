import streamlit as st
import pandas as pd


def data_cleaning(data):

    if data.isnull().values.any():
        st.write("##### Missing Values :")
        missing_count = pd.DataFrame(
            {"Columns": data.columns, "Count": list(data.isnull().sum())}
        )
        missing_count.index = range(1, len(missing_count) + 1)
        missing_count.index.name = "S.No"
        st.dataframe(missing_count, width=550)

        st.write("### Total Missing Value in Dataset : ", missing_count["Count"].sum())

        max_missing = missing_count.sort_values(by="Count", ascending=False).head(1)
        st.write(f"##### Column With Large Percentage of Missing Value :")
        st.dataframe(max_missing, width=550)

        st.header("Cleaning Process")

        if st.button("Drop Missing Data"):
            st.warning("Warning : Dropping Too Many rows may reduce data quality")
            data.dropna(axis=0, inplace=True)
            st.success("Missing values are Removed Sucessfully")
            st.write("Cleaned Dataset :")
            st.dataframe(data, width=550)
            st.write("Data Shape :", data.shape)
            drop_data = data.to_csv(index=False).encode("utf-8")
            st.download_button("Download Data", data=drop_data, mime="text/csv")

        if st.button("Fill Missing Data"):
            filled_data = data.apply(
                lambda x: (
                    x.fillna(x.mean())
                    if x.dtype == "float"
                    else x.fillna(x.value_counts().index[0])
                )
            )
            st.success("Missing values are Filled With Mean/Mode Sucessfully")
            st.write("Filled Dataset :")
            st.dataframe(filled_data, width=550)
            st.write("Data Shape :", data.shape)
            fill_data = filled_data.to_csv(index=False).encode("utf-8")
            st.download_button("Download Data", data=fill_data, mime="text/csv")
    else:
        st.success("Your Dataset does not Contain any Missing Values.")

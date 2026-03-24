import streamlit as st
import pandas as pd
from io import BytesIO

def data_preview(data, file):

    st.success("File Uploaded Successfully!")
    st.write("### File Name :", file.name)

    st.write("##### Dataset Size :", data.size)
    st.write("##### Number of Rows :", data.shape[0])

    # ---- SESSION INIT ----
    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = data.copy()

    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0

    st.write("## 🔍 Smart Data Filter")

    # ---- DROPDOWN FILTER UI ----
    with st.expander("⚙️ Click to Apply Filters", expanded=True):

        with st.form("filter_form"):

            user_inputs = {}
            columns = list(data.columns)
            max_per_row = 3

            for i in range(0, len(columns), max_per_row):
                row_cols = st.columns(max_per_row)

                for j in range(max_per_row):
                    if i + j < len(columns):
                        col_name = columns[i + j]

                        with row_cols[j]:

                            # 🔵 NUMERIC → SLIDER
                            if pd.api.types.is_numeric_dtype(data[col_name]):
                                min_val = float(data[col_name].min())
                                max_val = float(data[col_name].max())

                                selected_range = st.slider(
                                    col_name,
                                    min_val,
                                    max_val,
                                    (min_val, max_val),
                                    key=f"slider_{col_name}_{st.session_state.reset_counter}"
                                )

                                user_inputs[col_name] = ("numeric", selected_range)

                            # 🟢 CATEGORICAL → MULTISELECT
                            else:
                                unique_vals = data[col_name].dropna().unique().tolist()

                                selected_vals = st.multiselect(
                                    col_name,
                                    unique_vals,
                                    key=f"multi_{col_name}_{st.session_state.reset_counter}"
                                )

                                user_inputs[col_name] = ("categorical", selected_vals)

            # ---- BUTTONS IN SAME ROW ----
            col1, col2 = st.columns(2)

            with col1:
                apply_filter = st.form_submit_button(
                    "Apply Filter",
                    use_container_width=True
                )

            with col2:
                reset_filter = st.form_submit_button(
                    "🔄 Reset Filter",
                    use_container_width=True
                )

    # ---- APPLY FILTER ----
    if apply_filter:
        filtered_data = data.copy()

        for col, val in user_inputs.items():

            if val[0] == "numeric":
                min_val, max_val = val[1]
                filtered_data = filtered_data[
                    (filtered_data[col] >= min_val) &
                    (filtered_data[col] <= max_val)
                ]

            elif val[0] == "categorical":
                selected_vals = val[1]
                if selected_vals:
                    filtered_data = filtered_data[
                        filtered_data[col].isin(selected_vals)
                    ]

        st.session_state.filtered_data = filtered_data

    # ---- RESET FILTER ----
    if reset_filter:
        st.session_state.reset_counter += 1
        st.session_state.filtered_data = data.copy()
        st.rerun()

    # ---- DISPLAY ----
    st.write("### 📊 Data Preview")

    display_data = st.session_state.filtered_data

    if display_data.empty:
        st.warning("No data matches your filter")
    else:
        st.dataframe(display_data, width=900)

        # ---- DOWNLOAD ----
        st.divider()
        st.subheader("⬇️ Download Filtered Data")

        file_format = st.selectbox("Select format", ["CSV", "Excel"],width=300)

        if file_format == "CSV":
            csv = display_data.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"filtered_{file.name}",
                mime="text/csv"
            )

        elif file_format == "Excel":
            output = BytesIO()
            display_data.to_excel(output, index=False)
            excel_data = output.getvalue()

            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name="filtered_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

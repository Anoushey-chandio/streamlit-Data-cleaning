import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure Streamlit app
st.set_page_config(page_title="📅 Data Sweeper", layout="wide")
st.title('📅 Data Sweeper')
st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization!')

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)  # Fixed
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Show file info
        st.write(f"**File name:** {file.name}")
        st.write(f"**File size:** {file.size / 1024:.2f} KB")

        # Preview Data
        st.write('🔍 Preview of DataFrame')
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"🧹 Data Cleaning Options for {file.name}")

        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")

            # Column Selection
            st.subheader("🎯 Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Visualization (Outside Cleaning Checkbox for better usability)
        st.subheader(f"📊 Data Visualization for {file.name}")

        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if len(numeric_cols) < 1:
            st.warning("No numeric columns available for visualization.")
        else:
            selected_cols = st.multiselect(f"Select columns for chart (for {file.name})", numeric_cols, default=numeric_cols[:2])

            if st.button(f"Show Chart for {file.name}"):
                if len(selected_cols) >= 1:
                    st.bar_chart(df[selected_cols])
                else:
                    st.warning("Please select at least one column for visualization.")

        # File Conversion Section
        st.subheader(f"🔁 Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["csv", "excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type.upper()}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed!")



import pandas as pd
import streamlit as st


st.set_page_config(layout="wide")
data = pd.read_excel(
    "db/dataset.xlsx", 
    usecols = ["tds", "jarak", "kelembapan", "suhu"]
    )

col1, col2, col3, col4 = st.columns(4)
col1.metric("TDS", 10)
col2.metric("Water Distance", 20)
col3.metric("Moisture", 30)
col4.metric("Temperature", f"50 °C")

st.line_chart(data.iloc[:, [0, 2, 3]])
st.line_chart(data.iloc[:, 1])
# col5, col6 = st.columns(2)
# col5.line_chart(data["tds"])
# col6.line_chart(data["jarak"])

# col7, col8 = st.columns(2)
# col7.line_chart(data["kelembapan"])
# col8.line_chart(data["suhu"])
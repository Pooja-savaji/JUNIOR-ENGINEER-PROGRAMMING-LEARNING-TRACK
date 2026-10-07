import streamlit as st
import pandas as pd

st.title("Student Data Entry")
name = st.text_input("Name")
marks = st.number_input("Marks", 0, 100, 0)

if st.button("Add Student"):
    if name == "":
        st.error("Please enter a name.")
    else:
        st.success("Student added successfully!")

st.header("Report")

data = pd.DataFrame({
    "Name": [name] if name else [],
    "Marks": [marks] if name else []
})

if data.empty:
    st.info("No student data available.")
else:
    st.dataframe(data)

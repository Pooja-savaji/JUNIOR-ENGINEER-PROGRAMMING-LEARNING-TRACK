import streamlit as st
from service import calculate_result

st.title("Student Result")
name = st.text_input("Name")
marks = st.number_input("Marks", 0, 100)

if st.button("Check Result"):
    result = calculate_result(marks)
    st.write("Student:", name)
    st.write("Result:", result)

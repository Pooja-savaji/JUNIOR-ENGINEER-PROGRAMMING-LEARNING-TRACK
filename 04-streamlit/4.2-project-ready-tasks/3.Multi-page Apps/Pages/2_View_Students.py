import streamlit as st
st.title("View Students")

if "students" not in st.session_state:
    st.session_state.students = []

st.dataframe(st.session_state.students)

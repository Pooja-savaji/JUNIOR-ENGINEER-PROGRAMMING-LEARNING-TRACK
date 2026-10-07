import streamlit as st
st.title("Add Student")

if "students" not in st.session_state:
    st.session_state.students = []

name = st.text_input("Name")
course = st.text_input("Course")

if st.button("Add"):
    st.session_state.students.append({
        "Name": name,
        "Course": course
    })
    st.success("Student added!")

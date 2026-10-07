import streamlit as st
st.title("Delete Student")

if "students" not in st.session_state:
    st.session_state.students = []

if st.session_state.students:
    names = [s["Name"] for s in st.session_state.students]
    name = st.selectbox("Select Student", names)

    if st.button("Delete"):
        st.session_state.students = [
            s for s in st.session_state.students
            if s["Name"] != name
        ]
        st.success("Student deleted!")
else:
    st.write("No students available.")

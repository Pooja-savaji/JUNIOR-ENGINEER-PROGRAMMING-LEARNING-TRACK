import streamlit as st
st.title("Multi-Step Form")

if "step" not in st.session_state:
    st.session_state.step = 1

if "data" not in st.session_state:
    st.session_state.data = {}

if st.session_state.step == 1:
    st.header("Step 1")
    st.session_state.data["name"] = st.text_input("Name")

    if st.button("Next"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.header("Step 2")
    st.session_state.data["email"] = st.text_input("Email")

    if st.button("Next"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.header("Step 3")
    st.session_state.data["course"] = st.text_input("Course")

    if st.button("Submit"):
        st.success("Submitted!")
        st.write(st.session_state.data)

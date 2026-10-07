import streamlit as st
import pandas as pd
from auth import login
from operations import add_record

st.title("Internal Operations Dashboard")

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

# Load data
if "data" not in st.session_state:
    st.session_state.data = pd.read_csv(
        "data/operations.csv"
    )

# Add record
st.header("Add Record")

name = st.text_input("Name")
department = st.text_input("Department")

status = st.selectbox(
    "Status",
    ["Pending", "Completed"]
)

if st.button("Add Record"):
    if name and department:

        st.session_state.data = add_record(
            st.session_state.data,
            name,
            department,
            status
        )

        st.success("Record added successfully")

    else:
        st.error("Please fill all fields")

# Display records
st.header("Operations Report")

filter_status = st.selectbox(
    "Filter by Status",
    ["All", "Pending", "Completed"]
)

data = st.session_state.data
if filter_status != "All":
    data = data[
        data["Status"] == filter_status
    ]

if data.empty:
    st.info("No records found.")
else:
    st.dataframe(data)

# Download report
csv = data.to_csv(index=False)

st.download_button(
    "Download Report",
    csv,
    "operations_report.csv",
    "text/csv"
)

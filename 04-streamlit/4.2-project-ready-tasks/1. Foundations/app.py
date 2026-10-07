import streamlit as st
import pandas as pd

st.title("Data Viewer")

data = pd.DataFrame({
    "Name": ["Pooja", "Rahul", "Sneha"],
    "Age": [22, 23, 21],
    "Marks": [85, 78, 92]
})

# Section 1: Dashboard
st.header("Dashboard")
st.write("Total Students:", len(data))

# Section 2: Filter
st.header("Filter")
min_marks = st.slider("Minimum Marks", 0, 100, 0)
filtered_data = data[data["Marks"] >= min_marks]

# Section 3: Data Table
st.header("Student Data")
st.dataframe(filtered_data)

# Section 4: Chart
st.header("Marks Chart")
st.bar_chart(filtered_data.set_index("Name")["Marks"])

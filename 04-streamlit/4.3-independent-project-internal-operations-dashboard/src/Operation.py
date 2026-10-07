import pandas as pd

def add_record(data, name, department, status):
    new_record = {
        "Name": name,
        "Department": department,
        "Status": status
    }
    return pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)

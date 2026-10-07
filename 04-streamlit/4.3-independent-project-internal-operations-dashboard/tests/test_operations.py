import pandas as pd
from src.operations import add_record
def test_add_record():

    data = pd.DataFrame(
        columns=[
            "Name",
            "Department",
            "Status"
        ]
    )

    result = add_record(
        data,
        "Pooja",
        "IT",
        "Completed"
    )

    assert len(result) == 1
    assert result.iloc[0]["Name"] == "Pooja"
    assert result.iloc[0]["Department"] == "IT"
    assert result.iloc[0]["Status"] == "Completed"

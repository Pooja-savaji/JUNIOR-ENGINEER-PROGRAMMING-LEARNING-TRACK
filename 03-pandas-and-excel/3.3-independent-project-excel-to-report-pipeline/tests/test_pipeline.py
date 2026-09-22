from pipeline import run_pipeline
import os
def test_pipeline():
    run_pipeline("input.xlsx", "test_report.xlsx")
    assert os.path.exists("test_report.xlsx")
    os.remove("test_report.xlsx")
  
test_pipeline()
print("Test passed")

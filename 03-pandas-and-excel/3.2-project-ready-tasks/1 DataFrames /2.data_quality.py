import pandas as pd

df = pd.read_csv("data.csv")

print("DATA QUALITY REPORT")
print("-------------------")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nFirst 5 Rows:")
print(df.head())

print("\nSalary:")
print(df["Salary"])

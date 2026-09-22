import pandas as pd

df = pd.read_csv("messy_data.csv")

# Remove extra spaces
df["Name"] = df["Name"].str.strip()

# Normalize city names
df["City"] = df["City"].str.title()

# Convert Age to number
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# Fill missing age
df["Age"] = df["Age"].fillna(df["Age"].median())

# Remove duplicates
df = df.drop_duplicates()

# Validate salary
df = df[df["Salary"] > 0]

# Save cleaned data
df.to_csv("clean_data.csv", index=False)

print(df)

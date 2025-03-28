from datetime import datetime

import pandas as pd
from pandas import DataFrame
import os

def read_date(dataframe: DataFrame):
    content = dataframe.iat[0, 0]
    date_text = content.split(":")[1].strip()
    parsed = datetime.strptime(date_text, "%d / %m / %Y")
    return parsed


# Repo root
repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the Excel file
file_path = os.path.join(repo_dir, 'in', "A3.xlsx")


# Read the Excel file
df = pd.read_excel(file_path, header=None)

# Read date
text = read_date(df)

# Keep data only
df = df.iloc[3:]

employee_data = {}

for index, row in df.iterrows():
    print(f"{index} : {list(row.values)}")

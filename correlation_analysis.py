import pandas as pd
from data_analysis_tools import data_cleaner
import matplotlib.pyplot as plt

# load data
while True:
    try:
        df = pd.read_csv(input("What is the file name? ")+'.csv')
        break
    except FileNotFoundError:
        print("File not found!")

# cleaning data
raw_num = len(df)
df = data_cleaner(df, "number", ["unit_price", "units_sold", "discount", "rating"])

# correlation
print(df["unit_price"].corr(df["units_sold"]))
print(df["discount"].corr(df["units_sold"]))
print(df["rating"].corr(df["units_sold"]))

print(df[["unit_price", "units_sold", "discount", "rating"]].corr())

# plots
plt.scatter(df["unit_price"], df["units_sold"])
plt.title("unit_price vs units_sold")
plt.xlabel("unit_price")
plt.ylabel("units_sold")
plt.show()

plt.scatter(df["discount"], df["units_sold"])
plt.title("discount vs units_sold")
plt.xlabel("discount")
plt.ylabel("units_sold")
plt.show()
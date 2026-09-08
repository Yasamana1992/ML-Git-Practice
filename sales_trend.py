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
colomns_name = ["quantity", "unit_price"]
df = data_cleaner(df, "number", colomns_name)
df = data_cleaner(df, "date", ["date"])

# calculations
df["revenue"] = df["quantity"] * df["unit_price"]
max_rev = df["revenue"].idxmax()
min_rev = df["revenue"].idxmin()

# month column
df["year_month"] = df["date"].dt.to_period("M")

print("=============== OVERALL REPORT ===============", "\n")
print("Number of transactions: ",len(df))
print(f"Total revenue: {df["revenue"].sum():,.0f}")
print(f"Total quantity: {df["quantity"].sum():,.0f}")
print(f"Average revenue of each transaction: {df["revenue"].mean():,.2f}")
print("Highest revenue: ", df.loc[max_rev, "product"], "-", df.loc[max_rev, "revenue"])
print("Lowest revenue: ", df.loc[min_rev, "product"], "-", df.loc[min_rev, "revenue"])

print("\n", "------------- Analysis per month ------------", "\n")
print("Total revenue: ", df.groupby("year_month")["revenue"].sum())
print("Total quantity: ", df.groupby("year_month")["quantity"].sum())
print("Number of transactions: ", df.groupby("year_month")["product"].count())
print("Month with highest revenue : ", df.groupby("year_month")["revenue"].sum().idxmax())
print("Month with hishest quantity: ", df.groupby("year_month")["quantity"].sum().idxmax())

print("\n", "------------ Analysis by product ------------", "\n")
print("Total revenue: ", df.groupby("product")["revenue"].sum())
print("Total quantity: ", df.groupby("product")["quantity"].sum())
print("Top 3 products by revenue", df.groupby("product")["revenue"].sum().nlargest(3))

print("\n", "----------- Analysis by category ------------", "\n")
print("Total revenue: ", df.groupby("category")["revenue"].sum())
print("Total quantity: ", df.groupby("category")["quantity"].sum())
print("Number of transactions: ", df.groupby("category")["product"].count())

# plots
size = df.groupby("year_month")["revenue"].sum()
size.index = size.index.astype(str)
size.plot()
plt.title("Revenue per month")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

size = df.groupby("product")["revenue"].sum()
plt.pie(size, labels=size.index)
plt.title("Revenue by product")
plt.show()

size = df.groupby("category")["revenue"].sum()
plt.pie(size, labels=size.index)
plt.title("Revenue by category")
plt.show()
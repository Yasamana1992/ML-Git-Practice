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
df = data_cleaner(df, "number", ["units_sold", "unit_price", "unit_cost", "discount"])

# new columns calculation
df["revenue"] = df["units_sold"] * df["unit_price"] * (1 - df["discount"] / 100)   # gross revenue after discount

df["total_cost"] = df["units_sold"] * df["unit_cost"]

df["profit"] = df["revenue"] - df["total_cost"]

df["profit_margin"] = df["profit"] / df["revenue"] * 100
overall_profit_margin = df["profit"].sum() / df["revenue"].sum() * 100

# select columns for product dataframe
selected_df = df[["product", "category", "units_sold", "revenue", "total_cost", "profit", "profit_margin"]]

# making dataframe by category
df_by_category = df.groupby("category").agg({"revenue": "sum",
                                             "total_cost": "sum",
                                             "profit": "sum",
                                             "units_sold": "sum"})

df_by_category["profit_margin"] = df_by_category["profit"] / df_by_category["revenue"] * 100

# reports
print("=================== OVERALL REPORT ===================", "\n")
print("Total Units Sold: ", df["units_sold"].sum())
print("Total Revenue: ", df["revenue"].sum())
print("Total Cost: ", df["total_cost"].sum())
print("Total Profit: ", df["profit"].sum())
print(f'Overall Profit Margin: {overall_profit_margin:,.2f}')
print(f'Average Discount: {df["discount"].mean():,.2f}')
print("\n", "------------- Analysis Top products -------------", "\n")
print("Top 3 products by Profit: ", "\n", selected_df.nlargest(3, "profit"))
print("Top 3 products by Revenue: ", "\n", selected_df.nlargest(3, "revenue"))
print("Top 3 products by Profit Margin: ", "\n", selected_df.nlargest(3, "profit_margin"))
print("\n", "-------------- Analysis by category -------------", "\n")
print(df_by_category)
print("Best category by Profit: ", df_by_category["profit"].idxmax())
print("Best category by Profit Margin: ", df_by_category["profit_margin"].idxmax())

# plots
selected_df.set_index("product")["profit"].plot(kind='bar')
plt.title("Profit by product")
plt.xlabel("Product")
plt.ylabel("Profit")
plt.show()

df_by_category["profit"].plot(kind='bar')
plt.title("Profit by category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.show()

selected_df.set_index("product")[["revenue", "profit"]].plot(kind='bar')
plt.title("Revenue vs Profit by product")
plt.xlabel("Product")
plt.ylabel("Amount")
plt.show()
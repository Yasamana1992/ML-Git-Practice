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
df = data_cleaner(df, "number", ["quantity", "unit_price"])
df = data_cleaner(df, "date", ["date"])

# revenue and month column
df["revenue"] = df["quantity"] * df["unit_price"]

df["year_month"] = df["date"].dt.to_period("M")
df = df.sort_values(by=["year_month"])

# monthly business summary
month_df = df.groupby("year_month").agg(
    revenue=("revenue" , 'sum'),
    quantity=("quantity" , 'sum'),
    transactions=("revenue" , 'count'),
    avg_transactions=("revenue" , 'mean')
)
month_df["revenue_growth"] = month_df[["revenue"]].pct_change() * 100

# product report
total_rev = df["revenue"].sum()

product_df = df.groupby("product").agg(
    total_revenue=("revenue" , 'sum'),
    total_quantity=("quantity" , 'sum'),
    revenue_share_percent=("revenue" , lambda x : x.sum() * 100 / total_rev)
)

top_products = product_df.nlargest(3, ["revenue_share_percent"])
                                   
# reports
print("************* Monthly Report *************")
print(month_df)
print("************* Product Report *************")
print(product_df)
print("************* Business Summary ************")
print("Total Revenue: " , df["revenue"].sum())
print("Total Quantity: ",  df["quantity"].sum())
print("total_transactions: ", df["revenue"].count()),
print("Average Transactions Revenue: ", df["revenue"].mean())
print("Top Product : ", product_df["total_revenue"].idxmax())
print("Top Product Revenue: ", product_df["total_revenue"].max())
print("Top 3 Revenue Share: ", top_products["revenue_share_percent"].sum())
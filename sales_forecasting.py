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

# monthly df
month_df = df.groupby("year_month").agg(
    revenue=("revenue" , 'sum'),
    quantity=("quantity" , 'sum'),
    transactions=("revenue" , 'count'),
    avg_transactions=("revenue" , 'mean')
)

# growth
growth_df = month_df[["revenue", "quantity"]].pct_change() * 100
growth_df.columns = ["revenue_growth_%", "quantity_growth_%"]

# rolling average
month_df["three_month_avg_rev"] = month_df["revenue"].rolling(3).mean()

# by product 
product_df = df.groupby("product").agg(
    total_revenue=("revenue" , 'sum'),
    total_quantity=("quantity" , 'sum'),
    avg_unit_price=("unit_price" , 'mean')
)

# product & month
df = df.sort_values("year_month")
monthly_product_df = df.groupby(["product", "year_month"]).agg(
    total_revenue=("revenue" , 'sum'),
    total_quantity=("quantity" , 'sum'),
    avg_unit_price=("unit_price" , 'mean'),
)

first_last_df = monthly_product_df.groupby("product").agg(
    first_month_rev=("total_revenue" , 'first'),
    last_month_rev=("total_revenue" , 'last')
)

first_last_df["growth%"] = (first_last_df["last_month_rev"] - first_last_df["first_month_rev"]) / first_last_df["first_month_rev"] * 100

# reports
print("==================== Monthly Sales REPORT ====================", "\n")
print(month_df)
print("Monthly Growth Percent", "\n", growth_df)
print("3 Month Average Revenue: ", "\n", month_df["three_month_avg_rev"])
print("\n", "===================== Product Trend =====================", "\n")
print(product_df)
print(monthly_product_df)
print(first_last_df)

# plots
month_df["revenue"].plot(kind='bar')
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

month_df[["revenue", "three_month_avg_rev"]].plot(kind='line')
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

product_df["total_revenue"].plot(kind='bar')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.show()
# CLV = customer lifetime value
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
df = data_cleaner(df, "number", ["orders", "total_spent", "avg_order_value", "customer_age_months"])
df["returns"] = pd.to_numeric(df["returns"], errors="coerce")
df.dropna()
df = df[df["returns"] >= 0]

# required columns calculation
df["customer_value_per_month"] = df["total_spent"] / df["customer_age_months"] 

df["return_rate"] = df["returns"] / df["orders"] * 100
avg_return_rate = df["returns"].sum() / df["orders"].sum() * 100

# segmentation
def segment(spent):
    if spent >= 30000000:
        return "High Value"
    elif spent < 15000000:
        return "Low Value"
    else:
        return "Medium Value"

df["segment"] = df["total_spent"].apply(segment)
df_by_segment = df.groupby("segment").agg(
    customer_count=("customer" , "count"),
    total_spent=("total_spent" , "sum"),
    average_spent=("total_spent" , "mean"),
    returns=("returns" , "sum"),
    orders=("orders" , "sum")
)
df_by_segment["average_return_rate"] = df_by_segment["returns"] / df_by_segment["orders"] * 100

# reports
print("=================== OVERALL REPORT ===================", "\n")
print("Total Customers: ", df["customer"].nunique())
print("Total Orders: ", df["orders"].sum())
print("Total Spent: ", df["total_spent"].sum())
print(f'Average Customer Spending: {df["total_spent"].mean():,.2f}')
print(f'Average Orders per Customer: {df["orders"].mean():,.2f}')
print(f'Average Return Rate: {avg_return_rate:,.2f}')
print("\n", "------------- Analysis by Customer -------------", "\n")
print("Top 3 Customer by Total Spent: ", "\n", df.nlargest(3, "total_spent"))
print("Top 3 Customer by Orders: ", "\n", df.nlargest(3, "orders"))
print("Top 3 Customer by Value per Month: ", "\n", df.nlargest(3, "customer_value_per_month"))
print("Top 3 Customer by Average Order Value: ", "\n", df.nlargest(3, "avg_order_value"))
print("\n", "------------- Customer Segmentation ------------", "\n")
print(df_by_segment)

# plots
df.set_index("customer")["total_spent"].plot(kind='bar')
plt.title("Total Spent by Customer")
plt.xlabel("Customer")
plt.ylabel("Total spent")
plt.show()

df.set_index("customer")["customer_value_per_month"].plot(kind='bar')
plt.title("Customer Value Per Month by Customer")
plt.xlabel("Customer")
plt.ylabel("Customer Value Per Month")
plt.show()

size = df_by_segment["customer_count"]
plt.pie(size, labels=size.index)
plt.title("Customer Segment Distribution")
plt.show()
import pandas as pd
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

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna()
df = df[df["quantity"] > 0]
df = df[df["price"] > 0]

# calculating revenue
df["revenue"] = df["price"] * df["quantity"]

total_rev = df["revenue"].sum()
sales_num = df["quantity"].sum()
avg_per_unit = total_rev / sales_num

count_seri = pd.Series(df.groupby("customer")["order_id"].nunique(), name="Order Count")
quant_seri = pd.Series(df.groupby("customer")["quantity"].sum(), name="Quantity of Product")
rev_seri = pd.Series(df.groupby("customer")["revenue"].sum(), name="Customer Revenue")

count_df = pd.DataFrame(count_seri)
quant_df = pd.DataFrame(quant_seri)
rev_df = pd.DataFrame(rev_seri)

frames = [count_df, quant_df, rev_df]
customer_df = pd.concat(frames, axis=1)

# average order value
customer_df["AOV"] = customer_df["Customer Revenue"] / customer_df["Order Count"]

order_num = customer_df["Order Count"].sum()
maxi = customer_df["Customer Revenue"].idxmax()
mini = customer_df["Customer Revenue"].idxmin()

selected_1 = customer_df[customer_df["Order Count"] == 1]
selected_m = customer_df[customer_df["Order Count"] > 1]

#print report
print("=============== OVERALL REPORT ===============", "\n")
print("Number of records: ", raw_num)
print("Number of computable orders: ", order_num)
print("Highest revenue by customer: ", customer_df.loc[maxi], "-", customer_df.loc[maxi, "Customer Revenue"])
print("Lowest revenue by customer: ", customer_df.loc[mini], "-", customer_df.loc[mini, "Customer Revenue"], "\n")
print("----------------- BY CUSTOMER ----------------")
print(customer_df, "\n")
print("==============================================","\n")
print("Best 3 customers by revenue", "\n")
print(customer_df.nlargest(3, ["Customer Revenue"]))
print("==============================================","\n")
print("Best 3 customers by average order value")
print(customer_df.nlargest(3, ["AOV"]))
print("==============================================","\n")
print("Best 3 customers by quantity of orders (Loyal customer)")
print(customer_df.nlargest(3, ["Order Count"]))
print("==============================================","\n")
print("Customers by just one order", selected_1)
print("----------------------------------------------")
print("Returning customers", selected_m)
print("==============================================","\n")
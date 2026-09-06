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
colomns_name = ["stock", "unit_price", "sold_last_30_days", "reorder_level"]
df = data_cleaner(df, "number", colomns_name)

# calculations
df["inventory_value"] = df["stock"] * df["unit_price"]

def reorder(row):
    if row["stock"] <= row["reorder_level"]:
        return "Reorder"
    else:
        return "OK"

df["reorder_status"] = df.apply(reorder, axis=1)
reorder_products = df[df["reorder_status"] == 'Reorder']

# print report
print("=============== OVERALL REPORT ===============", "\n")
print("Number of products: ", df["product"].count())
print("Average inventory of product: ", df["stock"].mean())
print("Total current value of the warehouse: ", df["inventory_value"].sum())
print("\n", "---------- Products requiring order ----------", "\n")
print(reorder_products[["product", "stock", "reorder_level", "reorder_status"]])
print("\n", "----------- Best selling products -----------", "\n")
print(df.nlargest(3, "sold_last_30_days"))
print("\n", "-------- Inventory value by category --------", "\n")
print(df.groupby("category")["inventory_value"].sum())

# plots
df.groupby("reorder_status")["product"].count().plot(kind='bar', legend=False)
plt.title("Reorder status")
plt.xlabel("Status")
plt.ylabel("Number")
plt.show()

size = df.groupby("category")["inventory_value"].sum()
plt.pie(size, labels=size.index)
plt.title("Inventory value by category")
plt.show()
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
colomns_name = ["age", "total_orders", "total_spent", "last_order_days_ago"]
df = data_cleaner(df, "number", colomns_name)

# calculation
max_spent = df["total_spent"].idxmax()
min_spent = df["total_spent"].idxmin()

df["AOV"] = df["total_spent"] / df["total_orders"]

# segmentation
def segment(spent):
    if spent >= 15000000:
        return "VIP"
    elif spent < 8000000:
        return "Low Value"
    else:
        return "Regular"

df["segment"] = df["total_spent"].apply(segment)

# customer activity
def activity(days):
    if days <= 10:
        return "Active"
    elif days > 30:
        return "Inactive"
    else:
        return "At risk"
    
df["activity"] = df["last_order_days_ago"].apply(activity)

#print report
print("================ OVERALL REPORT ================", "\n")
print("Number of customers: ", df["customer"].count())
print("Average customers age: ", df["age"].mean())
print("Average of order number: ", df["total_orders"].mean())
print("Highest spent: ", df.loc[max_spent, "customer"], "-", df.loc[max_spent, "total_spent"])
print("Lowest spent: ", df.loc[min_spent, "customer"], "-", df.loc[min_spent, "total_spent"], "\n")
print("------------ TOP CUSTOMER BY SPENT ------------")
print(df.nlargest(3, "total_spent"))
print("------------ TOP CUSTOMER BY ORDER ------------")
print(df.nlargest(3, "total_orders"))
print("----------- TOP AVERAGE ORDER VALUE -----------")
print(df.nlargest(3, "AOV"), "\n")
print("Number of customer in each segment:")
print(df.groupby("segment")["customer"].count())

# plots
size = df["segment"].value_counts().reindex(["Low Value", "Regular", "VIP"])
plt.pie(size, labels=size.index)
plt.show()

segment_means_df = df.groupby("segment")["total_spent"].mean()
segment_means_df.plot(kind='bar')
plt.title("Total spent of each segment")
plt.xlabel("segment")
plt.ylabel("total_spent")
plt.show()
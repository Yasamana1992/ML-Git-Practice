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
df = data_cleaner(df, "number", ["transaction_id", "amount"])

# find anomaly status
def status(amount, median):
    if amount > median * 3:
        return "Suspicious"
    else:
        return "Normal"

df["anomaly_status"] = df["amount"].apply(
    lambda amount: status(amount, df["amount"].median())
    )

suspicious_df = df[df["anomaly_status"] == "Suspicious"]

# df by customer
customer_df = df.groupby("customer").agg(
    transaction_count=("transaction_id" , "count"),
    total_spent=("amount" , "sum"),
    average_spent=("amount" , "mean"),
    suspicious_transaction_count=("anomaly_status" , lambda x: (x=="Suspicious").sum())
)
# df by city
city_df = df.groupby("city").agg(
    transaction_count=("transaction_id" , "count"),
    total_spent=("amount" , "sum"),
    average_spent=("amount" , "mean"),
    suspicious_transaction_count=("anomaly_status" , lambda x: (x=="Suspicious").sum())
)

# reports
print("=================== OVERALL REPORT ===================", "\n")
print("Total Transactions: ", df["transaction_id"].count())
print("Total Amount: ", df["amount"].sum())
print(f'Average Transactions Amount: {df["amount"].mean():,.2f}')
print("Median Transactions Amount: ", df["amount"].median())
print("Maximum Transactions Amount: ", df["amount"].max())
print("Minimum TransactionsAmount: ", df["amount"].min())
print("\n", "---------- Suspicious Transactions Analysis ----------", "\n")
print("Total Transactions: ", suspicious_df["transaction_id"].count())
print("Total Amount: ", suspicious_df["amount"].sum())
print(f'Average Transactions Amount: {suspicious_df["amount"].mean():,.2f}')
print(f'Percent of Suspicious Transactions: {suspicious_df["transaction_id"].count() / df["transaction_id"].count() * 100:,.2f}')
print(f'Percent of Suspicious Transactions Amount: {suspicious_df["amount"].sum() / df["amount"].sum() * 100:,.2f}')
print("\n", "--------------- Analysis by Customer ---------------", "\n")
print(customer_df)
print("Top 3 Customer by Total Amount: ", "\n", customer_df.nlargest(3, "total_spent"))
print("Customers with Suspicious Transactions: ", customer_df[customer_df["suspicious_transaction_count"] > 0])
print("\n", "----------------- Analysis by City -----------------", "\n")
print(city_df)
print("City with Maximum Suspicious Transactions: ", city_df["suspicious_transaction_count"].idxmax())

# plots
plt.hist(df["amount"], bins=30)
plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.show()

city_df["total_spent"].plot(kind='bar')
plt.title("Total Spent by City")
plt.xlabel("City")
plt.ylabel("Total spent")
plt.show()

count_size = df.groupby("anomaly_status")["transaction_id"].count()
amount_size = df.groupby("anomaly_status")["amount"].sum()

fig , axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
axes[0].pie(count_size, labels=count_size.index)
axes[0].set_title("Normal vs Suspicious Transactions by Count")

axes[1].pie(amount_size, labels=amount_size.index)
axes[1].set_title("Normal vs Suspicious Transactions by Amount")

plt.tight_layout()
plt.show()
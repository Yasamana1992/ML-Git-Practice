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
df = data_cleaner(df, "number", ["order_id", "amount"])
df = data_cleaner(df, "date", ["date"])

# RFM table
last_date = df["date"].max()
rfm_df = df.groupby("customer").agg(
    recency=("date" , lambda x : (last_date - x.max()).days),
    frequency=("order_id" , 'count'),
    monetary=("amount" , 'sum')
)

# customer segmentation
def segment(recency, frequency, monetary):
    if (monetary >= 2000000 and frequency >= 4):
        return "High Value"
    elif recency > 30:
        return "At Risk"
    elif (monetary < 1700000 and frequency < 3):
        return "Low Value"
    else:
        return "Loyal"

rfm_df["segment"] = rfm_df[["recency", "frequency", "monetary"]].apply(
     lambda row: segment((row["recency"]),
                      row["frequency"],
                       row["monetary"]), axis=1
)

print(rfm_df)

# reports
print("====================== REPORT ======================", "\n")
print("Total Customers: ", df["customer"].nunique())
print(f'Average Recency: {rfm_df["recency"].mean():,.2f}')
print(f'Average Frequency: {rfm_df["frequency"].mean():,.2f}')
print(f'Average Monetary: {rfm_df["monetary"].mean():,.2f}')
print("Customers of each Segment: ", "\n", rfm_df.groupby("segment").size().reset_index(name="customer_count"))
print("Total Monetary of each Segment: ", "\n", rfm_df.groupby("segment")["monetary"].sum())

# plots
count_size = rfm_df.groupby("segment").size()
amount = rfm_df.groupby("segment")["monetary"].sum()

fig , axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
axes[0].pie(count_size, labels=count_size.index)
axes[0].set_title("Customer Count of each Segment")

axes[1].pie(amount, labels=amount.index)
axes[1].set_title("Total Monetary of each Segment")

plt.tight_layout()
plt.show()

fig , axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
rfm_df["monetary"].plot(kind='bar', ax=axes[0])
axes[0].set_title("Monetary by Customer")
axes[0].set_xlabel("Customer")
axes[0].set_ylabel("Amount")

rfm_df["frequency"].plot(kind='bar', ax=axes[1])
axes[1].set_title("Frequency by Customer")
axes[1].set_xlabel("Customer")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.show()
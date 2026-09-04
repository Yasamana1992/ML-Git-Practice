import pandas as pd
from data_analysis_tools import statistics
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

df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna()
df = df[df["amount"] > 0]

sts = statistics(df, ["amount"])

#print report
print("=============== OVERALL REPORT ===============", "\n")
print("Number of records: ", raw_num)
print("Number of valid transactions: ", sts.loc[sts["operation"] == 'count', "value"].iloc[0])
print("Total costs", sts.loc[sts["operation"] == 'sum', "value"].iloc[0])
print("Average costs", sts.loc[sts["operation"] == 'mean', "value"].iloc[0])
max_index = df["amount"].idxmax()
print("Highest cost: " +"\n"+ "Category: "+ df.loc[max_index, "category"] + "\n"+ "Amount:", df.loc[max_index, "amount"] , "\n")
min_index = df["amount"].idxmin()
print("Lowest cost: "+ "\n"+ "Category: " + df.loc[min_index, "category"] + "\n"+ "Amount:" , df.loc[min_index, "amount"] , "\n")
print("---------------- BY CATEGORY ----------------")
print(df.groupby("category")["amount"].sum())
print("------------- BY PAYMENT METHOD -------------")
print(df.groupby("payment_method")["amount"].sum())
print("----------------- BY MONTH ------------------")
df["year_month"] = df["date"].dt.to_period("M")
month_df = df.groupby("year_month")["amount"].sum()
print(month_df)

month_df.plot(kind='bar')
plt.title("Total costs per month")
plt.xlabel("Month")
plt.ylabel("Costs")
plt.show()
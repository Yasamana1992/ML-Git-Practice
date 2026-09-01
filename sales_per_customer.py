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

def aggregation_df(dataframe, by, feature, operation, title):
    opr_list = ["sum", "count", "nunique", "mean"]

    if operation in opr_list:
        grouped = dataframe.groupby(by)[feature]
        opr = getattr(grouped, operation)()
        seri = pd.Series(opr, name=title)
        return pd.DataFrame(seri)
    else:
        return "operation not found"

count_df = aggregation_df(df, "customer", "order_id", "nunique", "Order Count")
quant_df = aggregation_df(df, "customer", "quantity", "sum", "Quantity of Product")
rev_df = aggregation_df(df, "customer", "revenue", "sum", "Customer Revenue")

frames = [count_df, quant_df, rev_df]
customer_df = pd.concat(frames, axis=1)

def top_reports(dataframe, n, feature):
    ftr_list = dataframe.columns
    if feature in ftr_list:
        return dataframe.nlargest(n, feature)
    else:
        return "feature not found"

def print_top(dataframe, n, features):
    for feature in features:
        print("==============================================","\n")
        print("Best", n, "customers by" ,feature , "\n")
        print(top_reports(dataframe, n, feature))

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
features = ["Customer Revenue", "AOV", "Order Count"]
print_top(customer_df, 3, features)
print("==============================================","\n")
print("Customers by just one order", selected_1)
print("----------------------------------------------")
print("Returning customers", selected_m)
print("==============================================","\n")
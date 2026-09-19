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
df = data_cleaner(df, "number", ["age", "months_active", "total_orders", "total_spent", "last_order_days_ago"])
df["support_tickets"] = pd.to_numeric(df["support_tickets"], errors="coerce")
df = df.dropna()
df = df[df["support_tickets"] >= 0]

# churn dataframe
churn_df = df.groupby("churned").agg(
    customer_count=("customer" , 'count'),
    avg_months_active=("months_active" , 'mean'),
    avg_orders= ("total_orders" , 'mean'),
    avg_total_spent= ("total_spent" , 'mean'),
    avg_last_order_days= ("last_order_days_ago" , 'mean'),
    avg_support_tickets= ("support_tickets" , 'mean')
)
churned_count = int(churn_df.loc["Yes", "customer_count"])

# city dataframe
city_df = df.groupby("city").agg(
    customer_count=("customer" , 'count'),
    churned_count=("churned" , lambda x: (x=="Yes").sum()),
    avg_spent=("total_spent" , 'mean')
)
city_df["churn_rate"] = city_df["churned_count"] / city_df["customer_count"] * 100

# customer value
df["value_per_month"] = df["total_spent"] / df["months_active"]

# risk flag
def flag(days, tickets):
    if (days > 60 and tickets >= 4):
        return "High Risk"
    else:
        return "Normal"

df["risk_flag"] = df[["last_order_days_ago", "support_tickets"]].apply(
     lambda row: flag((row["last_order_days_ago"]),
                      row["support_tickets"]), axis=1
)

high_risk_df = df.loc[df["risk_flag"] == "High Risk"]

# reports
print("=================== OVERALL REPORT ===================", "\n")
print("Total Customers: ", df["customer"].count())
print("Churned Customers: ", churned_count)
print("Active Customers: ", df["customer"].count() - churned_count)
print(f'Churn Rate: {churned_count / df["customer"].count() * 100:,.2f}')
print(f'Average Total Spent: {df["total_spent"].mean():,.2f}')
print(f'Average Orders: {df["total_orders"].mean():,.2f}')
print(f'Average Last Order Days: {df["last_order_days_ago"].mean():,.2f}')
print("\n", "-------------- Churned vs Active ---------------", "\n")
print(churn_df)
print("\n", "--------------- Analysis by City ---------------", "\n")
print(city_df)
print("City with Maximum Churn Rate: ", city_df["churn_rate"].idxmax())
print("\n", "------------- Analysis by Customer -------------", "\n")
print("Top 3 Customer by Total Spent: ", "\n", df.nlargest(3, "total_spent"))
print("Top 3 Customer by Value per Month: ", "\n", df.nlargest(3, "value_per_month"))
print("\n", "---------------- Risk Analysis ----------------", "\n")
print(high_risk_df)
print("High Risk Customer Count: ", high_risk_df["risk_flag"].count())
print("Churned Percent: ", high_risk_df["churned"].count() / high_risk_df["risk_flag"].count() * 100)

# plots
status_df = df.groupby("churned")["customer"].count()
status_df.index = status_df.index.map({
    "Yes": "churned",
    "No": "Active"
})
status_df.plot(kind='bar')
plt.title("Churned vs Active Customers")
plt.xlabel("Churned")
plt.ylabel("Customers count")
plt.show()

city_df["churn_rate"].plot(kind='bar')
plt.title("Churn Rate by City")
plt.xlabel("City")
plt.ylabel("Churn Rate")
plt.show()

size = df.groupby("churned")["total_spent"].sum()
size.index = size.index.map({
    "Yes": "churned",
    "No": "Active"
})
plt.pie(size, labels=size.index)
plt.title("Churned vs Active Customers Total Spent")
plt.show()


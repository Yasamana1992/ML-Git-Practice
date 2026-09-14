import pandas as pd
from data_analysis_tools import data_cleaner
import matplotlib.pyplot as plt
import seaborn as sns

# load data
while True:
    try:
        df = pd.read_csv(input("What is the file name? ")+'.csv')
        break
    except FileNotFoundError:
        print("File not found!")

# cleaning data
raw_num = len(df)
df = data_cleaner(df, "number", ["amount"])
df = data_cleaner(df, "date", ["date"])

# month column
df["year_month"] = df["date"].dt.to_period("M")
df = df.sort_values(by=["year_month"])

# cohort month
print(df.groupby("customer")["year_month"].first())
df_cohort = pd.DataFrame(df.groupby("customer")["year_month"].first())
df_cohort["cohort_month"] = df_cohort["year_month"]
df_cohort = df_cohort.reset_index()
new_df = df.merge(right=df_cohort[["cohort_month", "customer"]], how="right", on="customer")

# cohort size
cohort_size = new_df.groupby(["cohort_month", "year_month"])["customer"].nunique()

new_df["cohort_size"] = (new_df.groupby("cohort_month")["customer"].transform("nunique"))
selected_df = new_df[["customer", "year_month", "cohort_month", "cohort_size"]]
cohort_table = selected_df.groupby(["cohort_month", "year_month", "cohort_size"])["customer"].nunique().reset_index(name="active")
print(cohort_table)

# retention calculate
cohort_table = pd.DataFrame(cohort_table)
cohort_table["%Retention"] = (cohort_table["active"] / cohort_table["cohort_size"]) * 100
print(cohort_table)
print(new_df.groupby(["cohort_month", "year_month"])["customer"].unique())

# plots
size = cohort_table.groupby("cohort_month")["%Retention"].mean()
size.plot()
plt.title("Average retention per month")
plt.xlabel("Month")
plt.ylabel("Retention")
plt.show()

cohort_retention = cohort_table.pivot(index="cohort_month", columns="year_month", values="%Retention")
print(cohort_retention)

for cohort in cohort_retention.index:
    plt.plot(cohort_retention.columns.astype(str), cohort_retention.loc[cohort], label = cohort)
plt.title("Retention per month")
plt.xlabel("Month")
plt.ylabel("Retention")
plt.show()

sns.heatmap(cohort_retention)
plt.title("Retention per month")
plt.xlabel("Month")
plt.ylabel("Retention")
plt.show()
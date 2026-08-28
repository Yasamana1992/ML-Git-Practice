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

# calculating required items for report

clean_num = len(df)
total_revenue = df["revenue"].sum()
count = df["quantity"].sum()
avg_per_sale = total_revenue / count
maxi = df["revenue"].idxmax()
mini = df["revenue"].idxmin()

#report by product
quant_seri = pd.Series(df.groupby("product")["quantity"].sum(), name="Quantity")
rev_seri = pd.Series(df.groupby("product")["revenue"].sum(), name="Revenue")

def grouped_weighted_avg(values, weights, by):
    return (values * weights).groupby(by).sum() / weights.groupby(by).sum()

m_df = grouped_weighted_avg(values=df["price"], weights=df["quantity"], by=df["product"])
mean_seri = pd.Series(m_df, name="Weighted Average")

quant_df = pd.DataFrame(quant_seri)
rev_df = pd.DataFrame(rev_seri)
mean_df = pd.DataFrame(mean_seri)

frames = [mean_df, quant_df, rev_df]
table = pd.concat(frames, axis=1)

#report by category
q_seri_cat = pd.Series(df.groupby("category")["quantity"].sum(), name="Quantity")
r_seri_cat = pd.Series(df.groupby("category")["revenue"].sum(), name="Revenue")

m_df_cat = grouped_weighted_avg(values=df["price"], weights=df["quantity"], by=df["category"])
m_seri_cat = pd.Series(m_df_cat, name="Weighted Average")

q_df_cat = pd.DataFrame(q_seri_cat)
r_df_cat = pd.DataFrame(r_seri_cat)
m_df_cat = pd.DataFrame(m_seri_cat)

frames_c = [m_df_cat, q_df_cat, r_df_cat]
table_cat = pd.concat(frames_c, axis=1)

#report by date
q_seri_date = pd.Series(df.groupby("date")["quantity"].sum(), name="Quantity")
r_seri_date = pd.Series(df.groupby("date")["revenue"].sum(), name="Revenue")

#make dataframe to find best days
frames_date = [q_seri_date, r_seri_date]
date_df = pd.concat(frames_date, axis=1)

df["year_month"] = df["date"].dt.to_period("M")

q_seri_month = pd.Series(df.groupby("year_month")["quantity"].sum(), name="Quantity")
r_seri_month = pd.Series(df.groupby("year_month")["revenue"].sum(), name="Revenue")

m_df_month = grouped_weighted_avg(values=df["price"], weights=df["quantity"], by=df["year_month"])
m_seri_month = pd.Series(m_df_month, name="Weighted Average")

q_df_month = pd.DataFrame(q_seri_month)
r_df_month = pd.DataFrame(r_seri_month)
m_df_month = pd.DataFrame(m_seri_month)

frames_m = [m_df_month, q_df_month, r_df_month]
table_month = pd.concat(frames_m, axis=1)

#print report
print("=============== OVERALL REPORT ===============", "\n")
print("Number of records: ", raw_num)
print("Number of computable records: ", clean_num)
print("Total revenue: ", total_revenue)
print("Average sale per unit: ", avg_per_sale)
print("Highest revenue: ", df.loc[maxi, "product"], "-", df.loc[maxi, "revenue"])
print("Lowest revenue: ", df.loc[mini, "product"], "-", df.loc[mini, "revenue"], "\n")
print("----------------- BY PRODUCT ----------------")
print(table, "\n")
print("---------------- BY CATEGORY ----------------")
print(table_cat, "\n")
print("----------------- BY MONTH ------------------")
print(table_month, "\n")
print("==============================================","\n")
print("Best product by revenue: ", rev_df.idxmax())
print("Total revenue of this product:", rev_df.max(), "\n")
print("Best product by quantity: ", quant_df.idxmax())
print("Total number of sales:", quant_df.max(), "\n")
print("Best category by revenue: ", r_df_cat.idxmax())
print("Total revenue of this category:", r_df_cat.max(), "\n")
print("Best category by quantity: ", q_df_cat.idxmax())
print("Total number of sales:", q_df_cat.max(), "\n")
print("Best month by revenue: ", r_df_month.idxmax())
print("Total revenue in this month:", r_df_month.max(), "\n")
print("Best month by quantity: ", q_df_month.idxmax())
print("Total number of sales:", q_df_month.max(), "\n")
print("==============================================","\n")
print("Best 10 days by revenue", "\n")
print(date_df.nlargest(10, ["Revenue"]))
print("==============================================","\n")
print("Best 10 days by quantity of sale")
print(date_df.nlargest(10, ["Quantity"]))

table_month["Revenue"].plot(kind='bar')
plt.title("Revenue per month")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()
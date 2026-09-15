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
df = data_cleaner(df, "number", ["impressions", "clicks", "conversions", "ad_spend", "revenue"])
df = data_cleaner(df, "date", ["date"])

# making required columns
# click rate
df["ctr"] = (df["clicks"] / df["impressions"]) * 100
overall_ctr = (df["clicks"].sum() / df["impressions"].sum()) * 100

# conversion rate of click to purchase
df["conversion_rate"] = (df["conversions"] / df["clicks"]) * 100
overall_conv_rate = (df["conversions"].sum() / df["clicks"].sum()) * 100

# cost of attracting each customer
df["cac"] = df["ad_spend"] / df["conversions"]

# return on advertising spend
df["roas"] = df["revenue"] / df["ad_spend"]
overall_roas = df["revenue"].sum() / df["ad_spend"].sum()

# calculation by channel
df_by_channel = df.groupby("channel").agg({"impressions": "sum",
                                            "clicks": "sum",
                                            "conversions": "sum",
                                            "ad_spend": "sum",
                                            "revenue": "sum"})

df_by_channel["ctr"] = (df_by_channel["clicks"] / df_by_channel["impressions"]) * 100

df_by_channel["conversion_rate"] = (df_by_channel["conversions"] / df_by_channel["clicks"]) * 100

df_by_channel["roas"] = df_by_channel["revenue"] / df_by_channel["ad_spend"]

# calculation by campaign
df_by_campaign = df.groupby("campaign").agg({"conversions": "sum",
                                            "ad_spend": "sum",
                                            "revenue": "sum"})

df_by_campaign["roas"] = df_by_campaign["revenue"] / df_by_campaign["ad_spend"]

df_by_campaign["cac"] = df_by_campaign["ad_spend"] / df_by_campaign["conversions"]

# reports
print("=============== OVERALL REPORT ===============", "\n")
print("Total Impressions: ", df["impressions"].sum())
print("Total Clicks: ", df["clicks"].sum())
print("Total Conversions: ", df["conversions"].sum())
print("Total Ad Spend: ", df["ad_spend"].sum())
print("Total Revenue: ", df["revenue"].sum())
print(f"Overall CTR(click rate): {overall_ctr:,.2f}")
print(f"Overall Conversion Rate: {overall_conv_rate:,.2f}")
print(f"Overall ROAS(return on advertising spend): {overall_roas:,.2f}")
print("\n", "------------ Analysis by channel ------------", "\n")
print("Total Impressions: ", "\n", df_by_channel["impressions"])
print("Total Clicks: ", "\n", df_by_channel["clicks"])
print("Total Conversions: ", "\n", df_by_channel["conversions"])
print("Total Ad Spend: ", "\n", df_by_channel["ad_spend"])
print("Total Revenue: ", "\n", df_by_channel["revenue"])
print("CTR: ", "\n", df_by_channel["ctr"])
print("Conversion Rate: ", "\n", df_by_channel["conversion_rate"])
print("ROAS: ", "\n", df_by_channel["roas"])
print("Best channel by ROAS: ", df_by_channel["roas"].idxmax())
print("Best channel by Revenue: ", df_by_channel["revenue"].idxmax())
print("\n", "----------- Analysis by campaign -----------", "\n")
print("Total Revenue: ", "\n", df_by_campaign["revenue"])
print("Total Ad Spend: ", "\n", df_by_campaign["ad_spend"])
print("Total Conversions: ", "\n", df_by_campaign["conversions"])
print("ROAS: ", "\n", df_by_campaign["roas"])
print("CAC: ", "\n", df_by_campaign["cac"])
print("3 Top campaigns by ROAS: ", "\n", df_by_campaign.nlargest(3, ["roas"]))
print("3 Top campaigns by Revenue: ", "\n", df_by_campaign.nlargest(3, ["revenue"]))

# plots
df_by_channel["revenue"].plot(kind="bar")
plt.title("Revenue by channel")
plt.xlabel("Channel")
plt.ylabel("Revenue")
plt.show()

df_by_channel["roas"].plot(kind="bar")
plt.title("ROAS by channel")
plt.xlabel("Channel")
plt.ylabel("ROAS")
plt.show()

# month column
df["year_month"] = df["date"].dt.to_period("M")
df = df.sort_values(by=["year_month"])

df.groupby("year_month")["revenue"].sum().plot(kind='line')
plt.title("Revenue by date")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.show()
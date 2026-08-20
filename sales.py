import pandas as pd

while True:
    try:
        num = int(input("How many item do you have? "))
        break
    except ValueError:
        print("number please")

sales = []

for i in range(num):
    product = input("Name of product: ").strip().lower()
    valid = False
    while valid==False:
        try:
            price = int(input("Price: "))
            valid = True
        except ValueError:
            print("number please")
    sales.append({"product" : product, "price" : price})

df = pd.DataFrame(sales)

total = df["price"].sum()
avg = df["price"].mean()
maxi = df["price"].idxmax()
mini = df["price"].idxmin()

print("Total sales: ", total)
print("Average price: ", avg)
print("Highest sale: ", df.loc[maxi, "product"], "-", df.loc[maxi, "price"])
print("Lowest sale: ", df.loc[mini, "product"], "-", df.loc[mini, "price"])
print(df.groupby("product")["price"].count())
print(df.groupby("product")["price"].sum())

prd_list = list(df["product"])

found = False
while found == False:
    selected = input("which product do you want to analyze? ").strip().lower()
    for j in range(len(prd_list)):
        if  (prd_list[j] == selected):
            found = True
            break;

df["selected"] = (df["product"] == selected)

selected_df = df.loc[df["selected"]==True]
print("Product: ", selected)
print("Number of sales: ", selected_df["price"].count())
print("Total revenue: ", selected_df["price"].sum())
print("Average price: ", selected_df["price"].mean())

cdf = pd.Series(df.groupby("product")["price"].count(), name="Count")
sdf = pd.Series(df.groupby("product")["price"].sum(), name="Sum")
mdf = pd.Series(df.groupby("product")["price"].mean(), name="Mean")

count_df = pd.DataFrame(cdf)
sum_df = pd.DataFrame(sdf)
mean_df = pd.DataFrame(mdf)

frames = [count_df, sum_df, mean_df]
table = pd.concat(frames, axis=1)
print(table)
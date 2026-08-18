import pandas as pd

num = int(input("How many item do you have? "))
sales = []

for i in range(num):
    sales.append({"product" : input("Name of product: "), "price" : int(input("Price: "))})

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

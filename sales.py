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
        price = input("Price: ")
        number = price.isnumeric()
        if number==True:           
            valid = True
        else:
            q = input("If price of this item is not available, press y").strip().lower()
            if q == 'y':
                valid = True
                price = "not_available"
        
    sales.append({"product" : product, "price" : price})

df = pd.DataFrame(sales)
clean_df = df

clean_df["price"] = pd.to_numeric(df["price"], errors="coerce")

clean_df = df.dropna(subset=["price"])

total = clean_df["price"].sum()
avg = clean_df["price"].mean()
#maxi = clean_df["price"].idxmax()
#mini = clean_df["price"].idxmin()

cdf = pd.Series(clean_df.groupby("product")["price"].count(), name="Count")
sdf = pd.Series(clean_df.groupby("product")["price"].sum(), name="Sum")
mdf = pd.Series(clean_df.groupby("product")["price"].mean(), name="Mean")

count_df = pd.DataFrame(cdf)
sum_df = pd.DataFrame(sdf)
mean_df = pd.DataFrame(mdf)

frames = [count_df, sum_df, mean_df]
table = pd.concat(frames, axis=1)
print(table, "\n")

print("Best selling product: ", sdf.idxmax())
print("Total sales:", sdf.max(), "\n")
"""
this part is related to previous version report
print("Total sales: ", total)
print("Average price: ", avg)
print("Highest sale: ", df.loc[maxi, "product"], "-", df.loc[maxi, "price"])
print("Lowest sale: ", df.loc[mini, "product"], "-", df.loc[mini, "price"])
print(df.groupby("product")["price"].count())
print(df.groupby("product")["price"].sum())
"""


prd_list = list(clean_df["product"])

found = False
while found == False:
    selected = input("which product do you want to analyze? ").strip().lower()
    for j in range(len(prd_list)):
        if  (prd_list[j] == selected):
            found = True
            break;

clean_df["selected"] = (clean_df["product"] == selected)

selected_df = clean_df.loc[clean_df["selected"]==True]
print("Product: ", selected)
print("Number of sales: ", selected_df["price"].count())
print("Total sales: ", selected_df["price"].sum())
print("Average sale: ", selected_df["price"].mean())

if selected_df["price"].count() > 1:
    print("Highest sale: ", selected_df["price"].max())
    print("Lowest sale: ", selected_df["price"].min())
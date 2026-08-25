import pandas as pd

while True:
    try:
        num = int(input("How many item do you have? "))
        break
    except ValueError:
        print("number please")

#get data from user and make list of dictionaries

sales = []
for i in range(num):
    product = input("Name of product: ").strip().lower()
    valid = False
    while valid==False:
        try:
            quantity = int(input("Number of sales of this product: "))
            valid = True
        except ValueError:
            print("number please")
    valid = False
    while valid==False:
        price = input("Price: ")
        if price.isnumeric():
            price = int(price)  
            revenue = price * quantity       
            valid = True
        else:
            a = input("If price of this item is not available, press y").strip().lower()
            if a == 'y':
                valid = True
                price = "not_available"
                revenue = "not_available"
    sales.append({"product" : product, "price" : price, "quantity" : quantity, "revenue" : revenue})

#making pandas dataframe and cleaning data
df = pd.DataFrame(sales)
clean_df = df.copy()

clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")
clean_df = clean_df.dropna(subset=["price"])

# sorting
clean_df = clean_df.sort_values(by=["revenue"], ascending=False)

# report calculating 

total = clean_df["revenue"].sum()
count = clean_df["quantity"].sum()
avg = total / count
maxi = clean_df["revenue"].idxmax()
mini = clean_df["revenue"].idxmin()

qdf = pd.Series(clean_df.groupby("product")["quantity"].sum(), name="Quantity")
rdf = pd.Series(clean_df.groupby("product")["revenue"].sum(), name="Revenue")

def grouped_weighted_avg(values, weights, by):
    return (values * weights).groupby(by).sum() / weights.groupby(by).sum()

mdf = grouped_weighted_avg(values=clean_df["revenue"], weights=clean_df["quantity"], by=clean_df["product"])
mdf = pd.Series(mdf, name="Average")

quant_df = pd.DataFrame(qdf)
rev_df = pd.DataFrame(rdf)
mean_df = pd.DataFrame(mdf)

frames = [mean_df, quant_df, rev_df]
table = pd.concat(frames, axis=1)

print("=============== SALES REPORT ===============", "\n")
print("Number of records: ", num)
print("Total revenue: ", total)
print("Average sale: ", avg)
print("Highest revenue: ", clean_df.loc[maxi, "product"], "-", clean_df.loc[maxi, "revenue"])
print("Lowest revenue: ", clean_df.loc[mini, "product"], "-", clean_df.loc[mini, "revenue"], "\n")
print("---------------- BY PRODUCT ---------------")
print(table, "\n")
print("============================================","\n")
print("Best product by revenue: ", rdf.idxmax())
print("Total revenue:", rdf.max(), "\n")
print("Best product by quantity: ", qdf.idxmax())
print("Total sales:", qdf.max(), "\n")

# part 2: calculating of selected item
prd_list = list(clean_df["product"])

selected = input("which product do you want to analyze? ").strip().lower()
x = 0
for j in range(len(prd_list)):
    if (prd_list[j] == selected):
        break;
    else:
        x += 1

if (x == len(prd_list)):
    print("product not found")
else:
    # add a column to df to identify selected rows
    clean_df["selected"] = (clean_df["product"] == selected)
    selected_df = clean_df.loc[clean_df["selected"]==True]
    print("Product: ", selected)
    print("Number of sales: ", selected_df["quantity"].sum())
    print("Total revenue: ", selected_df["revenue"].sum())
    avg_s = selected_df["revenue"].sum() / selected_df["quantity"].sum()
    print("Average sale: ", avg_s)
    print("Average price: ", selected_df["price"].mean())

    if selected_df["price"].count() > 1:
        print("Highest revenue: ", selected_df["revenue"].max())
        print("Lowest unit revenue: ", selected_df["revenue"].min())
        print("Highest unit price: ", selected_df["price"].max())
        print("Lowest unit price: ", selected_df["price"].min())
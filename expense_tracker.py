import pandas as pd

expenses = []

while True:
    try:
        cnt = int(input("how many expense do you have? "))
        break
    except ValueError:
        print("number please")

for i in range(cnt):
    valid = False
    category = input("input category: ").strip().lower()
    while valid == False:
        try:
            amount = int(input("how much does cost? "))
            valid = True
        except ValueError:
            print("number please")
    expenses.append({"category" : category, "amount" : amount})    

df = pd.DataFrame(expenses)
print("============= EXPENSE REPORT =============", "\n")
print("Total expenses: ", cnt)

s = df["amount"].sum()
print("Total amount: ", s)

avg = df["amount"].mean()
print("Average expense: ", avg, "\n")

maxi = df["amount"].idxmax()
print("Highest expense: " +"\n"+ "Category: "+ df.loc[maxi, "category"] + "\n"+ "Amount:", df.loc[maxi, "amount"] , "\n")
mini = df["amount"].idxmin()
print("Lowest expense: "+ "\n"+ "Category: " + df.loc[mini, "category"] + "\n"+ "Amount:" , df.loc[mini, "amount"] , "\n")
print("----- By Category -----" + "\n")

cdf = pd.Series(df.groupby("category")["amount"].count(), name="Count")
sdf = pd.Series(df.groupby("category")["amount"].sum(), name="Total")
mdf = pd.Series(df.groupby("category")["amount"].mean(), name="Average")
prc = sdf * 100 / s
percentage = pd.Series(prc, name="Percentage")


count_df = pd.DataFrame(cdf)
sum_df = pd.DataFrame(sdf)
mean_df = pd.DataFrame(mdf)
prc_df = pd.DataFrame(percentage)

frames = [count_df, sum_df, mean_df, prc_df]
table = pd.concat(frames, axis=1)
print(table)
print("==========================================", "\n")

print("Highest spending category: ", sdf.idxmax())
print("Amount:", sdf.max(), "\n")

categories = list(df["category"])

found = False
while found == False:
    selected = input("which category do you want to analyze? ").strip().lower()
    for j in range(len(categories)):
        if  (categories[j] == selected):
            found = True
            break;
    if found == False:    
        print("Category not found!")

df["selected"] = (df["category"] == selected)

selected_df = df.loc[df["selected"]==True]
print("Category: ", selected)
print("Number of expenses: ", selected_df["amount"].count())
print("Total : ", selected_df["amount"].sum())
print("Average : ", selected_df["amount"].mean())

max_s = selected_df["amount"].idxmax()
print("Highest expense: ", selected_df.loc[max_s, "category"] , selected_df.loc[max_s, "amount"])
min_s = selected_df["amount"].idxmin()
print("Lowest expense: ", selected_df.loc[min_s, "category"] , selected_df.loc[min_s, "amount"])
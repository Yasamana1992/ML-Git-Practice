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

s = df["amount"].sum()
print("Total: ", s)

avg = df["amount"].mean()
print("Average: ", avg)

maxi = df["amount"].idxmax()
print("Highest expense: ", df.loc[maxi, "category"] , df.loc[maxi, "amount"])
mini = df["amount"].idxmin()
print("Lowest expense: ", df.loc[mini, "category"] , df.loc[mini, "amount"])

print(df.groupby("category")["amount"].count())
sum_cat = df.groupby("category")["amount"].sum()
print(sum_cat)

sum_df = pd.Series(sum_cat)

max_sum = sum_df.max()
max_cat = sum_df.idxmax()
print("Highest spending category: "+ max_cat)
print("Total:", max_sum)

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
import pandas as pd

expenses = []
cnt = int(input("how many expense do you have? "))

for i in range(cnt):
    expenses.append({"category" : input("input category: "), "amount" : int(input("how much does cost? "))})    

df = pd.DataFrame(expenses)
s = df["amount"].sum()
print("Total: ", s)

maxi = df["amount"].idxmax()
print("Highest expense: ", df.loc[maxi, "category"] , df.loc[maxi, "amount"])
mini = df["amount"].idxmin()
print("Lowest expense: ", df.loc[mini, "category"] , df.loc[mini, "amount"])

avg = df["amount"].mean()
print("Average: ", avg)

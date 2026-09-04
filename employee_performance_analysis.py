import pandas as pd
from data_analysis_tools import data_cleaner
from data_analysis_tools import statistics
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

colomns_name = ["age", "experience", "salary", "performance_score", "projects_completed"]

df = data_cleaner(df, "number", colomns_name)

sts = statistics(df, ["performance_score"])

#print report
print("=============== OVERALL REPORT ===============", "\n")
print("Number of records: ", raw_num)
print("Staff number: ", sts.loc[sts["operation"] == 'count', "value"].iloc[0])
print("Average salary: ", df["salary"].mean())
print("Average performance score: ", sts.loc[sts["operation"] == 'mean', "value"].iloc[0])
max_performance = sts.loc[sts["operation"] == 'idxmax', "value"].iloc[0]
print("Highest performance score: ", df.loc[max_performance, "employee"], "-", df.loc[max_performance, "performance_score"])
min_performance = sts.loc[sts["operation"] == 'idxmin', "value"].iloc[0]
print("Lowest performance score: ", df.loc[min_performance, "employee"], "-", df.loc[min_performance, "performance_score"], "\n")
print("---------------- BY DEPARTMENT ---------------")
print("staff number: ", df.groupby("department")["employee"].count())
print("Average salary: ", df.groupby("department")["salary"].mean())
print("Average performance score: ", df.groupby("department")["performance_score"].mean())
print("Total projects completed: ", df.groupby("department")["projects_completed"].sum())
print("******* TOP PERFORMANCE EMPLOYEES *******")
df_top_performance = df[df["performance_score"] >= 85]
print(df_top_performance.nlargest(3, "performance_score"))
print("****** TOP PERFORMANCE PER MILLION ******")
df["performance_per_million"] = df["performance_score"] / (df["salary"] / 1000000)
print(df.nlargest(3, "performance_per_million"))

df_performance_by_department = df.groupby("department")["performance_score"].mean()
df_performance_by_department.plot(kind='bar')
plt.title("Performance by department")
plt.xlabel("Department")
plt.ylabel("Performance")
plt.show()

df_projects_by_department = df.groupby("department")["projects_completed"].sum()
df_projects_by_department.plot(kind='bar')
plt.title("Projects completed by department")
plt.xlabel("Department")
plt.ylabel("Projects")
plt.show()
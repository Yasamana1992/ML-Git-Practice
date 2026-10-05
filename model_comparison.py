import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

# load data
while True:
    try:
        df = pd.read_csv(input("What is the file name? ")+'.csv')
        break
    except FileNotFoundError:
        print("File not found!")

# cleaning data
raw_num = len(df)
df = data_cleaner(df, "number", ["age", "monthly_spend", "total_orders", "days_since_last_order"])
df["support_tickets"] = pd.to_numeric(df["support_tickets"], errors="coerce")
df["churn"] = pd.to_numeric(df["churn"], errors="coerce")
df = df.dropna()
df = df[df["support_tickets"] >= 0]
df = df[df["churn"] >= 0]
df = df[df["churn"] <= 1]

# separating data
X = df[["age", "monthly_spend", "total_orders", "days_since_last_order", "support_tickets"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# models list and comparison
model_a = LogisticRegression()
model_b = DecisionTreeClassifier()
model_c = RandomForestClassifier()
model_d = GaussianNB()

# models that required standard scaling
model_k = make_pipeline(StandardScaler(), KNeighborsClassifier())
model_s = make_pipeline(StandardScaler(), SVC())

models = [model_a, model_b, model_c, model_d, model_k, model_s]
result = []

for model in models:
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    result.append({'model' : model, 'accuracy' : scores.mean()})

result_df = pd.DataFrame(result)
print(result_df)
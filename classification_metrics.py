import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

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

# models list 
model_a = make_pipeline(StandardScaler(), LogisticRegression())
model_b = RandomForestClassifier(random_state=42)
model_c = make_pipeline(StandardScaler(), SVC())

models = [model_a, model_b, model_c]

# scoring
scoring = {
    "accuracy" : "accuracy",
    "precision" : "precision",
    "recall" : "recall",
    "f1" : "f1"
}

# cross validation
result = []
for model in models:
    cv_result = cross_validate(model, X_train, y_train, cv=5, scoring=scoring)
    result.append({
        'model' : model, 'accuracy' : cv_result["test_accuracy"].mean(),
        'precision' : cv_result["test_precision"].mean(),
        'recall' : cv_result["test_recall"].mean(),
        'f1' : cv_result["test_f1"].mean()
        })

result_df = pd.DataFrame(result)
print(result_df)

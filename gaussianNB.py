import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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

# model and fitting
model = GaussianNB()
model.fit(X_train, y_train)

# prediction
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# evaluation
acc = accuracy_score(y_true=y_test, y_pred=y_pred)
cnf = confusion_matrix(y_true=y_test, y_pred=y_pred)
cls_report = classification_report(y_true=y_test, y_pred=y_pred)

print("Accuracy Score: ", acc)
print("Confusion Matrix: ", cnf)
print("Classification Report: ", cls_report)
print(y_pred_proba)
import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report, confusion_matrix
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
df = df[
    (df["support_tickets"] >= 0) &
    (df["churn"].between(0, 1))]

# separating data
X = df[["age", "monthly_spend", "total_orders", "days_since_last_order", "support_tickets"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# define model and fitting
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
model.fit(X_train, y_train)

print("Test labels:")
print(y_test.value_counts())

# prediction and evaluation
y_pred = model.predict(X_test)

print("Predictions:")
print(pd.Series(y_pred).value_counts())

recall = recall_score(y_true=y_test, y_pred=y_pred)
precision = precision_score(y_true=y_test, y_pred=y_pred)
f1 = f1_score(y_true=y_test, y_pred=y_pred)
clf = classification_report(y_true=y_test, y_pred=y_pred)
cm = confusion_matrix(y_true=y_test, y_pred=y_pred)

print("Recall: ", recall)
print("Precision: ", precision)
print("F1 score: ", f1)
print("Classification Report: ", clf)
print("Confusion Matrix: ", cm)
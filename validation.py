import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
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
df = data_cleaner(df, "number", ["age", "monthly_spend", "total_orders", "days_since_last_order"])
df["support_tickets"] = pd.to_numeric(df["support_tickets"], errors="coerce")
df["churn"] = pd.to_numeric(df["churn"], errors="coerce")
df = df.dropna()
df = df[
    (df["support_tickets"] >= 0) &
    ((df["churn"] == 1) | (df["churn"] == 0))]

# separating data
X = df[["age", "monthly_spend", "total_orders", "days_since_last_order", "support_tickets"]]
y = df["churn"]

X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42, stratify=y_train_val)

# define model and fitting
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
model.fit(X_train, y_train)

# prediction and threshold evaluation
y_val_pred = model.predict(X_val)
y_val_proba = model.predict_proba(X_val)[:, 1]

cost_fn = 100
cost_fp = 5

thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

for threshold in thresholds:
    y_val_pred = (y_val_proba >= threshold).astype(int)

    cm = confusion_matrix(y_val, y_val_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    total_cost = fn * cost_fn + fp * cost_fp

    print(
        f"Threshold: {threshold:.1f} | "
        f"FP: {fp} | FN: {fn} | "
        f"Total Cost: {total_cost}"
    )

print("Actual labels:")
print(y_val.value_counts())

print("Predicted probabilities:")
print(y_val_proba)

print("Probability range:")
print(y_val_proba.min(), y_val_proba.max())

y_test_pred_05 = (model.predict_proba(X_test)[:, 1] >= 0.5).astype(int)

cm_test = confusion_matrix(y_test, y_test_pred_05, labels=[0, 1])
tn, fp, fn, tp = cm_test.ravel()

print("Test Confusion Matrix:")
print(cm_test)
print("TN:", tn, "FP:", fp, "FN:", fn, "TP:", tp)
print("Test Cost:", fn * 100 + fp * 5)
import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
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

# prediction & roc_auc & roc curve
y_proba = model.predict_proba(X_test)

roc_score = roc_auc_score(y_test, y_proba[:, 1])

fpr, tpr, thresholds = roc_curve(y_test, y_proba[:, 1])
print("Fpr: ", fpr,"\n"+ "Tpr: ", tpr,"\n"+ "Thresholds: ", thresholds)

plt.plot(fpr, tpr, label="ROC")
plt.axline((0, 0), (1, 1))
plt.title("ROC")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.show()

# examine treshold
threshold = 0.7
y_pred_custom = (y_proba[:, 1] >= threshold).astype(int)

cnf = confusion_matrix(y_true=y_test, y_pred=y_pred_custom)
print("confusion_matrix for threshold = 0.7: ", cnf)

threshold = 0.3
y_pred_custom = (y_proba[:, 1] >= threshold).astype(int)

cnf = confusion_matrix(y_true=y_test, y_pred=y_pred_custom)
print("confusion_matrix for threshold = 0.3: ", cnf)

# higher threshold --> tpr tends to decrease
# lower threshold --> fpr tends to increase
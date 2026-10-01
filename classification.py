import pandas as pd
from data_analysis_tools import data_cleaner
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

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
model = LogisticRegression()
model.fit(X_train, y_train)

# prediction
y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)
y_pred_train = model.predict(X_train)

# evaluation
acc = accuracy_score(y_true=y_test, y_pred=y_pred)
cnf = confusion_matrix(y_true=y_test, y_pred=y_pred)
cls_report = classification_report(y_true=y_test, y_pred=y_pred)
acc_train = accuracy_score(y_true=y_train, y_pred=y_pred_train)

print(y_pred)
print(y_pred_prob)
print("Accuracy Score: ", acc)
print("Confusion Matrix: ", cnf)
print("Classification Report: ", cls_report)

X_eval = [[40, 400000, 6, 50, 4]]
y_eval = model.predict(X_eval)
y_eval_prob = model.predict_proba(X_eval)

print("Evaluation for new data ([40, 400000, 6, 50, 4]):", y_eval)
print("Probability:", y_eval_prob)

# Decision tree classification
# model and fit
model_tree = DecisionTreeClassifier(random_state=42)
model_tree.fit(X_train, y_train)

# prediction
y_pred_tree = model_tree.predict(X_test)
y_pred_tree_train = model_tree.predict(X_train)

# evaluation
acc_tree = accuracy_score(y_true=y_test, y_pred=y_pred_tree)
cnf_tree = confusion_matrix(y_true=y_test, y_pred=y_pred_tree)
cls_report_tree = classification_report(y_true=y_test, y_pred=y_pred_tree)
acc_tree_train = accuracy_score(y_true=y_train, y_pred=y_pred_tree_train)

print(y_pred_tree)
print("Accuracy Score Decision Tree: ", acc_tree)
print("Train Accuracy: ", acc_tree_train)
print("Confusion Matrix Decision Tree: ", cnf_tree)
print("Classification Report Decision Tree: ", cls_report_tree)

# effect of max depth
result = []

for i in range(3):
    a = i+1
    model_tree = DecisionTreeClassifier(max_depth=a, random_state=42)
    model_tree.fit(X_train, y_train)
    y_pred_tree = model_tree.predict(X_test)
    y_pred_tree_train = model_tree.predict(X_train)
    acc_tree = accuracy_score(y_true=y_test, y_pred=y_pred_tree)
    train_acc = accuracy_score(y_true=y_train, y_pred=y_pred_tree_train)
    result.append({"Depth" : i+1 , "Actual Tree Depth" : model_tree.tree_.max_depth , "Train Accuracy" : train_acc , "Test Accuracy" : acc_tree})

result_df = pd.DataFrame(result)
print(result_df)

# effect of any feature
model_depth1 = DecisionTreeClassifier(max_depth=1, random_state=42)
model_depth1.fit(X_train, y_train)

print(model_depth1.feature_importances_)

# Random Forest Classification
# model and fitting
model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)

# prediction
y_pred_rf = model_rf.predict(X_test)
y_pred_rf_train = model_rf.predict(X_train)

# evaluation
acc_rf = accuracy_score(y_true=y_test, y_pred=y_pred_rf)
acc_rf_train = accuracy_score(y_true=y_train, y_pred=y_pred_rf_train)
cnf_rf = confusion_matrix(y_true=y_test, y_pred=y_pred_rf)
cls_report_rf = classification_report(y_true=y_test, y_pred=y_pred_rf)

print(y_pred_rf)
print("Random Forest Accuracy Score: ", acc_rf)
print("Random Forest Train Accuracy: ", acc_rf_train)
print("Random Forest Confusion Matrix: ", cnf_rf)
print("Random Forest Classification Report: ", cls_report_rf)

# feature importance
print(model_rf.feature_importances_)

# overall result
overall_result = [
    {"Model" : "Logistic Regression" , "Train Accuracy" : acc_train , "Test Accuracy" : acc},
    {"Model" : "Decision Tree Classifier" , "Train Accuracy" : acc_tree_train , "Test Accuracy" : acc_tree},
    {"Model" : "Random Forest Classifier" , "Train Accuracy" : acc_rf_train , "Test Accuracy" : acc_rf}
]

overall_df = pd.DataFrame(overall_result)
print(overall_df)
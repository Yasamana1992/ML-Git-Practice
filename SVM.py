import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
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

scaler = StandardScaler()
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_test = scaler.transform(X_test)

# model and fitting
model = SVC()
model.fit(scaled_X_train, y_train)

# prediction
y_pred = model.predict(scaled_X_test)

# evaluation
acc = accuracy_score(y_true=y_test, y_pred=y_pred)
cnf = confusion_matrix(y_true=y_test, y_pred=y_pred)
cls_report = classification_report(y_true=y_test, y_pred=y_pred)

print("Accuracy Score: ", acc)
print("Confusion Matrix: ", cnf)
print("Classification Report: ", cls_report)

# effect of kernel
kernel = ['linear', 'rbf']
result = []

for a in kernel:
    model = SVC(kernel=a)
    model.fit(scaled_X_train, y_train)
    y_pred = model.predict(scaled_X_test)
    acc = accuracy_score(y_true=y_test, y_pred=y_pred)
    result.append({"kernel" : a , "Test Accuracy" : acc})

result_df = pd.DataFrame(result)
print(result_df)
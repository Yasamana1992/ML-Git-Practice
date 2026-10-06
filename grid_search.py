import pandas as pd
from data_analysis_tools import data_cleaner
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

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

# define parameter and model
param_grid = {
    "max_depth" : [1, 2, 3, 4, 5],
    "min_samples_split" : [2, 4, 6],
    "min_samples_leaf" : [1, 2, 3]
}

model = DecisionTreeClassifier(random_state=42)

# define grid search and fit the model
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)
print("Best estimator: ", grid_search.best_estimator_)

# predict by best parameters
best_param_model = grid_search.best_estimator_
best_param_model.fit(X_train, y_train)
y_pred = best_param_model.predict(X_test)
acc = accuracy_score(y_true=y_test, y_pred=y_pred)
print("Accuracy Score: ", acc)
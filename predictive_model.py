import pandas as pd
from data_analysis_tools import data_cleaner
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# load data
while True:
    try:
        df = pd.read_csv(input("What is the file name? ")+'.csv')
        break
    except FileNotFoundError:
        print("File not found!")

# cleaning data
raw_num = len(df)
df = data_cleaner(df, "number", ["ad_spend", "sales"])

# separating data
X = df[["ad_spend"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model
model = LinearRegression()
model.fit(X_train, y_train)

# prediction
y_pred = model.predict(X_test)

# evaluation
r2 = r2_score(y_true=y_test, y_pred=y_pred)
mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)

print("R2 Score: ", r2)
print("MAE: ", mae)

# plots
plt.scatter(X_test, y_test, color ='b')
plt.plot(X_test, y_pred, color ='r')
plt.show()

X_eval = pd.DataFrame({"ad_spend" : [12.5]})
y_eval = model.predict(X_eval)
print("Predicted sales for ad_spend = 12.5: ", y_eval[0])

train_pred = model.predict(X_train)
train_r2 = r2_score(y_train, train_pred)
print("Train R2:", train_r2)
print("Test R2:", r2)

import pickle

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn_pandas import DataFrameMapper

df = pd.read_csv("data/football.csv", parse_dates=[6])
df = df.sort_values(["name", "date"]).reset_index(drop=True)
df["yards"] = df["passing"] + df["rushing"] + df["receiving"]
df["yards_1"] = df.groupby("name")["yards"].shift(1)
df["yards_2"] = df.groupby("name")["yards"].shift(2)
df = df.dropna(subset=["yards_1", "yards_2"])

target = "yards"
y = df[target]
X = df[["position", "yards_1", "yards_2"]]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.10, random_state=42, shuffle=False
)

mapper = DataFrameMapper(
    [
        (["position"], [SimpleImputer(strategy="most_frequent"), LabelBinarizer()]),
        (["yards_1"], [SimpleImputer(), StandardScaler()]),
        (["yards_2"], [SimpleImputer(), StandardScaler()]),
    ],
    df_out=True,
)

model = LinearRegression()

pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
score = round(pipe.score(X_train, y_train), 2)

with open("pickles/pipe.pkl", "wb") as f:
    pickle.dump(pipe, f)

print("Success!")

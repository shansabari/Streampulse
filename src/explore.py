import pandas as pd

df = pd.read_csv("data/raw/netflix_titles.csv")
print(df.shape)
print(df.head())
print(df.isnull().sum())
print(df["type"].value_counts())
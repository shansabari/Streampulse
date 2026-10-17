import pandas as pd
from db import get_engine

engine = get_engine()

titles = pd.read_csv("data/processed/titles.csv", parse_dates=["date_added"])
titles["duration_value"] = titles["duration_value"].astype("Int64")
genres = pd.read_csv("data/processed/title_genres.csv")
countries = pd.read_csv("data/processed/title_countries.csv")

# Order matters: titles first, because the other two tables depend on it
titles.to_sql("titles", engine, if_exists="append", index=False)
genres.to_sql("title_genres", engine, if_exists="append", index=False)
countries.to_sql("title_countries", engine, if_exists="append", index=False)

print("Data loaded.")
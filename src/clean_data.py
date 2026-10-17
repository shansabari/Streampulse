import pandas as pd

df = pd.read_csv("data/raw/netflix_titles.csv")

# 1. Fill missing values
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")

# 2. Fix dates and add a decade column
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["decade"] = (df["release_year"] // 10) * 10

# 3. Split duration ("90 min" or "2 Seasons") into number + unit
df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)
df["duration_unit"] = df["duration"].str.extract(r"([A-Za-z]+)")

# 4. Split multi-value columns into one row per value
genres = (df[["show_id", "listed_in"]]
          .assign(genre=df["listed_in"].str.split(","))
          .explode("genre"))
genres["genre"] = genres["genre"].str.strip()
genres = genres[["show_id", "genre"]].drop_duplicates()

countries = (df[["show_id", "country"]]
             .assign(country=df["country"].str.split(","))
             .explode("country"))
countries["country"] = countries["country"].str.strip()
countries = countries[countries["country"] != ""][["show_id", "country"]].drop_duplicates()

# 5. Select the columns for the main table
titles = df[["show_id", "type", "title", "release_year", "decade",
             "date_added", "rating", "duration_value", "duration_unit"]]

# 6. Save
titles.to_csv("data/processed/titles.csv", index=False)
genres.to_csv("data/processed/title_genres.csv", index=False)
countries.to_csv("data/processed/title_countries.csv", index=False)

print("titles:", len(titles), "| genres:", len(genres), "| countries:", len(countries))
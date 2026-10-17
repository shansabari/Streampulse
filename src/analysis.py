import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db import get_engine

engine = get_engine()
os.makedirs("outputs/charts", exist_ok=True)
sns.set_theme(style="whitegrid")

genre_q = """
SELECT t.decade, g.genre, COUNT(*) AS title_count
FROM titles t
JOIN title_genres g ON g.show_id = t.show_id
WHERE t.decade >= 1990
GROUP BY t.decade, g.genre
"""
gdf = pd.read_sql(genre_q, engine)
top_genres = gdf.groupby("genre")["title_count"].sum().nlargest(8).index
gdf_top = gdf[gdf["genre"].isin(top_genres)]

plt.figure(figsize=(11, 6))
sns.lineplot(data=gdf_top, x="decade", y="title_count", hue="genre", marker="o")
plt.title("Netflix Catalog: Top Genres by Release Decade")
plt.xlabel("Release decade")
plt.ylabel("Number of titles")
plt.xticks(sorted(gdf_top["decade"].unique()))
plt.savefig("outputs/charts/genre_by_decade.png", dpi=150, bbox_inches="tight")
plt.close()

ratio_q = """
SELECT release_year, type, COUNT(*) AS n
FROM titles
WHERE release_year >= 2000
GROUP BY release_year, type
"""
rdf = pd.read_sql(ratio_q, engine)
pivot = rdf.pivot(index="release_year", columns="type", values="n").fillna(0)
pivot["tv_share"] = pivot["TV Show"] / (pivot["TV Show"] + pivot["Movie"])

plt.figure(figsize=(10, 5))
sns.lineplot(x=pivot.index, y=pivot["tv_share"], marker="o")
plt.title("TV Show Share of Titles by Release Year")
plt.xlabel("Release year")
plt.ylabel("TV show share")
plt.savefig("outputs/charts/tv_vs_movie.png", dpi=150, bbox_inches="tight")
plt.close()


pivot_g = gdf_top.pivot(index="decade", columns="genre", values="title_count").fillna(0)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_g.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Genre Correlation Across Decades")
plt.savefig("outputs/charts/genre_corr.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts saved to outputs/charts/")
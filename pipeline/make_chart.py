import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean/gdp_pc_relative_to_usa.csv", index_col=0)
df.columns = df.columns.astype(int)

benchmarks = ["USA", "ESP", "KOR"]

fig, ax = plt.subplots(figsize=(11, 6))
for country in df.index:
    if country in benchmarks:
        ax.plot(df.columns, df.loc[country], linestyle="--", linewidth=2.5, label=country)
    else:
        ax.plot(df.columns, df.loc[country], linewidth=1, alpha=0.8, label=country)

ax.set_title("GDP per capita (PPP) as % of US level")
ax.set_xlabel("Year")
ax.set_ylabel("% of US income")
ax.legend(ncol=4, fontsize=8)
ax.grid(alpha=0.3)

fig.savefig("charts/relative_income.png", dpi=150, bbox_inches="tight")
plt.show()
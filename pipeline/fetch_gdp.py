import wbgapi as wb

latam = ["ARG", "BOL", "BRA", "CHL", "COL", "CRI", "DOM", "ECU",
         "GTM", "HND", "MEX", "PAN", "PER", "PRY", "SLV", "URY"]
benchmarks = ["USA", "ESP", "KOR"]

df = wb.data.DataFrame(
    "NY.GDP.PCAP.PP.KD",
    economy=latam + benchmarks,
    time=range(1990, 2025),
)
df.columns = [int(c.replace("YR", "")) for c in df.columns]

# Income as a share of the US level
relative = df.div(df.loc["USA"]) * 100

relative.to_csv("data/clean/gdp_pc_relative_to_usa.csv")
print(relative[[1990, 2000, 2010, 2023]].round(1))
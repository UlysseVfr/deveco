from pathlib import Path
import wbgapi as wb

LATAM = ["ARG", "BOL", "BRA", "CHL", "COL", "CRI", "DOM", "ECU",
         "GTM", "HND", "MEX", "PAN", "PER", "PRY", "SLV", "URY"]
BENCHMARKS = ["USA", "ESP", "KOR"]
OUTPUT = Path("data/clean/gdp_pc_relative_to_usa.csv")


def fetch_gdp_per_capita():
    """Download GDP per capita (PPP, constant) from the World Bank."""
    df = wb.data.DataFrame(
        "NY.GDP.PCAP.PP.KD",
        economy=LATAM + BENCHMARKS,
        time=range(1990, 2025),
    )
    # Columns come as "YR1990", "YR1991"... so we turn them into integers
    df.columns = [int(c.replace("YR", "")) for c in df.columns]
    return df


def relative_to_usa(df):
    """Express each country's income as a % of the US level."""
    return df.div(df.loc["USA"]) * 100


if __name__ == "__main__":
    df = fetch_gdp_per_capita()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv("data/clean/gdp_pc_ppp.csv")
    relative = relative_to_usa(df)
    relative.to_csv(OUTPUT)
    print(relative[[1990, 2000, 2010, 2023]].round(1))
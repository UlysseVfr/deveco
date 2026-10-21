import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

START, END = 1990, 2023
BENCHMARKS = ["USA", "ESP", "KOR"]


def compute_growth(df, start, end):
    """Average annual growth (%) between two years, from income levels."""
    return (np.log(df[end]) - np.log(df[start])) / (end - start) * 100


def run_beta_regression(df, start, end):
    """Regress average growth on log of initial income."""
    data = pd.DataFrame({
        "log_initial_income": np.log(df[start]),
        "growth": compute_growth(df, start, end),
    }).dropna()
    X = sm.add_constant(data["log_initial_income"])
    model = sm.OLS(data["growth"], X).fit()
    return data, model


if __name__ == "__main__":
    df = pd.read_csv("data/clean/gdp_pc_ppp.csv", index_col=0)
    df.columns = df.columns.astype(int)
    latam = df.drop(index=BENCHMARKS)  # test convergence within Latin America

    data, model = run_beta_regression(latam, START, END)
    print(model.summary())

    # Scatter plot with the regression line
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(data["log_initial_income"], data["growth"])
    for country, row in data.iterrows():
        ax.annotate(country, (row["log_initial_income"], row["growth"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=9)

    x_line = np.linspace(data["log_initial_income"].min(),
                         data["log_initial_income"].max(), 50)
    y_line = model.params["const"] + model.params["log_initial_income"] * x_line
    ax.plot(x_line, y_line, color="red", linestyle="--")

    ax.set_title(f"Beta convergence in Latin America, {START}-{END}")
    ax.set_xlabel(f"Log of GDP per capita in {START} (PPP)")
    ax.set_ylabel("Average annual growth (%)")
    ax.grid(alpha=0.3)
    fig.savefig("charts/beta_convergence.png", dpi=150, bbox_inches="tight")
    plt.show()
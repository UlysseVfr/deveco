import pandas as pd
from pipeline.convergence import compute_growth, run_beta_regression


def make_data():
    # Poor country grows 5%/year, rich country grows 1%/year, over 10 years
    return pd.DataFrame(
        {2000: [1000.0, 2000.0, 4000.0], 2010: [1628.9, 2208.0, 4417.0]},
        index=["POOR", "MID", "RICH"],
    )


def test_compute_growth_is_correct():
    df = pd.DataFrame({2000: [100.0], 2010: [200.0]}, index=["X"])
    growth = compute_growth(df, 2000, 2010)
    # Doubling in 10 years = ln(2)/10 = 6.93% per year
    assert abs(growth["X"] - 6.93) < 0.01


def test_regression_detects_convergence():
    _, model = run_beta_regression(make_data(), 2000, 2010)
    assert model.params["log_initial_income"] < 0
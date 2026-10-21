import pandas as pd

DATA = "data/clean/gdp_pc_relative_to_usa.csv"


def load():
    return pd.read_csv(DATA, index_col=0)


def test_all_economies_present():
    df = load()
    assert len(df) == 19
    for code in ["USA", "ESP", "KOR", "CHL", "BRA", "MEX"]:
        assert code in df.index


def test_values_are_positive():
    df = load()
    assert (df.stack() > 0).all()


def test_usa_is_100_percent():
    df = load()
    assert (df.loc["USA"].dropna() == 100).all()
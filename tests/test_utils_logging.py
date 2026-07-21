from emmessence.utils_logging import shorten_path
from emmessence.utils_logging import pyo_var_to_csv

import pytest

import pandas as pd
import pandas.testing as pdt
import pyomo.environ as pyo




@pytest.mark.parametrize(
    "longPath, expectedShortenedPath",
    [
        (r"C:\\Users\\idm\\Desktop\\OpenSourceModel\\data", ".../OpenSourceModel/data"),
        (r"C:\Users\idm\Desktop\OpenSourceModel\data", ".../OpenSourceModel/data"),
        (r"C:/Users/idm/Desktop/OpenSourceModel/data", ".../OpenSourceModel/data"),
        (r"C:\\\\\Users\\\idm\\\\Desktop/OpenSourceModel///data", ".../OpenSourceModel/data"),
    ]
)
def test_shorten_path(longPath, expectedShortenedPath):
    assert shorten_path(longPath) == expectedShortenedPath


def test_pyo_var_to_csv_2d_ok(tmp_path):
    m = pyo.ConcreteModel()
    m.I = pyo.Set(initialize=["a", "b"])
    m.J = pyo.Set(initialize=[1, 2])
    m.x = pyo.Var(m.I, m.J)
    m.x["a", 1] = 10
    m.x["a", 2] = 20
    m.x["b", 1] = 30
    m.x["b", 2] = 40
    pyo_var_to_csv(m.x, tmp_path, value_col="production")
    df = pd.read_csv(tmp_path / "x.csv")
    expected = pd.DataFrame({
        "I": ["a", "a", "b", "b"],
        "J": [1, 2, 1, 2],
        "production": [10, 20, 30, 40],
    })
    pdt.assert_frame_equal(df, expected)


def test_pyo_var_to_csv_file_created(tmp_path):
    m = pyo.ConcreteModel()
    m.I = pyo.Set(initialize=[1])
    m.x = pyo.Var(m.I, initialize={1: 42})
    pyo_var_to_csv(m.x, tmp_path)
    assert (tmp_path / "x.csv").exists()

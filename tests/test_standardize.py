
import pandas as pd

from src.divar_auto_data.transformation.standardize import (
    normalize_digits,
    parse_integer,
    parse_production_year,
    select_production_year,
    standardize_dataframe
)


def test_normalize_persian_digits():
    assert normalize_digits("۱۲۳۴۵") == "12345"


def test_parse_price():
    assert parse_integer("۱,۶۱۰,۰۰۰,۰۰۰ تومان") == 1610000000


def test_parse_mileage():
    assert parse_integer("۱۳۰۰۰۰") == 130000


def test_parse_invalid_integer():
    assert pd.isna(parse_integer("توافقی"))


def test_parse_production_year():
    solar, gregorian = parse_production_year("۱۳۹۵ - ۲۰۱۶")

    assert solar == 1395
    assert gregorian == 2016


def test_parse_invalid_production_year():
    solar, gregorian = parse_production_year("نامشخص")

    assert pd.isna(solar)
    assert pd.isna(gregorian)


def test_standardize_dataframe():
    df = pd.DataFrame({
        "price": ["۱,۶۱۰,۰۰۰,۰۰۰ تومان"],
        "mileage": ["۱۳۰۰۰۰"],
        "production_year": ["۱۳۹۵ - ۲۰۱۶"],
        "origin": ["domestic"]
    })

    result = standardize_dataframe(df)

    assert result.loc[0, "price"] == 1610000000
    assert result.loc[0, "mileage"] == 130000
    assert result.loc[0, "production_year"] == 1395
    assert df.loc[0, "price"] == "۱,۶۱۰,۰۰۰,۰۰۰ تومان"

def test_parse_gregorian_only_year():
    solar, gregorian = parse_production_year("۲۰۲۴")

    assert pd.isna(solar)
    assert gregorian == 2024


def test_parse_solar_only_year():
    solar, gregorian = parse_production_year("۱۳۹۵")

    assert solar == 1395
    assert pd.isna(gregorian)


def test_classify_price():
    from src.divar_auto_data.transformation.standardize import classify_price

    assert classify_price(550_000_000) == "normal"
    assert classify_price(10_000_000) == "needs_review"
    assert classify_price(pd.NA) == "missing"

def test_select_domestic_year():
    assert select_production_year(
        "۱۳۹۵ - ۲۰۱۶", "domestic"
    ) == 1395


def test_select_assembly_year():
    assert select_production_year(
        "۱۳۹۵ - ۲۰۱۶", "assembly"
    ) == 1395


def test_select_foreign_year():
    assert select_production_year(
        "۱۳۹۵ - ۲۰۱۶", "foreign"
    ) == 2016


def test_foreign_with_only_solar_year():
    assert pd.isna(
        select_production_year("۱۳۹۵", "foreign")
    )


def test_domestic_with_only_gregorian_year():
    assert pd.isna(
        select_production_year("۲۰۱۶", "domestic")
    )
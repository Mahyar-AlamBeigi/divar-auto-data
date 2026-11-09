
import re
import pandas as pd


PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"

DIGIT_TRANSLATION = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ENGLISH_DIGITS + ENGLISH_DIGITS
)


def normalize_digits(value):
    if pd.isna(value):
        return None

    return str(value).translate(DIGIT_TRANSLATION)


def parse_integer(value):
    if pd.isna(value):
        return pd.NA

    value = normalize_digits(value)
    digits = re.sub(r"[^\d]", "", value)

    if not digits:
        return pd.NA

    return int(digits)


def parse_production_year(value):
    if pd.isna(value):
        return pd.NA, pd.NA

    value = normalize_digits(value)
    years = re.findall(r"\d{4}", value)

    if len(years) == 2:
        return int(years[0]), int(years[1])

    if len(years) == 1:
        year = int(years[0])

        if 1300 <= year <= 1499:
            return year, pd.NA

        if 1900 <= year <= 2100:
            return pd.NA, year

    return pd.NA, pd.NA

def select_production_year(value, origin):
    solar_year, gregorian_year = parse_production_year(value)

    if origin in {"domestic", "assembly"}:
        return solar_year

    if origin == "foreign":
        return gregorian_year

    return pd.NA

def standardize_dataframe(df):
    df = df.copy()

    df["price"] = df["price"].apply(
        parse_integer
    ).astype("Int64")

    df["mileage"] = df["mileage"].apply(
        parse_integer
    ).astype("Int64")

    df["production_year"] = pd.array(
        [
            select_production_year(year, origin)
            for year, origin in zip(
                df["production_year"],
                df["origin"]
            )
        ],
        dtype="Int64"
    )

    df["price_status"] = df["price"].apply(classify_price)

    return df

def classify_price(price):
    if pd.isna(price):
        return "missing"

    if price < 100_000_000:
        return "needs_review"

    return "normal"
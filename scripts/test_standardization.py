from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.divar_auto_data.transformation.standardize import (
    standardize_dataframe
)

DATA_ROOT = PROJECT_ROOT / "data" / "raw" / "listings"

files = list(DATA_ROOT.rglob("data.csv"))

frames = []

for file in files:
    df = pd.read_csv(file, dtype={"token": str})
    frames.append(df)

raw_df = pd.concat(frames, ignore_index=True)

standardized_df = standardize_dataframe(raw_df)

print("Raw data types:")
print(raw_df[["price", "mileage", "production_year"]].dtypes)

print("\nStandardized data types:")
print(standardized_df[
    ["price", "mileage", "production_year"]
].dtypes)
print("\nStandardized samples:")
print(standardized_df[
    ["origin", "brand", "model", "price", "mileage", "production_year"]
].head(10))

print("\nMissing values after transformation:")
print(standardized_df[
    ["price", "mileage", "production_year"]
].isna().sum())

print("\nOriginal data unchanged:")
print(raw_df["price"].iloc[0])

print("\n--- INVALID PRODUCTION YEARS ---")

invalid_years = raw_df[
    standardized_df["production_year"].isna()
]

print(invalid_years[
    ["token", "title", "production_year"]
].head(20).to_string(index=False))


print("\n--- LOWEST PRICES ---")

print(
    standardized_df[
        ["token", "title", "price"]
    ]
    .sort_values("price")
    .head(15)
    .to_string(index=False)
)
print("\n--- PRICE QUALITY REPORT ---")

print(
    standardized_df["price_status"]
    .value_counts(dropna=False)
)

print("\n--- PRICES NEEDING REVIEW ---")

print(
    standardized_df.loc[
        standardized_df["price_status"] == "needs_review",
        ["token", "title", "price", "price_status"]
    ]
    .sort_values("price")
    .to_string(index=False)
)
print("\n--- PRODUCTION YEAR BY ORIGIN ---")

for origin, group in standardized_df.groupby("origin"):
    print(f"\nOrigin: {origin}")
    print("Total records:", len(group))
    print("Missing years:", group["production_year"].isna().sum())
    print("Sample years:")
    print(group["production_year"].dropna().head(10).tolist())

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data" / "raw" / "listings"


def load_all_data():
    files = list(DATA_ROOT.rglob("data.csv"))

    if not files:
        raise FileNotFoundError("No CSV files found.")

    frames = []

    for file in files:
        df = pd.read_csv(file, dtype={"token": str})
        df["source_file"] = str(file.relative_to(DATA_ROOT))
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def run_audit():
    df = load_all_data()

    print("=" * 50)
    print("DATA QUALITY AUDIT")
    print("=" * 50)

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": (df.isna().mean() * 100).round(2)
    })
    print(missing.sort_values("missing_percent", ascending=False))

    print("\nDuplicate tokens:")
    print(df["token"].duplicated().sum())

    print("\nUnique values in categorical columns:")

    for col in ["origin", "brand", "model", "color", "gearbox"]:
        if col in df.columns:
            print(f"\n{col}: {df[col].nunique()} unique values")
            print(df[col].value_counts().head(10))

    print("\nNumeric statistics:")
    print(df.describe(include="all").T)


    print(df[["price", "mileage", "production_year"]].dtypes)

    print("\nOrigin distribution:")
    print(df["origin"].value_counts(dropna=False))

    print("\nToken validation:")
    print("Total:", len(df))
    print("Unique:", df["token"].nunique())
    print("Duplicates:", df["token"].duplicated().sum())

    print("\n--- RAW VALUE SAMPLES ---")

    for col in ["price", "mileage", "production_year"]:
        print(f"\n{col}:")
        print(df[col].dropna().head(10).tolist())

if __name__ == "__main__":
    run_audit()

from pathlib import Path
import pandas as pd


def save_processed_data(df, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = output_path.with_name(output_path.name + ".tmp")

    df.to_csv(temp_path, index=False, encoding="utf-8-sig")
    temp_path.replace(output_path)

    print(f"Processed data saved: {output_path}")
    print(f"Total records: {len(df)}")
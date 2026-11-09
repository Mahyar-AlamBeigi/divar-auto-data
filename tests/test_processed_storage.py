import pandas as pd

from src.divar_auto_data.storage.processed_storage import save_processed_data


def test_save_processed_data(tmp_path):
    df = pd.DataFrame({
        "token": ["abc123", "def456"],
        "price": [500000000, 700000000]
    })

    output_path = tmp_path / "processed" / "listings.csv"

    save_processed_data(df, output_path)

    assert output_path.exists()

    saved_df = pd.read_csv(output_path, dtype={"token": str})

    assert len(saved_df) == 2
    assert saved_df["token"].tolist() == ["abc123", "def456"]
    assert saved_df["price"].tolist() == [500000000, 700000000]
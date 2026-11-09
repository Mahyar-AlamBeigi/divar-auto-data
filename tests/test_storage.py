
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd

from src.divar_auto_data.storage.csv_storage import save_posts


def test_save_posts():

    with TemporaryDirectory() as temp_dir:

        test_path = Path(temp_dir) / "cars.csv"

        old_data = pd.DataFrame([
            {"token": "A", "title": "Old Car A", "price": 500},
            {"token": "B", "title": "Car B", "price": 600}
        ])

        old_data.to_csv(
            test_path,
            index=False
        )

        new_data = [
            {"token": "A", "title": "Updated Car A", "price": 450},
            {"token": "C", "title": "New Car C", "price": 700}
        ]

        with patch(
            "src.divar_auto_data.storage.csv_storage.DATA_PATH",
            test_path
        ):

            save_posts(new_data)

        result = pd.read_csv(test_path)

        assert len(result) == 3

        car_a = result[result["token"] == "A"].iloc[0]

        assert car_a["title"] == "Updated Car A"
        assert car_a["price"] == 450

        assert "B" in result["token"].values
        assert "C" in result["token"].values

        print("Storage Upsert test passed!")


if __name__ == "__main__":
    test_save_posts()

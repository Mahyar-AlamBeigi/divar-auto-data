
import pandas as pd

from src.divar_auto_data.storage.partitioned_csv_storage import (
    save_partitioned_posts
)


def test_insert_new_records(tmp_path):

    posts = [
        {
            "token": "A",
            "origin": "domestic",
            "brand": "پژو",
            "model": "206",
            "variant": "تیپ 5",
            "price": 100
        },
        {
            "token": "B",
            "origin": "foreign",
            "brand": "Toyota",
            "model": "Corolla",
            "variant": "Hybrid",
            "price": 200
        }
    ]

    save_partitioned_posts(posts, tmp_path)

    domestic_file = (
        tmp_path / "domestic" / "پژو"
        / "206" / "تیپ 5" / "data.csv"
    )

    foreign_file = (
        tmp_path / "foreign" / "Toyota"
        / "Corolla" / "data.csv"
    )

    assert domestic_file.exists()
    assert foreign_file.exists()

    index = pd.read_csv(tmp_path / "token_index.csv")

    assert len(index) == 2


def test_upsert_existing_record(tmp_path):

    first_record = {
        "token": "A",
        "origin": "domestic",
        "brand": "پژو",
        "model": "206",
        "variant": "تیپ 5",
        "price": 100
    }

    updated_record = {
        **first_record,
        "price": 150
    }

    save_partitioned_posts([first_record], tmp_path)
    save_partitioned_posts([updated_record], tmp_path)

    file_path = (
        tmp_path / "domestic" / "پژو"
        / "206" / "تیپ 5" / "data.csv"
    )

    df = pd.read_csv(file_path)

    assert len(df) == 1
    assert df.iloc[0]["price"] == 150


def test_move_record_after_reclassification(tmp_path):

    original_record = {
        "token": "A",
        "origin": "domestic",
        "brand": "پژو",
        "model": "206",
        "variant": "تیپ 5",
        "price": 100
    }

    updated_record = {
        "token": "A",
        "origin": "assembly",
        "brand": "پژو",
        "model": "206",
        "variant": "تیپ 5",
        "price": 150
    }

    save_partitioned_posts([original_record], tmp_path)
    save_partitioned_posts([updated_record], tmp_path)

    old_file = (
        tmp_path / "domestic" / "پژو"
        / "206" / "تیپ 5" / "data.csv"
    )

    new_file = (
        tmp_path / "assembly" / "پژو"
        / "206" / "تیپ 5" / "data.csv"
    )

    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)

    assert len(old_df) == 0
    assert len(new_df) == 1
    assert new_df.iloc[0]["price"] == 150

    index = pd.read_csv(tmp_path / "token_index.csv")

    assert len(index) == 1
    assert index.iloc[0]["file_path"] == (
        "assembly/پژو/206/تیپ 5/data.csv"
    )

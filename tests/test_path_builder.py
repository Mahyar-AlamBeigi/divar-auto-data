
from src.divar_auto_data.storage.path_builder import (
    build_storage_path
)


def test_domestic_path(tmp_path):

    record = {
        "origin": "domestic",
        "brand": "پژو",
        "model": "206",
        "variant": "تیپ 5"
    }

    path = build_storage_path(record, tmp_path)

    assert path == (
        tmp_path / "domestic" / "پژو" / "206"
        / "تیپ 5" / "data.csv"
    )


def test_assembly_nested_variant_path(tmp_path):

    record = {
        "origin": "assembly",
        "brand": "سمند",
        "model": "سورن",
        "variant": "پلاس / XU7P بنزینی"
    }

    path = build_storage_path(record, tmp_path)

    assert path == (
        tmp_path / "assembly" / "سمند" / "سورن"
        / "پلاس" / "XU7P بنزینی" / "data.csv"
    )


def test_foreign_path_ignores_variant(tmp_path):

    record = {
        "origin": "foreign",
        "brand": "Toyota",
        "model": "Corolla",
        "variant": "Hybrid / Elite"
    }

    path = build_storage_path(record, tmp_path)

    assert path == (
        tmp_path / "foreign" / "Toyota"
        / "Corolla" / "data.csv"
    )


def test_unclassified_missing_brand(tmp_path):

    record = {
        "origin": "domestic",
        "brand": None,
        "model": "206",
        "variant": "تیپ 5"
    }

    path = build_storage_path(record, tmp_path)

    assert path == tmp_path / "unclassified.csv"


def test_unclassified_invalid_origin(tmp_path):

    record = {
        "origin": "unknown",
        "brand": "پژو",
        "model": "206",
        "variant": "تیپ 5"
    }

    path = build_storage_path(record, tmp_path)

    assert path == tmp_path / "unclassified.csv"


from pathlib import Path
import re


VALID_ORIGINS = {
    "domestic",
    "assembly",
    "foreign"
}


def safe_path_segment(value):
    """
    Convert a breadcrumb value into a safe folder name.
    """

    value = str(value).strip()

    # Remove Windows-invalid characters
    value = re.sub(r'[<>:"/\\|?*]', "_", value)

    # Remove trailing spaces and dots
    value = value.strip(" .")

    # Avoid empty names and Windows reserved names
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10))
    }

    if not value or value.upper() in reserved_names:
        return "_unknown"

    return value


def build_storage_path(record, data_root):
    """
    Build the destination CSV path for a vehicle listing.
    """

    origin = record.get("origin")
    brand = record.get("brand")
    model = record.get("model")
    variant = record.get("variant")

    data_root = Path(data_root)

    # Unknown origin or incomplete vehicle classification
    if origin not in VALID_ORIGINS or not brand or not model:
        return data_root / "unclassified.csv"

    path = (
        data_root
        / origin
        / safe_path_segment(brand)
        / safe_path_segment(model)
    )

    # Imported vehicles are grouped only by brand and model
    if origin in {"domestic", "assembly"} and variant:

        variant_parts = [
            part.strip()
            for part in variant.split("/")
            if part.strip()
        ]

        for part in variant_parts:
            path = path / safe_path_segment(part)

    return path / "data.csv"

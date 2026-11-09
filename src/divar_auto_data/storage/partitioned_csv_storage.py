
from pathlib import Path

import pandas as pd

from src.divar_auto_data.storage.path_builder import (
    build_storage_path
)


def _read_csv(path):
    """Read a CSV while preserving token as a string."""
    return pd.read_csv(path, dtype={"token": str})


def _write_csv_atomic(df, path):
    """Write to a temporary file before replacing the destination."""
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_name(path.name + ".tmp")

    df.to_csv(
        temp_path,
        index=False,
        encoding="utf-8-sig"
    )

    temp_path.replace(path)


def save_partitioned_posts(posts, data_root):
    """
    Save vehicle listings into separate CSV files.

    Features:
    - Partition records by origin, brand, model and variant.
    - Upsert records using token.
    - Maintain a global token index.
    - Move records when their classification changes.
    """

    if not posts:
        print("No posts to save.")
        return

    data_root = Path(data_root)
    data_root.mkdir(parents=True, exist_ok=True)

    index_path = data_root / "token_index.csv"

    # Validate and keep the latest incoming record per token
    incoming = {}

    for post in posts:
        token = post.get("token")

        if token is None or not str(token).strip():
            raise ValueError("Every post must have a valid token.")

        record = dict(post)
        record["token"] = str(token)

        incoming[record["token"]] = record

    # Load the global token index
    if index_path.exists():
        index_df = _read_csv(index_path)

        if not {"token", "file_path"}.issubset(index_df.columns):
            raise ValueError("Invalid token index structure.")

        token_index = dict(
            zip(index_df["token"], index_df["file_path"])
        )
    else:
        token_index = {}

    # Determine destination paths
    destinations = {}
    records_by_path = {}

    for token, record in incoming.items():

        destination = build_storage_path(
            record,
            data_root
        )

        relative_path = destination.relative_to(
            data_root
        ).as_posix()

        destinations[token] = relative_path

        records_by_path.setdefault(
            relative_path, []
        ).append(record)

    # Find records that need to move
    tokens_to_remove = {}

    for token, new_path in destinations.items():

        old_path = token_index.get(token)

        if old_path and old_path != new_path:

            tokens_to_remove.setdefault(
                old_path, set()
            ).add(token)

    # Remove moved records from their old CSV files
    for old_relative_path, tokens in tokens_to_remove.items():

        old_file = data_root / old_relative_path

        if not old_file.exists():
            continue

        old_df = _read_csv(old_file)

        old_df = old_df[
            ~old_df["token"].astype(str).isin(tokens)
        ]

        _write_csv_atomic(old_df, old_file)

    # Upsert records into their destination CSV files
    for relative_path, records in records_by_path.items():

        destination = data_root / relative_path

        new_df = pd.DataFrame(records)

        if destination.exists():

            old_df = _read_csv(destination)

            combined_df = pd.concat(
                [old_df, new_df],
                ignore_index=True
            )

        else:
            combined_df = new_df

        combined_df = combined_df.drop_duplicates(
            subset=["token"],
            keep="last"
        )

        _write_csv_atomic(
            combined_df,
            destination
        )

    # Update the global token index
    for token, relative_path in destinations.items():
        token_index[token] = relative_path

    index_df = pd.DataFrame(
        [
            {
                "token": token,
                "file_path": relative_path
            }
            for token, relative_path in token_index.items()
        ]
    )

    _write_csv_atomic(index_df, index_path)

    print(f"Incoming unique records: {len(incoming)}")
    print(f"Updated token index: {len(token_index)}")
    print(f"Moved records: {sum(len(v) for v in tokens_to_remove.values())}")
    print(f"Storage directory: {data_root}")

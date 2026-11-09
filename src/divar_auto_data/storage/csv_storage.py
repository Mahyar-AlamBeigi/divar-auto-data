
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "cars.csv"


def save_posts(posts):

    if not posts:
        print("No posts to save.")
        return

    new_df = pd.DataFrame(posts)

    if "token" not in new_df.columns:
        raise ValueError("Posts must contain a token column.")

    DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if DATA_PATH.exists():

        old_df = pd.read_csv(DATA_PATH)

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

    combined_df.to_csv(
        DATA_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved {len(new_df)} incoming records.")
    print(f"Total unique records: {len(combined_df)}")
    print(f"Storage path: {DATA_PATH}")

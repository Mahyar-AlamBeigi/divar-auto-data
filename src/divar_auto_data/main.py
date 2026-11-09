import pandas as pd

from src.divar_auto_data.transformation.standardize import standardize_dataframe
from src.divar_auto_data.storage.processed_storage import save_processed_data
from config.settings import (
    MAX_PAGES,
    TARGET_POSTS,
    VEHICLE_ORIGINS,
    build_search_payload
)

from src.divar_auto_data.ingestion.search import get_all_posts
from src.divar_auto_data.ingestion.details import get_all_details
from src.divar_auto_data.storage.partitioned_csv_storage import (
    save_partitioned_posts
)

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_ROOT = PROJECT_ROOT / "data" / "raw" / "listings"

def process_raw_data():
    print("\n" + "=" * 50)
    print("PROCESSING RAW DATA")
    print("=" * 50)

    raw_files = list(DATA_ROOT.rglob("data.csv"))

    if not raw_files:
        print("No raw data files found.")
        return

    dataframes = []

    for file in raw_files:
        df = pd.read_csv(file, dtype={"token": str})

        df["source_file"] = file.relative_to(DATA_ROOT).as_posix()

        dataframes.append(df)

    raw_df = pd.concat(dataframes, ignore_index=True)

    print(f"Raw records loaded: {len(raw_df)}")

    processed_df = standardize_dataframe(raw_df)

    print(f"Processed records: {len(processed_df)}")

    output_path = PROJECT_ROOT / "data" / "processed" / "listings.csv"

    save_processed_data(processed_df, output_path)

def run_pipeline():

    print("=" * 50)
    print("DIVAR AUTO DATA PIPELINE")
    print("=" * 50)

    all_detailed_posts = []

    # Step 1 & 2: Collect posts and details for each origin
    for origin, origin_name in VEHICLE_ORIGINS.items():

        print("\n" + "-" * 50)
        print(f"Processing origin: {origin_name} ({origin})")
        print("-" * 50)

        payload = build_search_payload(origin)

        posts = get_all_posts(
            first_payload=payload,
            max_pages=MAX_PAGES,
            target_posts=TARGET_POSTS
        )

        print(f"Collected posts: {len(posts)}")

        if not posts:
            print(f"No posts found for {origin}. Skipping...")
            continue

        detailed_posts = get_all_details(
            posts,
            origin=origin
        )

        print(f"Detailed posts: {len(detailed_posts)}")

        all_detailed_posts.extend(detailed_posts)

    # Step 3: Save all collected data
    print("\n" + "=" * 50)
    print("SAVING DATA")
    print("=" * 50)

    print(f"Total detailed posts: {len(all_detailed_posts)}")

    if all_detailed_posts:
        save_partitioned_posts(
            all_detailed_posts,
            DATA_ROOT
        )
    else:
        print("No new detailed posts. Existing raw data will be processed.")

    # Step 4: Process all raw data
    process_raw_data()


    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()

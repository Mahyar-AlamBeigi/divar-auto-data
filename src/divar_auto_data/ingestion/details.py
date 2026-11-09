import time

from src.divar_auto_data.extraction.detail_extractor import extract_details
import requests

from config.settings import POST_URL, HEADERS


def get_post_details(token):

    url = POST_URL.format(token)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        else:
            print(
                f"Post Error {response.status_code}: {token}"
            )

            return None

    except requests.RequestException as e:

        print(
            f"Request error for {token}:",
            e
        )

        return None


def get_all_details(posts, origin=None):
    results = []
    total = len(posts)

    for i, post in enumerate(posts, start=1):
        token = post["token"]
        print(f"[{i}/{total}] {token}")

        data = get_post_details(token)

        if data is None:
            continue

        details = extract_details(data)

        row = {
            "token": token,
            "origin": origin,
            "title": post.get("title"),
            "price": post.get("price_search"),
            "location": post.get("location"),
            "image_count": post.get("image_count"),

            "brand": details["brand"],
            "model": details["model"],
            "variant": details["variant"],
            "breadcrumb": details["breadcrumb"],

            "mileage": details["mileage"],
            "production_year": details["production_year"],
            "color": details["color"],
            "engine": details["engine"],
            "chassis": details["chassis"],
            "body": details["body"],
            "gearbox": details["gearbox"]
        }

        results.append(row)
        time.sleep(0.3)

    return results



# =========================================================
# MAIN
# =========================================================
from copy import deepcopy
import time
from src.divar_auto_data.extraction.post_extractor import extract_posts
import requests

from config.settings import SEARCH_URL, HEADERS


def get_page(payload):

    try:
        response = requests.post(
            SEARCH_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        print("Search Error:", response.status_code)
        print(response.text[:500])

        return None

    except requests.RequestException as e:
        print("Request error:", e)
        return None


def get_all_posts(
    first_payload,
    max_pages=500,
    target_posts=10000
):

    all_posts = []
    payload = deepcopy(first_payload)

    seen_tokens = set()

    for page in range(max_pages):

        print(f"Getting page: {page + 1}")

        # دریافت صفحه
        data = get_page(payload)

        if data is None:
            print("Could not get page.")
            break

        # استخراج آگهی‌ها
        posts = extract_posts(data)

        print("Posts in page:", len(posts))

        # حذف آگهی‌های تکراری
        new_posts = []

        for post in posts:

            token = post["token"]

            if token not in seen_tokens:
                seen_tokens.add(token)
                new_posts.append(post)

        all_posts.extend(new_posts)

        print("New posts:", len(new_posts))
        print("Total unique posts:", len(all_posts))

        # بررسی تعداد آگهی‌های هدف
        if len(all_posts) >= target_posts:
            print("Target reached!")
            break

        # بررسی صفحه بعد
        pagination = data.get("pagination")

        if not pagination:
            print("Pagination not found.")
            break

        has_next_page = pagination.get("has_next_page", False)

        if not has_next_page:
            print("No more pages.")
            break

        next_pagination = pagination.get("data")

        if not next_pagination:
            print("Next pagination data not found.")
            break

        payload["pagination_data"] = next_pagination

        time.sleep(1)

    return all_posts

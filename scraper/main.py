import requests
import pandas as pd
import time
from copy import deepcopy


# =========================================================
# SETTINGS
# =========================================================

SEARCH_URL = "https://api.divar.ir/v8/postlist/w/search"

POST_URL = "https://api.divar.ir/v8/posts-v2/web/{}"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}


# =========================================================
# SEARCH PAYLOAD
# =========================================================

payload = {

    "city_ids": ["1"],

    "source_view": "FILTER",

    "pagination_data": {
        "@type": "type.googleapis.com/post_list.PaginationData",
        "page": 1,
        "layer_page": 1
    },

    "disable_recommendation": False,

    "map_state": {
        "camera_info": {
            "bbox": {}
        }
    },

    "search_data": {
        "form_data": {
            "data": {

                "brand_model": {
                    "repeated_string": {
                        "value": [
                            "Peugeot 206 5"
                        ]
                    }
                },

                "category": {
                    "str": {
                        "value": "light"
                    }
                }

            }
        }
    }
}


# =========================================================
# GET SEARCH PAGE
# =========================================================

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

        else:

            print(
                "Search Error:",
                response.status_code
            )

            print(
                response.text[:500]
            )

            return None

    except requests.RequestException as e:

        print(
            "Request error:",
            e
        )

        return None


# =========================================================
# EXTRACT POSTS FROM SEARCH
# =========================================================

def extract_posts(data):

    posts = []

    for widget in data.get(
        "list_widgets",
        []
    ):

        if widget.get(
            "widget_type"
        ) != "POST_ROW":

            continue


        post_data = widget.get(
            "data",
            {}
        )


        action = post_data.get(
            "action",
            {}
        )


        action_payload = action.get(
            "payload",
            {}
        )


        token = action_payload.get(
            "token"
        )


        if not token:

            continue


        post = {

            "token": token,

            "title": post_data.get(
                "title"
            ),

            "price_search":
                post_data.get(
                    "middle_description_text"
                ),

            "mileage_search":
                post_data.get(
                    "top_description_text"
                ),

            "location":
                post_data.get(
                    "bottom_description_text"
                ),

            "image_count":
                post_data.get(
                    "image_count"
                )
        }


        posts.append(post)


    return posts


# =========================================================
# GET ALL POSTS
# =========================================================

def get_all_posts(
    first_payload,
    max_pages=500,
    target_posts=10000
):

    all_posts = []

    payload = deepcopy(
        first_payload
    )


    # جلوگیری از duplicate

    seen_tokens = set()


    for page in range(
        max_pages
    ):

        print()
        print("=" * 50)

        print(
            f"Getting page: {page + 1}"
        )

        print("=" * 50)


        # -----------------------------------------
        # GET PAGE
        # -----------------------------------------

        data = get_page(
            payload
        )


        if data is None:

            print(
                "Could not get page."
            )

            break


        # -----------------------------------------
        # EXTRACT POSTS
        # -----------------------------------------

        posts = extract_posts(
            data
        )


        print(
            "Posts in page:",
            len(posts)
        )


        # -----------------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------------

        new_posts = []


        for post in posts:

            token = post["token"]


            if token not in seen_tokens:

                seen_tokens.add(
                    token
                )

                new_posts.append(
                    post
                )


        all_posts.extend(
            new_posts
        )


        print(
            "New posts:",
            len(new_posts)
        )

        print(
            "Total unique posts:",
            len(all_posts)
        )


        # -----------------------------------------
        # TARGET
        # -----------------------------------------

        if len(all_posts) >= target_posts:

            print()
            print(
                "Target reached!"
            )

            break


        # -----------------------------------------
        # PAGINATION
        # -----------------------------------------

        pagination = data.get(
            "pagination"
        )


        if not pagination:

            print(
                "Pagination not found."
            )

            break


        has_next_page = pagination.get(
            "has_next_page",
            False
        )


        print(
            "Has next page:",
            has_next_page
        )


        if not has_next_page:

            print(
                "No more pages."
            )

            break


        next_pagination = pagination.get(
            "data"
        )


        if not next_pagination:

            print(
                "Next pagination data not found."
            )

            break


        # -----------------------------------------
        # PAGE AFTER
        # -----------------------------------------

        payload["pagination_data"] = (
            next_pagination
        )


        time.sleep(1)


    return all_posts


# =========================================================
# GET ONE POST DETAILS
# =========================================================

def get_post_details(token):

    url = POST_URL.format(
        token
    )


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


# =========================================================
# EXTRACT DETAILS
# =========================================================

def extract_details(data):

    result = {

        "mileage": None,

        "production_year": None,

        "color": None,

        "engine": None,

        "chassis": None,

        "body": None,

        "gearbox": None
    }


    if not data:

        return result


    for section in data.get(
        "sections",
        []
    ):


        for widget in section.get(
            "widgets",
            []
        ):


            widget_type = widget.get(
                "widget_type"
            )


            widget_data = widget.get(
                "data",
                {}
            )


            # =====================================
            # MODEL / YEAR / COLOR / MILEAGE
            # =====================================

            if widget_type == "GROUP_INFO_ROW":


                for item in widget_data.get(
                    "items",
                    []
                ):


                    title = item.get(
                        "title"
                    )


                    value = item.get(
                        "value"
                    )


                    if title == "کارکرد":

                        result["mileage"] = value


                    elif title == "مدل (سال تولید)":

                        result["production_year"] = value


                    elif title == "رنگ":

                        result["color"] = value


            # =====================================
            # ENGINE / CHASSIS / BODY / GEARBOX
            # =====================================

            elif widget_type == "SCORE_ROW":


                title = widget_data.get(
                    "title"
                )


                value = widget_data.get(
                    "descriptive_score"
                )


                if title == "موتور":

                    result["engine"] = value


                elif title == "وضعیت شاسی‌ها":

                    result["chassis"] = value


                elif title == "بدنه":

                    result["body"] = value


                elif title == "گیربکس":

                    result["gearbox"] = value


    return result


# =========================================================
# GET DETAILS OF ALL POSTS
# =========================================================

def get_all_details(posts):

    results = []

    total = len(posts)


    for i, post in enumerate(
        posts,
        start=1
    ):


        token = post["token"]


        print(
            f"[{i}/{total}] {token}"
        )


        # -----------------------------------------
        # GET DETAIL API
        # -----------------------------------------

        data = get_post_details(
            token
        )


        if data is None:

            continue


        # -----------------------------------------
        # EXTRACT DETAILS
        # -----------------------------------------

        details = extract_details(
            data
        )


        # -----------------------------------------
        # CREATE ROW
        # -----------------------------------------

        row = {

            # Search API

            "token":
                token,

            "title":
                post.get(
                    "title"
                ),

            "price":
                post.get(
                    "price_search"
                ),

            "location":
                post.get(
                    "location"
                ),

            "image_count":
                post.get(
                    "image_count"
                ),


            # Detail API

            "mileage":
                details["mileage"],

            "production_year":
                details[
                    "production_year"
                ],

            "color":
                details["color"],

            "engine":
                details["engine"],

            "chassis":
                details["chassis"],

            "body":
                details["body"],

            "gearbox":
                details["gearbox"]
        }


        results.append(
            row
        )


        # -----------------------------------------
        # REQUEST DELAY
        # -----------------------------------------

        time.sleep(
            0.3
        )


    return results


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":


    # ---------------------------------------------
    # STEP 1
    # گرفتن آگهی‌ها و pagination
    # ---------------------------------------------

    posts = get_all_posts(

        payload,

        max_pages=500,

        target_posts=10000
    )


    print()
    print("=" * 60)

    print(
        "SEARCH FINISHED"
    )

    print(
        "Total posts:",
        len(posts)
    )

    print("=" * 60)


    # ---------------------------------------------
    # STEP 2
    # گرفتن جزئیات
    # ---------------------------------------------

    results = get_all_details(
        posts
    )


    print()
    print("=" * 60)

    print(
        "DETAIL EXTRACTION FINISHED"
    )

    print(
        "Total detailed posts:",
        len(results)
    )

    print("=" * 60)


    # ---------------------------------------------
    # STEP 3
    # DataFrame
    # ---------------------------------------------

    df = pd.DataFrame(
        results
    )


    print()
    print(
        df.head()
    )


    print()
    print(
        "Shape:",
        df.shape
    )


    # ---------------------------------------------
    # STEP 4
    # Save
    # ---------------------------------------------

    df.to_csv(
        "divar_206_type5_raw.csv",
        index=False,
        encoding="utf-8-sig"
    )


    print()
    print(
        "Saved:"
    )

    print(
        "divar_206_type5_raw.csv"
    )
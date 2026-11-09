from copy import deepcopy

# API endpoints
SEARCH_URL = "https://api.divar.ir/v8/postlist/w/search"
POST_URL = "https://api.divar.ir/v8/posts-v2/web/{}"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Search configuration
CITY_IDS = ["1"]
CATEGORY = "light"
SOURCE_VIEW = "FILTER"

# Test-mode limits
MAX_PAGES = 1
TARGET_POSTS = 24

# Vehicle origins
VEHICLE_ORIGINS = {
    "domestic": "داخلی",
    "assembly": "مونتاژی",
    "foreign": "وارداتی"
}

# General passenger car search payload
SEARCH_PAYLOAD = {
    "city_ids": CITY_IDS,
    "source_view": SOURCE_VIEW,

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
                "category": {
                    "str": {
                        "value": CATEGORY
                    }
                }
            }
        }
    }
}


def build_search_payload(origin):
    if origin not in VEHICLE_ORIGINS:
        raise ValueError(f"Invalid vehicle origin: {origin}")

    payload = deepcopy(SEARCH_PAYLOAD)

    form_data = payload["search_data"]["form_data"]["data"]

    form_data["brand_model_manufacturer_origin"] = {
        "repeated_string": {
            "value": [origin]
        }
    }

    return payload

from unittest.mock import patch

from src.divar_auto_data.ingestion.search import get_all_posts


def fake_extract_posts(data):
    return data["posts"]


page_1 = {
    "posts": [
        {"token": "A", "title": "Car A"},
        {"token": "B", "title": "Car B"}
    ],
    "pagination": {
        "has_next_page": True,
        "data": {"page": 2}
    }
}

page_2 = {
    "posts": [
        {"token": "B", "title": "Car B"},
        {"token": "C", "title": "Car C"}
    ],
    "pagination": {
        "has_next_page": False
    }
}


@patch(
    "src.divar_auto_data.ingestion.search.extract_posts",
    side_effect=fake_extract_posts
)
@patch(
    "src.divar_auto_data.ingestion.search.get_page",
    side_effect=[page_1, page_2]
)
@patch("src.divar_auto_data.ingestion.search.time.sleep")
def test_get_all_posts(mock_sleep, mock_get_page, mock_extract):

    result = get_all_posts(
        first_payload={"pagination_data": {}},
        target_posts=10
    )

    tokens = [post["token"] for post in result]

    assert tokens == ["A", "B", "C"]
    assert mock_get_page.call_count == 2

    print("Test passed!")


if __name__ == "__main__":
    test_get_all_posts()
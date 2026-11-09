
from unittest.mock import patch

from src.divar_auto_data.ingestion.details import get_all_details


fake_post = {
    "token": "TEST123",
    "title": "پژو 206 تیپ 5",
    "price_search": "500 میلیون",
    "location": "تهران",
    "image_count": 4
}

fake_detail_response = {
    "sections": [
        {
            "widgets": [
                {
                    "widget_type": "GROUP_INFO_ROW",
                    "data": {
                        "items": [
                            {"title": "کارکرد", "value": "100000"},
                            {"title": "مدل (سال تولید)", "value": "1395"},
                            {"title": "رنگ", "value": "سفید"}
                        ]
                    }
                },
                {
                    "widget_type": "SCORE_ROW",
                    "data": {
                        "title": "موتور",
                        "descriptive_score": "سالم"
                    }
                }
            ]
        }
    ]
}


@patch(
    "src.divar_auto_data.ingestion.details.get_post_details",
    return_value=fake_detail_response
)
@patch(
    "src.divar_auto_data.ingestion.details.time.sleep"
)
def test_get_all_details(mock_sleep, mock_api):

    result = get_all_details([fake_post])

    assert len(result) == 1

    assert result[0]["token"] == "TEST123"
    assert result[0]["title"] == "پژو 206 تیپ 5"
    assert result[0]["mileage"] == "100000"
    assert result[0]["production_year"] == "1395"
    assert result[0]["color"] == "سفید"
    assert result[0]["engine"] == "سالم"

    assert mock_api.call_count == 1

    print("Details integration test passed!")


if __name__ == "__main__":
    test_get_all_details()

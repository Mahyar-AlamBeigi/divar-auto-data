
from unittest.mock import patch

from src.divar_auto_data.main import run_pipeline, DATA_ROOT


@patch("src.divar_auto_data.main.save_partitioned_posts")
@patch("src.divar_auto_data.main.get_all_details")
@patch("src.divar_auto_data.main.get_all_posts")
@patch("src.divar_auto_data.main.build_search_payload")
def test_pipeline(
    mock_build_payload,
    mock_get_posts,
    mock_get_details,
    mock_save
):

    mock_build_payload.side_effect = lambda origin: {
        "origin": origin
    }

    mock_get_posts.side_effect = [
        [{"token": "A"}],
        [{"token": "B"}],
        [{"token": "C"}]
    ]

    mock_get_details.side_effect = [
        [{"token": "A", "origin": "domestic"}],
        [{"token": "B", "origin": "assembly"}],
        [{"token": "C", "origin": "foreign"}]
    ]

    run_pipeline()

    assert mock_build_payload.call_count == 3
    assert mock_get_posts.call_count == 3
    assert mock_get_details.call_count == 3
    assert mock_save.call_count == 1

    assert mock_get_details.call_args_list[0].kwargs == {
        "origin": "domestic"
    }

    assert mock_get_details.call_args_list[1].kwargs == {
        "origin": "assembly"
    }

    assert mock_get_details.call_args_list[2].kwargs == {
        "origin": "foreign"
    }

    mock_save.assert_called_once_with(
        [
            {"token": "A", "origin": "domestic"},
            {"token": "B", "origin": "assembly"},
            {"token": "C", "origin": "foreign"}
        ],
        DATA_ROOT
    )


@patch("src.divar_auto_data.main.save_partitioned_posts")
@patch("src.divar_auto_data.main.get_all_details")
@patch("src.divar_auto_data.main.get_all_posts")
def test_empty_posts(
    mock_get_posts,
    mock_get_details,
    mock_save
):

    mock_get_posts.return_value = []

    run_pipeline()

    assert mock_get_posts.call_count == 3
    mock_get_details.assert_not_called()
    mock_save.assert_not_called()


@patch("src.divar_auto_data.main.save_partitioned_posts")
@patch("src.divar_auto_data.main.get_all_details")
@patch("src.divar_auto_data.main.get_all_posts")
def test_empty_details(
    mock_get_posts,
    mock_get_details,
    mock_save
):

    mock_get_posts.side_effect = [
        [{"token": "A"}],
        [{"token": "B"}],
        [{"token": "C"}]
    ]

    mock_get_details.return_value = []

    run_pipeline()

    assert mock_get_details.call_count == 3
    mock_save.assert_not_called()

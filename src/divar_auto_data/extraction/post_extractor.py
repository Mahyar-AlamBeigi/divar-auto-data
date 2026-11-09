
def extract_posts(data):

    posts = []

    for widget in data.get("list_widgets", []):

        if widget.get("widget_type") != "POST_ROW":
            continue

        post_data = widget.get("data", {})
        action = post_data.get("action", {})
        action_payload = action.get("payload", {})

        token = action_payload.get("token")

        if not token:
            continue

        post = {
            "token": token,
            "title": post_data.get("title"),
            "price_search": post_data.get("middle_description_text"),
            "mileage_search": post_data.get("top_description_text"),
            "location": post_data.get("bottom_description_text"),
            "image_count": post_data.get("image_count")
        }

        posts.append(post)

    return posts

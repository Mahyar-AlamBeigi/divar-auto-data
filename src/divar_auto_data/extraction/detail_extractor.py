
def extract_details(data):
    result = {
        "brand": None,
        "model": None,
        "variant": None,
        "breadcrumb": None,
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

    ignored_breadcrumbs = {
        "وسایل نقلیه",
        "خودرو",
        "خودرو سواری و وانت"
    }

    for section in data.get("sections", []):

        if section.get("section_name") == "BREADCRUMB":
            for widget in section.get("widgets", []):
                if widget.get("widget_type") != "BREADCRUMB":
                    continue

                parent_items = widget.get("data", {}).get(
                    "parent_items", []
                )

                parts = [
                    item.get("title")
                    for item in parent_items
                    if item.get("title")
                    and item.get("title") not in ignored_breadcrumbs
                ]

                if parts:
                    result["breadcrumb"] = " / ".join(parts)
                    result["brand"] = parts[0]

                if len(parts) >= 2:
                    result["model"] = parts[1]

                if len(parts) >= 3:
                    result["variant"] = " / ".join(parts[2:])

        for widget in section.get("widgets", []):
            widget_type = widget.get("widget_type")
            widget_data = widget.get("data", {})

            if widget_type == "GROUP_INFO_ROW":
                for item in widget_data.get("items", []):
                    title = item.get("title")
                    value = item.get("value")

                    if title == "کارکرد":
                        result["mileage"] = value
                    elif title == "مدل (سال تولید)":
                        result["production_year"] = value
                    elif title == "رنگ":
                        result["color"] = value

            elif widget_type == "SCORE_ROW":
                title = widget_data.get("title")
                value = widget_data.get("descriptive_score")

                if title == "موتور":
                    result["engine"] = value
                elif title == "وضعیت شاسی‌ها":
                    result["chassis"] = value
                elif title == "بدنه":
                    result["body"] = value
                elif title == "گیربکس":
                    result["gearbox"] = value

    return result

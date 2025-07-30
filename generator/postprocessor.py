def inject_components(md: str, data: dict) -> str:
    for i, url in enumerate(data["image_urls"]):
        md = md.replace(f"{{{{image:{i+1}}}}}", f"![이미지 {i+1}]({url})")

    if "{{map}}" in md:
        md = md.replace("{{map}}", f"<iframe src=\"{data['naver_map_iframe']}\" width=\"100%\" height=\"300px\"></iframe>")
    else:
        md += f"\n\n<iframe src=\"{data['naver_map_iframe']}\" width=\"100%\" height=\"300px\"></iframe>"

    md += f"\n\n[📅 진료 예약하러 가기]({data['reservation_url']})"
    return md

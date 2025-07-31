from main_recursive import generate_blog_article

if __name__ == "__main__":
    input_data = {
        "keyword": "강남역 임플란트",
        "hospital_name": "내이튼치과",
        "address": "서울 강남구 강남대로 396",
        "naver_map_iframe": "https://map.naver.com/p/entry/place/12345678",
        "reservation_url": "https://booking.example.com/clinic",
        "image_urls": [
            "https://example.com/img1.jpg",
            "https://example.com/img2.jpg"
        ],
        "seo_guideline": [
            "제목에 메인 키워드 포함",
            "본문에 키워드 3회 이상 사용",
            "소제목은 H2 태그 사용",
            "내용은 800자 이상",
            "이미지는 최소 2개 포함",
            "지도 또는 위치 정보 포함"
        ]
    }

    result = generate_blog_article(input_data)

    with open("blog_post.md", "w", encoding="utf-8") as f:
        f.write(result)

    print("✅ 블로그 글 생성 완료! → blog_post.md")

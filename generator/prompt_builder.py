def build_prompt(data: dict) -> str:
    image_tags = "\n".join([f"{{{{image:{i+1}}}}}" for i in range(len(data["image_urls"]))])
    seo_rules = "\n- ".join(data["seo_guideline"])

    prompt = f"""
당신은 SEO에 최적화된 블로그 글 작성 전문가이자, 치과의사입니다.

주제: "{data['keyword']}"에 대한 블로그 글을 작성해주세요.

블로그 글의 목적은 검색 엔진 최적화이며, 다음 기준을 반드시 지켜야 합니다:
- {seo_rules}

작성 시 아래와 같은 요소도 포함해주세요:
1. 제목은 키워드를 포함한 H1 형태
2. 소제목(H2)으로 2~4개 단락 구분
3. 아래 이미지 태그가 들어갈 위치에 설명을 작성해주세요:
{image_tags}
4. 마지막에는 병원 위치 안내 및 예약 버튼도 포함해주세요
5. 단, 의료 광고 등 법법에 위반되어서는 안 됩니다.

병원 정보:
- 이름: {data['hospital_name']}
- 주소: {data['address']}
- 지도 링크: {data['naver_map_iframe']}
- 예약 링크: {data['reservation_url']}

출력은 마크다운 형식으로 해주세요.
"""
    return prompt.strip()

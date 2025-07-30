import os
import google.generativeai as genai
from google.generativeai import GenerativeModel

# 환경변수에서 Gemini API 키 불러오기
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def create_prompt(data: dict) -> str:
    image_tags = "\n".join([f"{{{{image:{i+1}}}}}" for i in range(len(data["image_urls"]))])
    seo_rules = "\n- ".join(data["seo_guideline"])

    prompt = f"""
당신은 SEO에 최적화된 블로그 글 작성 전문가이자, 치과의사사입니다.

주제: "{data['keyword']}"에 대한 블로그 글을 작성해주세요.

블로그 글의 목적은 검색 엔진 최적화이며, 다음 기준을 반드시 지켜야 합니다:
- {seo_rules}

작성 시 아래와 같은 요소도 포함해주세요:
1. 제목은 키워드를 포함한 H1 형태
2. 소제목(H2)으로 2~4개 단락 구분
3. 아래 이미지 태그가 들어갈 위치에 설명을 작성해주세요:
{image_tags}
4. 마지막에는 병원 위치 안내 및 예약 버튼도 포함해주세요
5. 단, 의료 광고 등 법령에 위배되는 내용은 포함하지 마세요.

병원 정보:
- 이름: {data['hospital_name']}
- 주소: {data['address']}
- 지도 링크: {data['naver_map_iframe']}
- 예약 링크: {data['reservation_url']}

출력은 마크다운 형식으로 해주세요.
"""
    return prompt.strip()

def generate_with_gemini(prompt: str) -> str:
    model = GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def postprocess_markdown(md: str, data: dict) -> str:
    for i, url in enumerate(data["image_urls"]):
        md = md.replace(f"{{{{image:{i+1}}}}}", f"![이미지 {i+1}]({url})")

    if "{{map}}" in md:
        md = md.replace("{{map}}", f"<iframe src=\"{data['naver_map_iframe']}\" width=\"100%\" height=\"300px\"></iframe>")
    else:
        md += f"\n\n<iframe src=\"{data['naver_map_iframe']}\" width=\"100%\" height=\"300px\"></iframe>"

    md += f"\n\n[📅 진료 예약하러 가기]({data['reservation_url']})"
    return md

def generate_blog_article(data: dict) -> str:
    prompt = create_prompt(data)
    raw_markdown = generate_with_gemini(prompt)
    final_markdown = postprocess_markdown(raw_markdown, data)
    return final_markdown

if __name__ == "__main__":
    # 예시 입력
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

    output_file = "blog_post.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ 블로그 글 생성 완료! → {output_file}")

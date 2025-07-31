import openai
import os
import re
import pandas as pd
from konlpy.tag import Okt
from typing import List, Dict
import json
from datetime import datetime
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class EnhancedRecursiveThinkingChat:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-3.5-turbo",
        system_prompt_file: str = None,
        reference_csv: str = None
    ):
        # API 키 설정
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("환경변수 OPENAI_API_KEY에 키를 설정해주세요.")
        openai.api_key = self.api_key
        self.model = model
        self.conversation_history: List[Dict] = []

        # 형태소 분석기 초기화 및 참조 데이터 로드
        self.morph_analyzer = Okt()
        self.reference_df = None

        # 시스템 프롬프트 불러오기
        if system_prompt_file and os.path.exists(system_prompt_file):
            with open(system_prompt_file, encoding="utf-8") as f:
                system_prompt = f.read().strip()
            # 초기 지침에 글자수, 형태소수, 이미지설명 제외 규칙 포함
            system_prompt += (
                "\n\n추가 지침: 출력물에서 마크다운 이미지 설명(예: ![alt](file.png): 설명) 라인은 글자수 및 형태소 수 계산에서 제외하고, "
                "제목(공백 포함 40±5, 공백 제외 30±5)과 본문(공백 포함 1763±50, 공백 제외 1339±50, 형태소 340±10)을 반드시 맞춰 작성하세요."
            )
            self.conversation_history.append({"role": "system", "content": system_prompt})

        # CSV 데이터 로드 (카테고리-흐름)
        if reference_csv and os.path.exists(reference_csv):
            df = pd.read_csv(reference_csv, encoding='utf-8-sig')
            df.columns = ['category', 'flow'] + list(df.columns[2:])
            self.reference_df = df[['category', 'flow']]

    def _call_api(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        stream: bool = True
    ) -> str:
        try:
            resp = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=stream
            )
            if stream:
                full = ""
                for chunk in resp:
                    content = chunk.choices[0].delta.get('content')
                    if content:
                        full += content
                return full
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"

    def _extract_reference_flow(self, user_input: str) -> str:
        if self.reference_df is None:
            return ""
        nouns = self.morph_analyzer.nouns(user_input)
        matched = self.reference_df[self.reference_df.apply(
            lambda row: any(noun in row['category'] or noun in row['flow'] for noun in nouns), axis=1
        )]
        if matched.empty:
            return ""
        flows = matched['flow'].dropna().tolist()
        return "참고 흐름 (유사한 증상-진료-치료):\n" + "\n".join(f"- {f}" for f in flows)

    def _strip_image_lines(self, text: str) -> str:
        # 이미지 설명 라인 제거 (!\[...\]\(...\): ...)
        lines = text.split("\n")
        filtered = [ln for ln in lines if not re.match(r"^!\[.*?\]\(.*?\):.*", ln)]
        return "\n".join(filtered)

    def think_and_respond(self, user_input: str) -> Dict:
        messages = list(self.conversation_history)
        # 참조 흐름
        ref = self._extract_reference_flow(user_input)
        if ref:
            messages.append({"role": "system", "content": ref})
        # 사용자 메시지
        messages.append({"role": "user", "content": user_input})

        # API 호출 (모델이 지침에 따라 길이 맞춤하도록)
        response = self._call_api(messages, stream=True)

        # 계산용 텍스트: 이미지 라인 제외
        calc_text = self._strip_image_lines(response)
        # 메시지에 계산된 길이 요약(디버깅용, 필요시 제거)
        title_body = calc_text.replace('# ', '')
        # 대화 이력 업데이트
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "_calc_text": title_body}


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY 환경변수가 필요합니다.")
        return
    chat = EnhancedRecursiveThinkingChat(
        api_key=api_key,
        model="gpt-3.5-turbo",
        system_prompt_file="prompt_test.txt",
        reference_csv="test_write_data5.csv"
    )
    print("Chat 시작 (exit 입력 시 종료)")
    while True:
        inp = input("You: ").strip()
        if inp.lower() == "exit":
            break
        if not inp:
            continue
        result = chat.think_and_respond(inp)
        print(f"\n🤖 AI FINAL RESPONSE:\n{result['response']}\n")

if __name__ == "__main__":
    main()

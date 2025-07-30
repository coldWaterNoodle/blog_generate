# generator/recursive_generator.py

from generator.gemini_engine import generate_content
from generator.postprocessor import inject_components
from generator.prompt_builder import build_prompt

class RecursiveBlogGenerator:
    def __init__(self, max_rounds=3):
        self.max_rounds = max_rounds

    def generate_initial(self, base_prompt: str) -> str:
        return generate_content(base_prompt)

    def reflect_and_improve(self, base_prompt: str, current: str) -> str:
        prompt = f"""{base_prompt}

---

아래는 현재 작성된 블로그 글입니다:

{current}

이 글의 SEO 측면 또는 표현 측면에서 부족한 점을 분석하고, 개선된 글을 새로 작성해주세요.
"""
        return generate_content(prompt)

    def generate_with_thinking(self, data: dict) -> str:
        base_prompt = build_prompt(data)
        current = self.generate_initial(base_prompt)

        for round_num in range(self.max_rounds):
            improved = self.reflect_and_improve(base_prompt, current)
            if improved.strip() == current.strip():
                break
            current = improved

        return inject_components(current, data)

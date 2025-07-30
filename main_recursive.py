from generator.recursive_generator import think_and_respond
from generator.prompt_builder import create_prompt
from generator.gemini_engine import postprocess_markdown


def generate_blog_article(data: dict) -> str:
    prompt = create_prompt(data)
    result = think_and_respond(prompt)

    if isinstance(result, dict):
        raw_markdown = result["response"]
    else:
        raw_markdown = result

    final_markdown = postprocess_markdown(raw_markdown, data)
    return final_markdown

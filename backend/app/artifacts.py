def build_markdown_prompt(
    question: str,
    answer: str,
) -> str:

    return f"""
Create a Markdown document based on the grounded answer below.

Requirements:
- Use Markdown headings
- Use bullet points where useful
- Use bold emphasis selectively
- Keep claims grounded in the provided answer
- Do not add unsupported facts
- Return only the Markdown document

REQUEST:
{question}

GROUNDED ANSWER:
{answer}
"""


def build_html_prompt(
    question: str,
    answer: str,
) -> str:

    return f"""
Create a complete standalone HTML document based on the
grounded answer below.

Requirements:
- Return complete HTML
- Include CSS inside <style>
- Make it readable and professional
- No JavaScript
- Do not load external resources
- Keep all claims grounded in the provided answer
- Return only HTML

REQUEST:
{question}

GROUNDED ANSWER:
{answer}
"""
def build_markdown_prompt(
    question: str,
    grounded_answer: str,
) -> str:

    return f"""
You are creating a Markdown artifact for a product manager.

Create a useful Markdown document based ONLY on the grounded
answer below.

Requirements:
- Use clear Markdown headings.
- Use bullet points where useful.
- Use bold emphasis selectively.
- Make the document practical and easy to read.
- Do not invent facts.
- Do not introduce claims that are not supported by the grounded answer.
- Return ONLY the Markdown document.
- Do not wrap the response in ```markdown fences.

USER REQUEST:
{question}

GROUNDED ANSWER:
{grounded_answer}

MARKDOWN DOCUMENT:
"""


def build_html_prompt(
    question: str,
    grounded_answer: str,
) -> str:

    return f"""
You are creating an HTML artifact for a product manager.

Create a complete standalone HTML document based ONLY on the
grounded answer below.

Requirements:
- Return complete HTML beginning with <!DOCTYPE html>.
- Include CSS inside a <style> tag.
- Make it clean and readable.
- Do not use JavaScript.
- Do not load external resources.
- Do not use external fonts, images, scripts, or stylesheets.
- Do not invent facts.
- Keep all claims grounded in the provided answer.
- Return ONLY the HTML document.
- Do not wrap it in Markdown code fences.

USER REQUEST:
{question}

GROUNDED ANSWER:
{grounded_answer}

HTML DOCUMENT:
"""
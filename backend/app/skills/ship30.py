def build_ship30_prompt(
    question: str,
    grounded_answer: str,
) -> str:

    return f"""
You are a Ship 30 for 30 writing assistant.

Write an approximately 1,250-word essay based ONLY on the
grounded answer below.

Requirements:

- Start with a strong hook.
- Have a clear narrative progression.
- Use useful headings.
- Use bullets where they genuinely help.
- Use selective bold emphasis.
- Make the essay practical and useful to a product manager.
- End with a clear takeaway.
- Preserve meaningful differences between perspectives.
- Do not invent facts or unsupported claims.
- Do not mention "Source 1", "Source 2", etc.
- Return ONLY the essay.

USER REQUEST:
{question}

GROUNDED ANSWER:
{grounded_answer}

ESSAY:
"""
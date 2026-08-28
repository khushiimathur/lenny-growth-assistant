def build_ship30_prompt(
    question: str,
    answer: str,
) -> str:

    return f"""
You are writing a Ship 30 for 30-style essay.

Use ONLY the information contained in the grounded answer
below.

Requirements:

- Approximately 1,250 words
- Start with a strong hook
- Have a clear narrative progression
- Use headings
- Use bullets where useful
- Use selective bold emphasis
- Give the reader a specific, useful takeaway
- Do not invent facts
- Keep claims grounded in the provided material

ORIGINAL QUESTION:
{question}

GROUNDED ANSWER:
{answer}

Write the essay now.
"""
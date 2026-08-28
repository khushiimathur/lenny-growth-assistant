def detect_intent(message: str) -> str:
    text = message.lower()

    if (
        "ship 30" in text
        or "ship30" in text
        or "write an essay" in text
        or "write a 1250" in text
        or "write a 1,250" in text
    ):
        return "ship30"

    if (
        "markdown" in text
        or "generate markdown" in text
        or "document" in text
    ):
        return "markdown"

    if (
        "html" in text
        or "generate html" in text
        or "html page" in text
        or "create a webpage" in text
    ):
        return "html"

    return "chat"
from app.knowledge.rag import RAGService


def main():

    rag = RAGService()

    question = (
        "How do I know if my product has "
        "product-market fit?"
    )

    result = rag.answer(
        question,
        top_k=5,
    )

    print("\n")
    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    print("\n")
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n")
    print("=" * 80)
    print("SOURCES")
    print("=" * 80)

    for source in result["sources"]:

        print(
            f"\n{source['guest']}"
        )

        print(
            source["title"]
        )

        print(
            f"Timestamp: "
            f"{source['start_timestamp']} - "
            f"{source['end_timestamp']}"
        )

        print(
            source["youtube_url"]
        )


if __name__ == "__main__":
    main()
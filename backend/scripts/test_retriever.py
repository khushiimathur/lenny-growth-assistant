from app.knowledge.retriever import Retriever


def main():

    retriever = Retriever()

    query = (
        "How do I know if my product has "
        "product-market fit?"
    )

    results = retriever.search(
        query=query,
        top_k=5,
    )

    print("\n")
    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(query)

    for index, result in enumerate(
        results,
        start=1,
    ):

        source = result["source"]

        print("\n")
        print("=" * 80)
        print(f"RESULT #{index}")
        print("=" * 80)

        print(
            f"Distance: {result['distance']}"
        )

        print(
            f"Guest: {source['guest']}"
        )

        print(
            f"Episode: {source['title']}"
        )

        print(
            f"Timestamp: "
            f"{source['start_timestamp']} "
            f"- "
            f"{source['end_timestamp']}"
        )

        print(
            f"URL: {source['youtube_url']}"
        )

        print("\nTEXT:")
        print(result["text"])


if __name__ == "__main__":
    main()
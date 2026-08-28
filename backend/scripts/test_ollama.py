from app.llm.ollama_client import OllamaClient


def main():

    client = OllamaClient()

    response = client.generate(
        "Explain product-market fit in two sentences."
    )

    print("\nOLLAMA RESPONSE:\n")
    print(response)


if __name__ == "__main__":
    main()
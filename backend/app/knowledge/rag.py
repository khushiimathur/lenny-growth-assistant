from app.knowledge.prompt import build_rag_prompt
from app.knowledge.retriever import Retriever
from app.llm.ollama_client import OllamaClient

from app.skills.artifacts import (
    build_markdown_prompt,
    build_html_prompt,
)

from app.skills.ship30 import build_ship30_prompt


class RAGService:

    def __init__(self):
        self.retriever = Retriever()
        self.llm = OllamaClient()

    def answer(
        self,
        question: str,
        history: list[dict] | None = None,
        top_k: int = 3,
    ):

        results = self.retriever.search(
            query=question,
            top_k=top_k,
        )

        prompt = build_rag_prompt(
            question=question,
            results=results,
            history=history,
        )

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": [
                result["source"]
                for result in results
            ],
        }

    def generate_artifact(
        self,
        artifact_type: str,
        question: str,
        grounded_answer: str,
    ) -> str:

        if artifact_type == "markdown":
            prompt = build_markdown_prompt(
                question,
                grounded_answer,
            )

        elif artifact_type == "html":
            prompt = build_html_prompt(
                question,
                grounded_answer,
            )

        elif artifact_type == "ship30":
            prompt = build_ship30_prompt(
                question,
                grounded_answer,
            )

        else:
            raise ValueError(
                f"Unsupported artifact type: {artifact_type}"
            )

        return self.llm.generate(prompt)
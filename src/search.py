"""Find the chunks of the user's data that best match a question.

Version 1 uses TF-IDF: it scores chunks by the words they share with the
question, giving more weight to rare words (like "GPA") than common ones.
"""
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.knowledge_base import Chunk, load_chunks


class Searcher:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english")
        # the heading is included because it often IS the question
        texts = [f"{c.title}\n{c.text}" for c in chunks]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, question: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        """Return up to top_k (chunk, score) pairs, best first. Score is 0-1."""
        scores = cosine_similarity(self.vectorizer.transform([question]), self.matrix)[0]
        best = scores.argsort()[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in best if scores[i] > 0]


if __name__ == "__main__":
    folder = sys.argv[2] if len(sys.argv) > 2 else "data/personal"
    searcher = Searcher(load_chunks(folder))
    question = sys.argv[1] if len(sys.argv) > 1 else input("Question: ")
    results = searcher.search(question)
    if not results:
        print("No matching information found.")
    for chunk, score in results:
        print(f"[{score:.2f}] {chunk.source} > {chunk.title}\n    {chunk.text[:100]}...")
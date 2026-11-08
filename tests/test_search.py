from src.knowledge_base import Chunk, load_chunks
from src.search import Searcher

CHUNKS = [
    Chunk("profile.md", "Education", "I study Software Engineering at Zhengzhou University."),
    Chunk("profile.md", "Languages", "Arabic, English, French and some Chinese."),
    Chunk("qa.md", "Your GPA is low, why?", "My first year was hard because the major was new."),
]


def test_best_match_comes_first():
    results = Searcher(CHUNKS).search("Which university do you study at?")
    assert results[0][0].title == "Education"


def test_matches_question_heading():
    results = Searcher(CHUNKS).search("Why is your GPA so low?")
    assert results[0][0].title == "Your GPA is low, why?"


def test_unrelated_question_returns_nothing():
    assert Searcher(CHUNKS).search("pizza recipe") == []


def test_top_k_limits_results():
    results = Searcher(CHUNKS).search("study university languages GPA", top_k=2)
    assert len(results) == 2


def test_works_on_sample_data():
    results = Searcher(load_chunks("data/sample")).search("Tell me about your projects")
    assert results
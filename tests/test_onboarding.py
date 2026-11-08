from src.knowledge_base import load_chunks
from src.onboarding import QUESTIONS, build_markdown, has_data, run_onboarding


def test_build_markdown_skips_empty_answers():
    md = build_markdown("Profile", {"Skills": "Python", "Languages": "  "})
    assert "## Skills\nPython" in md
    assert "Languages" not in md


def test_has_data(tmp_path):
    assert not has_data(tmp_path)
    (tmp_path / "profile.md").write_text("## A\nb", encoding="utf-8")
    assert has_data(tmp_path)


def test_onboarding_answers_become_chunks(tmp_path):
    fake_ask = lambda question: "my answer"
    run_onboarding(tmp_path, ask=fake_ask)
    chunks = load_chunks(tmp_path)
    total_questions = sum(len(q) for q in QUESTIONS.values())
    assert len(chunks) == total_questions
    assert all(c.text == "my answer" for c in chunks)
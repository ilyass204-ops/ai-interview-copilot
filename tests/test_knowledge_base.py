from src.knowledge_base import load_chunks, split_markdown


def test_splits_one_chunk_per_section():
    text = "# Title\n\n## Education\nZhengzhou University\n\n## Skills\nPython"
    chunks = split_markdown(text, "profile.md")
    assert [c.title for c in chunks] == ["Education", "Skills"]
    assert chunks[0].text == "Zhengzhou University"
    assert chunks[0].source == "profile.md"


def test_skips_empty_sections():
    chunks = split_markdown("## Empty\n\n## Full\nsome text", "x.md")
    assert [c.title for c in chunks] == ["Full"]


def test_load_chunks_reads_only_md_files(tmp_path):
    (tmp_path / "a.md").write_text("## A\none", encoding="utf-8")
    (tmp_path / "b.md").write_text("## B\ntwo", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("## C\nignored", encoding="utf-8")
    chunks = load_chunks(tmp_path)
    assert [c.source for c in chunks] == ["a.md", "b.md"]


def test_sample_data_loads():
    assert len(load_chunks("data/sample")) >= 3
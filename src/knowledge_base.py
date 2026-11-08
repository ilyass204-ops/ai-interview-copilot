"""Load personal knowledge files and split them into searchable chunks."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    source: str  # file the chunk came from, e.g. "profile.md"
    title: str   # the "## " heading of the section
    text: str    # the section's content


def split_markdown(text: str, source: str) -> list[Chunk]:
    """Split one markdown file into chunks: one chunk per '## ' section."""
    chunks = []
    title, lines = None, []

    def save_current():
        body = "\n".join(lines).strip()
        if title and body:  # skip text before the first heading and empty sections
            chunks.append(Chunk(source, title, body))

    for line in text.splitlines():
        if line.startswith("## "):
            save_current()
            title, lines = line[3:].strip(), []
        else:
            lines.append(line)
    save_current()
    return chunks


def load_chunks(folder: str | Path) -> list[Chunk]:
    """Read every .md file in a folder and return all their chunks."""
    chunks = []
    for path in sorted(Path(folder).glob("*.md")):
        chunks.extend(split_markdown(path.read_text(encoding="utf-8"), path.name))
    return chunks


if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "data/sample"
    for chunk in load_chunks(folder):
        print(f"[{chunk.source}] {chunk.title}: {chunk.text[:60]}...")
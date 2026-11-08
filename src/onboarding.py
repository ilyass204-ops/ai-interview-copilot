"""First-run questionnaire: asks the user about themselves and saves the
answers as markdown files that the knowledge base can read."""
from pathlib import Path

# file name -> list of (section title, question shown to the user)
QUESTIONS = {
    "profile.md": [
        ("Basic info", "What is your full name, nationality, and where do you live?"),
        ("Education", "What do you study, at which university, and when do you graduate?"),
        ("Skills", "Which programming languages and tools do you know?"),
        ("Languages", "Which languages do you speak, and at what level?"),
        ("Projects", "Describe your projects (name, what it does, technologies)."),
        ("Goal", "What master's or job are you aiming for?"),
    ],
    "qa.md": [
        ("Introduce yourself", "Introduce yourself in 2-3 sentences."),
        ("Why do you want a master's?", "Why do you want to do a master's?"),
        ("Tell me about your best project", "Tell me about your best project."),
        ("What are your strengths and weaknesses?", "What are your strengths and weaknesses?"),
    ],
}

# file name -> title written at the top of that file
TITLES = {"profile.md": "My profile", "qa.md": "My interview answers"}


def has_data(folder: str | Path) -> bool:
    """True if the user's data folder already contains markdown files."""
    return any(Path(folder).glob("*.md"))


def build_markdown(title: str, answers: dict[str, str]) -> str:
    """Turn {section title: answer} into markdown, skipping empty answers."""
    parts = [f"# {title}"]
    for section, answer in answers.items():
        if answer.strip():
            parts.append(f"## {section}\n{answer.strip()}")
    return "\n\n".join(parts) + "\n"


def run_onboarding(folder: str | Path, ask=input) -> list[Path]:
    """Ask every question, save one markdown file per group, return the paths.

    `ask` is the function used to ask a question (input by default);
    tests replace it with a fake so they don't need a keyboard.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    print("Welcome! Answer a few questions so the copilot can answer like you.")
    print("Press Enter to skip a question.\n")

    saved = []
    for file_name, questions in QUESTIONS.items():
        answers = {section: ask(f"{question}\n> ") for section, question in questions}
        path = folder / file_name
        path.write_text(build_markdown(TITLES[file_name], answers), encoding="utf-8")
        saved.append(path)
    print(f"\nSaved your answers in {folder}/")
    return saved
"""Entry point: run the questionnaire on first use, then load the user's data."""
import sys

from src.knowledge_base import load_chunks
from src.onboarding import has_data, run_onboarding

DEFAULT_FOLDER = "data/personal"


def main(folder: str = DEFAULT_FOLDER):
    if not has_data(folder):
        run_onboarding(folder)
    chunks = load_chunks(folder)
    print(f"Copilot ready: {len(chunks)} pieces of information loaded from {folder}/")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FOLDER)
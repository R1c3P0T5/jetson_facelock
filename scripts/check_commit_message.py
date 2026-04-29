from __future__ import annotations

from pathlib import Path
import re
import sys


ALLOWED_TYPES = [
    "feat",
    "fix",
    "chore",
    "docs",
    "refactor",
    "test",
    "ci",
    "build",
    "perf",
    "style",
]

VAGUE_SUBJECTS = {"misc changes", "stuff", "updates", "fixes"}
HEADER_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[a-z0-9_-]+)\))?:\s(?P<subject>.+)$"
)


def validate_commit_message(message: str) -> dict[str, object]:
    first_line = message.splitlines()[0].strip() if message.splitlines() else ""
    match = HEADER_PATTERN.match(first_line)

    if match is None:
        return {
            "ok": False,
            "errors": [
                "Commit header must follow type(scope): subject or type: subject."
            ],
        }

    commit_type = match.group("type")
    subject = match.group("subject")

    if commit_type not in ALLOWED_TYPES:
        return {
            "ok": False,
            "errors": [
                "Commit type must be one of: feat, fix, chore, docs, refactor, test, ci, build, perf, style."
            ],
        }

    if subject in VAGUE_SUBJECTS:
        return {
            "ok": False,
            "errors": [
                "Commit subject is too vague. Use a specific action and object."
            ],
        }

    errors: list[str] = []

    if re.search(r"[.!?]$", subject):
        errors.append("Commit subject must not end with punctuation.")

    first_word = subject.split()[0]
    if re.fullmatch(r"[a-z][a-z0-9-]*", first_word) is None:
        errors.append(
            "Commit subject must start with a lowercase imperative verb (ASCII letters), e.g. add, fix, update, remove, refactor."
        )
    elif (first_word.endswith("ed") and len(first_word) > 4) or (
        first_word.endswith("ing") and len(first_word) > 5
    ):
        errors.append(
            "Commit subject should use imperative mood (e.g. 'add', not 'added' or 'adding')."
        )

    return {"ok": not errors, "errors": errors}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python scripts/check_commit_message.py <commit-message-file>",
            file=sys.stderr,
        )
        return 1

    commit_message_path = Path(argv[1])
    message = commit_message_path.read_text(encoding="utf-8")
    result = validate_commit_message(message)

    if result["ok"]:
        return 0

    print("Commit message validation failed:", file=sys.stderr)
    for error in result["errors"]:
        print(f"- {error}", file=sys.stderr)
    print("Valid example: feat(frontend): add login form", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

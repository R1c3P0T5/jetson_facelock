from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("check_commit_message.py")


def load_module():
    spec = spec_from_file_location("check_commit_message", SCRIPT_PATH)
    module = module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ValidateCommitMessageTest(unittest.TestCase):
    def test_accepts_valid_lowercase_verb_subject(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("feat(frontend): add login form"),
            {"ok": True, "errors": []},
        )

    def test_rejects_subject_ending_with_period(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("chore: update pre-commit hooks."),
            {
                "ok": False,
                "errors": ["Commit subject must not end with punctuation."],
            },
        )

    def test_rejects_uppercase_subject_start(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("feat: Add login form"),
            {
                "ok": False,
                "errors": [
                    "Commit subject must start with a lowercase verb such as add, fix, update, remove, refactor, rename, improve, simplify, or revert.",
                ],
            },
        )

    def test_rejects_low_signal_phrases(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("fix: misc changes"),
            {
                "ok": False,
                "errors": [
                    "Commit subject is too vague. Use a specific action and object."
                ],
            },
        )

    def test_rejects_unknown_commit_type(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("feature: add login form"),
            {
                "ok": False,
                "errors": [
                    "Commit type must be one of: feat, fix, chore, docs, refactor, test, ci, build, perf, style."
                ],
            },
        )

    def test_rejects_non_conventional_format(self):
        module = load_module()

        self.assertEqual(
            module.validate_commit_message("Add login form"),
            {
                "ok": False,
                "errors": [
                    "Commit header must follow type(scope): subject or type: subject."
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()

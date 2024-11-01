import sys
import re

args = sys.argv[1:]

if len(args) != 1:
    print("Usage: validate_commit_msg.py <commit-msg-file>")
    sys.exit(1)

commit_msg_file = args[0]

commit_msg_types = [
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "chore",
    "revert",
]
commit_msg_regex = rf"^({'|'.join(commit_msg_types)}): .+"

with open(commit_msg_file, "r") as f:
    commit_msg = f.read()

    if not re.match(commit_msg_regex, commit_msg):
        print(f"Commit message invalid: '{commit_msg}'")
        print(
            f"Invalid commit message format, commit message must match the following regex: {commit_msg_regex}."
        )
        print(
            "See README for details on commit message format in Contributing section."
        )

        sys.exit(1)

    sys.exit(0)

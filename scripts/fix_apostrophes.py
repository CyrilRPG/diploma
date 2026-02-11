#!/usr/bin/env python3
"""Fix unescaped apostrophes in UPEC flashcard JS strings."""

import os
import re

base = "UPEC_LSPS1_S2"
CURLY = "\u2019"  # Right single quotation mark (curly apostrophe)

count = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not (f.endswith(".html") and f.startswith("fc")):
            continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()

        match = re.search(
            r"(const flashcardsData\s*=\s*\[)(.*?)(\];\s*\n)", content, re.DOTALL
        )
        if not match:
            continue

        before = content[: match.start()]
        prefix = match.group(1)
        data = match.group(2)
        suffix = match.group(3)
        after = content[match.end() :]

        # Replace French contractions: word'word -> word'word (curly)
        french_letters = r"[a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇ]"
        new_data = re.sub(
            f"({french_letters})'({french_letters})",
            lambda m: m.group(1) + CURLY + m.group(2),
            data,
        )

        if new_data != data:
            content = before + prefix + new_data + suffix + after
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            count += 1
            rel = os.path.relpath(path, base)
            print(f"Fixed: {rel}")

print(f"\nTotal fixed: {count}")

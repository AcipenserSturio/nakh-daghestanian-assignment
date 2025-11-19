import re
from typing import Generator

columns = ["lemma", "morph1", "morph2", "reference_type", "reference_lemma"]

def process_row(row: dict[str, str]) -> Generator[list[str] | None]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

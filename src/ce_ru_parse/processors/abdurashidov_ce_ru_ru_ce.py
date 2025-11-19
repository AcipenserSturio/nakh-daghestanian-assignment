import re
from typing import Generator


def process_row(row: dict[str, str]) -> Generator[dict[str, str] | None]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    yield {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Bersanov 2013",
        "annotator": "Shestakov Maxim",

        "id_meaning": "",
        "id_word": "",
        "lemma": "",
        "ipa": "",

        "morphology": "",
        "pos": "",
        "meaning_ru": "",
        "examples": "",

        "definition": "",
    }

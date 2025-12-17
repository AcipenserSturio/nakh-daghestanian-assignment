import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    meaning_ru = row["word"]
    meaning_ru = re.split(r"[\(\)\,\!\?]", meaning_ru)[0]

    m = re.match(r"(?P<meaning>.*?)(\((?P<morph>.*)\))", row["translate"])
    if not m:
        # print(row["translate"])
        return
    lemma = m.group("meaning").strip()
    morph = m.group("morph")

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Aslahanov",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": "",
        "pos": "",
        "meaning_ru": meaning_ru,
        "examples": "",

        "definition": string,
    }

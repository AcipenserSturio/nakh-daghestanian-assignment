import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    l = re.match(r"(?P<lemma>[^,]+)(, ?(?P<tag>.*))?", row["word"])
    if not l:
        return
    meaning_ru = l.group("lemma")
    _morph = l.group("tag")
    # print(meaning_ru, "\t\t\t", _morph)


    m = re.match(r"(?P<meaning>[^;]+)(; (?P<examples>.*))?", row["translate"])
    if not m:
        # print(row["translate"])
        return
    lemma = m.group("meaning").strip()
    examples = m.group("examples")

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Karasaev 1978",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": "",
        "pos": "",
        "meaning_ru": meaning_ru,
        "examples": examples,

        "definition": string,
    }

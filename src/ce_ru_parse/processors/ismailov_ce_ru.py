import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    lemma = row["word"]

    m = re.match(r" ?((\<i\>|\()(?P<tag>.*)(\<\/i\>|\)))? – (?P<meaning>.*)", row["translate"])
    if not m:
        # print(row["translate"])
        return
    tag = m.group("tag")
    meaning_ru = m.group("meaning").strip()
    # Delete HTML
    meaning_ru = re.sub(r"\<.*?>", "", meaning_ru)
    # Drop stuff post first punctuation
    meaning_ru = re.split(r"[\(\)\,\!\?\<\>\;]", meaning_ru)[0]

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Ismailov (ce-ru)",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": tag,
        "pos": "",
        "meaning_ru": meaning_ru,
        "examples": "",

        "definition": string,
    }

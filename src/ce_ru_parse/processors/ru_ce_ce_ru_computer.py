import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    l = re.match(r"(?P<lemma>.*) (?P<tag>(\<i\>|\().*(\<\/i\>|\)))", row["word"])
    if not l:
        # print(row["word"])
        return
    lemma = l.group("lemma")
    word_class_tag = l.group("tag")

    m = re.match(r"(?P<meaning>.*?)(\n?\<br ?\/\>(?P<examples>.*))", row["translate"] + "<br />")
    if not m:
        # print(row["translate"])
        return
    meaning_ru = m.group("meaning").strip()
    # Drop Russian vowel length marking
    meaning_ru = meaning_ru.replace("\u0301", "")
    # Drop stuff post first punctuation
    meaning_ru = re.split(r"[\(\)\,\.\!\?\<\>\;]", meaning_ru)[0]

    examples = m.group("examples")

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Umarhadjiev",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": "",
        "pos": word_class_tag,
        "meaning_ru": meaning_ru,
        "examples": examples,

        "definition": string,
    }

import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    l = re.match(r"(?P<lemma>.*) (?P<tag>.);", row["word"])
    if not l:
        return
    lemma = l.group("lemma")
    word_class_tag = l.group("tag")

    m = re.match(r"(?P<morph>\<b\>.*?\<\/b\>)(?P<meaning>.*?)(\n?;(?P<examples>.*))", row["translate"] + ";")
    if not m:
        # print(row["translate"])
        return
    morph = m.group("morph")
    meaning_ru = m.group("meaning").strip()
    examples = m.group("examples").strip()
    examples = examples.replace("<b>", "<che>").replace("</b>", "</che>")
    examples = examples.replace("<i>", "").replace("</i>", "")

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Umarhadjiev 2010",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": morph,
        "pos": word_class_tag,
        "meaning_ru": meaning_ru,
        "examples": examples,

        "definition": string,
    }

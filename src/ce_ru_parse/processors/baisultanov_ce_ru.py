import re
from typing import Optional


def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    l = re.match(r"(?P<lemma>.*?) (?P<tag>\(.*\))", row["word"])
    if not l:
        # print(row["word"])
        return
    lemma = l.group("lemma").replace("«", "").replace("»", "")
    morph = l.group("tag")

    m = re.match(r"(?P<qualifier>(Прост-ирон|Разг.-шутл|Прост|Устар|Разг|Религ|Диал|Старин|Уст|Ирон|Уст\. Прост)\.)? ?((?P<meaning>.*?)\.?)(\n?\<br ?\/\>(?P<examples>.*))", row["translate"] + "<br />")
    if not m:
        # print(row["translate"])
        return
    qualifier = m.group("qualifier")
    meaning_ru = m.group("meaning").strip()
    examples = m.group("examples")

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Baisultanov (2015)",
        "annotator": "Shestakov Maxim",

        "id_meaning": "1",
        "id_word": row["id"],
        "lemma": lemma,
        "ipa": "",

        "morphology": morph,
        "pos": qualifier,
        "meaning_ru": meaning_ru,
        "examples": examples,

        "definition": string,
    }

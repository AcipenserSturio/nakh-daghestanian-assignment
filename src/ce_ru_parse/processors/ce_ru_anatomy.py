import re


def process_row(row: dict[str, str]) -> dict[str, str] | None:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    lemma = row["word"].split("(")[0].strip()
    meaning_ru = row["translate"].split("(")[0]
    examples = row["translate"].split(")")[-1]

    # consider:
    # Мышца, поднимающая верхнюю губу и крылья носа
    # Лакхара балда а, меран тӀемаш а хьалаойу оьзг
    if "," in lemma:
        return

    # Sometimes the data is erroneously flipped.
    if "Ӏ" in meaning_ru or "аь" in meaning_ru:
        meaning_ru, lemma = lemma, meaning_ru

    return {
        "language": "Chechen",
        "glottocode": "chec1245",
        "reference": "Bersanov 2013",
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

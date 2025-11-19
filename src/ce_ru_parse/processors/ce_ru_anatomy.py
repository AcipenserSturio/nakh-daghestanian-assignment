import re


def process_row(row: dict[str, str]) -> dict[str, str] | None:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    # TODO: sometimes the lemma and meaning_ru are backwards.
    # try using the orthography to unswap them.
    lemma = row["word"].strip()
    meaning_ru = row["translate"].split("(")[0]
    examples = row["translate"].split(")")[-1]

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

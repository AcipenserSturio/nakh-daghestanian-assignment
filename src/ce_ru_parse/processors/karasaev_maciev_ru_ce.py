import re
from typing import Optional


def extract_lemmas(text: str):

    pattern_defs = r'(?<=\d[.)]\s)(.*?)(?=(?:\d+[.)]\s)|$)'
    defs = [d.strip() for d in re.findall(pattern_defs, text, flags=re.S | re.U)]
    if not defs:
        defs = [text]
    lemmas = []
    for lemma in defs:
        # Delete HTML
        lemma = re.sub(r"\<.*?\>.*?\<.*?>", "", lemma)
        # Delete possible leftover brackets
        lemma = re.sub(r"\( ?\)", "", lemma).strip()
        # Drop stuff post first punctuation
        lemma = re.split(r"[\(\)\,\.\!\?\<\>\;]", lemma)[0]
        # Ignore long phrases
        if len(lemma.split(" ")) > 2:
            continue
        if lemma.isdigit():
            continue
        if re.match("^-", lemma):
            continue
        if "[" in lemma or "]" in lemma:
            continue
        if lemma in {"а", "а́я", "ая", "аяся"}:
            continue
        if not lemma:
            continue

        # dictionary-specific long vowel markers; maybe keep?
        lemma = lemma.replace("\u0303", "")
        lemmas.append(lemma)

    return lemmas

def process_row(row: dict[str, str]) -> Optional[dict[str, str]]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    l = re.match(r"(?P<lemma>[^,]+)(, ?(?P<tag>.*))?", row["word"])
    if not l:
        return
    meaning_ru = l.group("lemma")
    meaning_ru = re.sub(r"\d", "", meaning_ru)
    meaning_ru = meaning_ru.replace("\u0301", "")

    _morph = l.group("tag")
    # print(meaning_ru, "\t\t\t", _morph)


    m = re.match(r"(?P<meaning>[^;]+)(; (?P<examples>.*))?", row["translate"])
    if not m:
        # print(row["translate"])
        return
    lemma = m.group("meaning").strip()
    lemmas = extract_lemmas(lemma)

    examples = m.group("examples")

    for index, lemma in enumerate(lemmas):
        return {
            "language": "Chechen",
            "glottocode": "chec1245",
            "reference": "Karasaev 1978",
            "annotator": "Shestakov Maxim",

            "id_meaning": str(index+1),
            "id_word": row["id"],
            "lemma": lemma,
            "ipa": "",

            "morphology": "",
            "pos": "",
            "meaning_ru": meaning_ru,
            "examples": examples,

            "definition": string,
        }

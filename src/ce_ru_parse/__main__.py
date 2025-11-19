import json
from pathlib import Path

import pandas as pd
import requests

from .processors import maciev_ce_ru

columns = [
    "id_meaning",
    "lemma",
    "morph",
    "reference_type",
    "reference_lemma",
    "morph_tag",
    "meaning_ru",
    "example",
    "raw",
]

def get_rows():
    if Path("wordlist.json").exists():
        with open("wordlist.json") as f:
            wordlist = json.load(f)
    else:
        URL = "https://raw.githubusercontent.com/laamxo/dosham/refs/heads/main/unified.json"
        wordlist = requests.get(URL).json()
        with open("wordlist.json", "w") as f:
            json.dump(wordlist, f)

    for row in wordlist:
        yield {
            "id": row["id"],
            "word": row["word"],
            "translate": row["translate"],
            "source": row["parent"]
        }


def main():
    df: list[dict[str, str]] = []
    for row in get_rows():
        match row["source"]:
            case "maciev_ce_ru":
                for row_ in maciev_ce_ru.process_row(row):
                    if row_:
                        df.append(row_)
                continue
            case _:
                continue
    df_: list[list[str]] = [[row[col] for col in columns] for row in df]
    (pd.DataFrame(df_, columns=columns)
        .sort_values(by=["lemma", "id_meaning"])
        .drop_duplicates()
        .to_csv("processed.csv")
    )

# examples = [
#     "<i>прил.</i> 1) па́русный; <b>гатанан ке̃ма </b>па́русная ло́дка; 2) полоте́нечный; 3) полотняный; паруси́новый; холщо́вый.",
#     "<i>прич.</i> ветви́стый.",
#     "шум (<i>голосов</i>); <b>а̃рахь гӀар</b>-<b>говгӀа яьлла </b>на дворе́ подня́лся шум.",
#     "1) уси́лие, напо́р; 2) опо́ра, опло́т, <b>Советски Союз </b>– <b>машаран гӀортõ ю </b>Сове́тский Сою́з – опло́т ми́ра.",
# ]

# for e in examples:
#     print(parse_definition(e))


if __name__ == "__main__":
    main()

from typing import Generator
import requests
import re
from pathlib import Path
import json
import pandas as pd

columns = ["lemma", "morph1", "morph2", "reference_type", "reference_lemma"]

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


def parse_definition(text):
    # 1. Extract optional morph
    pattern_morph = r'^(?:<i>(?P<morph>.*?)<\/i>)?\s*(?P<rest>.*)'
    m = re.match(pattern_morph, text.strip(), flags=re.S)
    morph = m.group('morph')
    rest = m.group('rest').strip()

    # 2. Extract definitions, excluding numeric markers
    pattern_defs = r'(?<=\d[.)]\s)(.*?)(?=(?:\d+[.)]\s)|$)'
    defs = [d.strip() for d in re.findall(pattern_defs, rest, flags=re.S | re.U)]

    # 3. If no numeric markers, treat all as one definition
    if not defs and rest:
        defs = [rest.strip()]

    # 4. Split into keyword / example
    def split_def(d):
        parts = d.split(';', 1)
        keyword = parts[0].strip()
        example = parts[1].strip() if len(parts) > 1 else None
        return {'keyword': keyword, 'example': example}

    definitions = [split_def(d) for d in defs]

    return {"morph": morph, "definitions": definitions}


def process_maciev(row: dict[str, str]) -> Generator[list[str] | None]:
    if not row["word"] or not row["translate"]:
        # print(f"skipping {row["id"]}: no word/translate")
        return

    string = f"{row["word"]} | {row["translate"]}"

    # fix palochka in a couple of lines.
    string = string.replace("l", "Ӏ")

    # These rows actually correspond to definition segments,
    # which are too fragmentary to extract the correct word from.
    if "[/ | i]]" in string:
        # print(f"skipping {row["id"]}: fragmentary data")
        return

    # The word contains Russian acute diacritic, which should never happen
    # in a ce_ru dictionary. The cause is the original dictionary being parsed incorrectly.
    if "| ]" in string or "\u0301" in row["word"]:
        # print(f"skipping {row["id"]}: fragmentary data")
        return

    # reference_types = [
    #     "прил. к", "см.", "прич. от", "масд. от", "мн. от", "прич. прош. вр. от"
    # ]

    basicinfo = "".join([
        # r"(?<=\n)",
        # lemma. can be multiple words. can have parentheses. can have !.
        r"(?P<lemma>[а-яА-ЯёЁӀ1-9\u0303\u2013\- \(\)!]+)",
        # morph alongside the lemma
        r"(, ?(?P<morph1>[а-яА-ЯёЁӀ1-9\u0303\u2013\-]+))?",
        # morph in square brackets
        r" +\| (\[(?P<morph2>.*)\] )?",

        # the following is technically a definition, but it simply refer you to a different word
        # show reference type (some grammatical relation)
        r"((?P<refer><i>(?P<reference_type>см\.|[а-я\. ]+ к|[а-я\. ]+ от) ?<\/i> ?",
        # and the relevant lemma
        r"<b>(?P<reference_lemma>[а-яА-ЯёЁӀ1-9\u0303\u2013\-]+)\.?\,? ?\.?(<\/b>|\;))|)",
        # return the remaining string as meaning which we will parse further.
        r"(?P<meaning>.*)",
    ])
    # print(basicinfo)
    # print(re.match(basicinfo, "вехка2 | <i>см.</i> <b>дехка2.</b>"))
    # return True

    if match := re.match(basicinfo, string):
        # print(match.groupdict())
        # print(match.groupdict()["meaning"])
        groupdict = match.groupdict()
        meaning = parse_definition(groupdict["meaning"])
        del groupdict["meaning"]
        if meaning["definitions"]:
            for index, definition in enumerate(meaning["definitions"]):
                yield [index+1, *(groupdict[column] for column in columns), meaning["morph"], definition["keyword"], definition["example"], string]
        else:
            yield [1, *(groupdict[column] for column in columns), meaning["morph"], "", "", string]
    else:
        # print("failed parse:", string)
        pass


if __name__ == "__main__":
    df: list[list[str]] = []
    for row in get_rows():
        match row["source"]:
            case "maciev_ce_ru":
                for row_ in process_maciev(row):
                    if row_:
                        df.append(row_)
                continue
            case _:
                continue
    (pd.DataFrame(df, columns=["id_meaning", *columns, "morph_tag", "meaning_ru", "example", "raw"])
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

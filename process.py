import requests
import re
from pathlib import Path
import json

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

def process_maciev(row):
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
        r" +\| (\[(?P<morph2>[а-яА-ЯёЁӀ1-9\u0303\u2013\-]+(, [а-яА-ЯёЁӀ1-9\u0303\u2013\-]+)*)\] )?",
        # the following is technically a definition, but it simply refer you to a different word
        # show reference type (some grammatical relation)
        r"((?P<refer><i>(?P<reference_type>прил\. к|см.|прич\. от|масд. от|мн\. от|прич\. прош\. вр\. от) ?<\/i> ?",
        # and the relevant lemma
        r"<b>(?P<reference_lemma>[а-яА-ЯёЁӀ1-9\u0303\u2013\-]+)\.?<\/b>)|)",
        # return the remaining string as meaning which we will parse further.
        r"(?P<meaning>.*)",
    ])
    # print(basicinfo)
    # print(re.match(basicinfo, "вехка2 | <i>см.</i> <b>дехка2.</b>"))
    # return True

    if match := re.match(basicinfo, string):
        # print(match.groupdict())
        print(match.groupdict()["meaning"])
        pass
    else:
        # print("failed parse:", string)
        pass


if __name__ == "__main__":
    for row in get_rows():
        match row["source"]:
            case "maciev_ce_ru":
                result = process_maciev(row)
                if result:
                    break
                continue
            case _:
                continue
        print(row)

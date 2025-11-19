import re
from typing import Generator


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


def process_row(row: dict[str, str]) -> Generator[dict[str, str] | None]:
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
                yield {
                    "language": "Chechen",
                    "glottocode": "chec1245",
                    "reference": "Matsiyev 1961",
                    "annotator": "Shestakov Maxim",

                    "id_meaning": str(index+1),
                    "id_word": row["id"],
                    "lemma": groupdict["lemma"],
                    "ipa": "",

                    "morphology": (groupdict["morph1"] or groupdict["morph2"]),
                    "pos": meaning["morph"],
                    "meaning_ru": definition["keyword"],
                    "examples": definition["example"],

                    "definition": string,

                    # "reference_type": groupdict["reference_type"],
                    # "reference_lemma": groupdict["reference_lemma"],
                }
        else:
            yield {
                "language": "Chechen",
                "glottocode": "chec1245",
                "reference": "Matsiyev 1961",
                "annotator": "Shestakov Maxim",

                "id_meaning": "1",
                "id_word": row["id"],
                "lemma": groupdict["lemma"],
                "ipa": "",

                "morphology": (groupdict["morph1"] or groupdict["morph2"]),
                "pos": meaning["morph"],
                "meaning_ru": "",
                "examples": "",

                "definition": string,

                # "reference_type": groupdict["reference_type"],
                # "reference_lemma": groupdict["reference_lemma"],
            }
    else:
        # print("failed parse:", string)
        pass

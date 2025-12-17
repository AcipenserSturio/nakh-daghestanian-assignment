import re
from typing import Optional

qualifiers = [
    "Анатом",
    "АН – Академия наук.",
    "Арабск.-арабский.",
    "Бран",
    "Букв.-буквально.",
    "В,й,д,б – показатели грамматических классов в нахских языках.",
    "Восторж.-восторженное.",
    "В сб.-в сборнике.",
    "Вып.-выпуск.",
    "ВЯ – Вопросы языкознания.",
    "Груб",
    "Груб.-прост",
    "Диалект",
    "Др",
    "Ед.ч",
    "Ж",
    "Звукопод",
    "Знач",
    "Зоол",
    "Изд.-издание.",
    "Изм.-изменение.",
    "Ирон",
    "Использ",
    "И т.д",
    "И т.п",
    "ИЯЛИ – Институт языка, литературы и иискусства.",
    "Книжн",
    "Кн. Изд-во",
    "Кого-л",
    "Конф",
    "Косв",
    "Ласк",
    "Лингв",
    "Лит",
    "М",
    "Мат",
    "Мед",
    "Мн.ч",
    "Нац",
    "Неодобр",
    "Одобр",
    "О чём-л",
    "П.л",
    "Презр",
    "Пренебр",
    "Прост",
    "ПФ",
    "Р",
    "Разг",
    "РАН",
    "Рел",
    "Респуб",
    "Русск",
    "Сер. Филол. наук",
    "След",
    "Словос",
    "См",
    "Соот",
    "Ср",
    "С., стр",
    "Сущ",
    "Т.к",
    "Трансф",
    "Устар",
    "Уничиж",
    "Чеч",
    "Что-л",
    "Шутл",
    "Шутл.-ирон",
    "Экспресс",
    "Яз",

    "-разг",
    "Старин",
    "Прост-разг",
    "Уст",
    "Из арабск",
    "Прост-шутл",
    "Диал",
    "Прост-ирон",
    "Религ",
    "Чего-л",
    "Жарг",
    "Неол",
    "Архаич",
    "Из арабск, яз",
    "Доп"
    "значение",
    "Религ-лит",
    "Первонач",
    "Стар",
    "Старин-диал",
    "назв",
    "Кому-л",
    "Поэт",
    "Прост-губ",
    "Просл",
    "К кому-ч",
    "В знач",
    "Разг-прост",
    "Межд",
    "Индив",
    "слово поэта",
    "От литер",
]
qualifiers = [q.lower().strip().replace("-", "") for q in qualifiers]

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

    # m = re.match(r"(?P<qualifier>(Разг. Прост|Из арабск|Прост-ирон|Прост.-ирон|Уст. Прост|Прост.-разг|Разг.-шутл|Презр|Прост|Устар|Разг|Религ|Диал|Старин|Уст|Ирон|Уст\. Прост)\.)? ?((?P<meaning>.*?)\.?)(\n?\<br ?\/\>(?P<examples>.*))", row["translate"] + "<br />")
    m = re.match(r"((?P<meaning>.*?)\.?)(\n?\<br ?\/\>(?P<examples>.*))", row["translate"] + "<br />")
    if not m:
        # print(row["translate"])
        return
    # qualifier = m.group("qualifier")
    meaning_ru = re.sub("^ ?[–-]", "", m.group("meaning")).strip()
    meaning_ru = re.sub("Доп. значение: ", "", meaning_ru, flags=re.IGNORECASE)
    meaning_ru = [string for string in re.split(r"[\.\:]", meaning_ru.strip()) if string]
    if not meaning_ru:
        return
    # Filter out qualifiers
    meaning_ru = [sent.strip() for sent in meaning_ru if sent.strip().lower().replace("-", "") not in qualifiers]
    # Select the first valid "sentence"
    meaning_ru = meaning_ru[0]
    # Drop stuff post first punctuation
    meaning_ru = re.split(r"[\(\)\,\!\?\;]", meaning_ru)[0]
    meaning_ru = re.sub("^ ?[–-]", "", meaning_ru).strip()
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
        "pos": "",
        "meaning_ru": meaning_ru,
        "examples": examples,

        "definition": string,
    }

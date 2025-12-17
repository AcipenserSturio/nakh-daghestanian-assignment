import re

transcription_system = {
    "б": "b",
    "в": "w", #~v
    "г": "g",
    "гӀ": "ʁ", # agreed to use uvular symbol, following the transcriptions doc
    "д": "d",
    "ж": "dʒ", #~ʒ
    "з": "dz", #~z
    "й": "j",
    "к": "k", # aspirated in the doc
    "кк": "kː",
    "кх": "q", # aspirated in the doc
    "ккх": "qː",
    "къ": "q’",
    "кӀ": "k’",
    "л": "l",
    "м": "m",
    "н": "n",
    "п": "p", # aspirated in the doc
    "пп": "pː",
    "пӀ": "p’",
    "р": "r",
    "рхӏ": "r̥", # does this actually occur?
    "с": "s",
    "сс": "sː",
    "т": "t", # aspirated in the doc
    "тт": "tː",
    "тӀ": "t’",
    "ф": "f",
    "х": "x",
    "хӀ": "h",
    "хь": "ħ", #~ʜ
    "ц": "ts",
    "цӀ": "ts’",
    "ч": "tʃ", # aspirated in the doc
    "чӀ": "tʃ’",
    "ш": "ʃ",
    "ъ": "ʔ",
    "Ӏ": "ˤ", # only after a vowel - check
    "а": "ə", # , ɑː
    "аь": "æ", # , æː
    "е": "e", # e, ɛː, je, ie
    "ё": "jo",
    "и": "i",
    "ий": "iː",
    "о": "o", # , ɔː, wo, uo
    "ов": "ɔʊ",
    "оь": "ɥø", # , yø
    "у": "uʊ",
    "ув": "uː",
    "уь": "y",
    "уьй": "yː",
    "э": "e",
    "ю": "ju",
    "юь": "jy",
    "я": "ja",
    "яь": "jæ",
    # Matsiev-specific long vowel marking:
    # 'а̃': 'ɑː',
    # 'е̃': 'ɛː',
    # 'о̃': 'ɔː',
    # 'о̃ь': '',
    # 'у̃': '',
    # 'э̃': '',
    # 'ю̃': '',
    # 'я̃': ''

    # Cyrillic not in Chechen, but found anyway:
    'ы': 'ə', # complete guess

    # Remaining weirdness in the dataset:
    # Ӏьа
}

transcription_system = {cyr: ipa for cyr, ipa in sorted(transcription_system.items(), key=lambda x: len(x[0]), reverse=True)}

def transcribe(word):
    word = word.lower().strip()
    # Enforce true palochka
    word = word.replace("l", "Ӏ").replace("Ӏ", "Ӏ")
    for cyr, ipa in transcription_system.items():
        word = word.replace(cyr.lower(), f"-{ipa}")
    word = word.replace(" -", " ").replace("--", " ")
    return word[1:]

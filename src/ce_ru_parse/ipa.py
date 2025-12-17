import re

transcription_system = {
    "б": "b",
    "в": "w", #~v
    "г": "g",
    "гӀ": "ʁ",
    "д": "d",
    "ж": "dʒ", #~ʒ
    "з": "dz", #~z
    "й": "j",
    "к": "kʰ",
    "кк": "kː",
    "кх": "qʰ",
    "ккх": "qː",
    "къ": "q’",
    "кӀ": "k’",
    "л": "l",
    "м": "m",
    "н": "n",
    "п": "pʰ",
    "пп": "pː",
    "пӀ": "p’",
    "р": "r",
    "рхӏ": "r̥", # does this actually occur?
    "с": "s",
    "сс": "sː",
    "т": "tʰ",
    "тт": "tː",
    "тӀ": "t’",
    "ф": "f",
    "х": "x",
    "хӀ": "h",
    "хь": "ħ", #~ʜ
    "ц": "tsʰ",
    "цӀ": "ts’",
    "ч": "tʃʰ",
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

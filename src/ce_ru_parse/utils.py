
latin_to_cyrillic_homographs = {
    "e": "е",
    "u": "и",
    "o": "о",
    "p": "р",
    "a": "а",
    "n": "п",
    "x": "х"
}

# Some presumably cyrillic strings in the lemma have
# suspicious Latin character inclusions. replace them with cyrillic
def ensure_cyrillic(string):
    for lat, cyr in latin_to_cyrillic_homographs.items():
        string = string.replace(lat, cyr)
    return string

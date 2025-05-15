import re

mati = ["Блять", "Сука", "Еблан", "Пидр", "Долбоёб", "Охуел"]


def contains_bad_words(message_text):
    if not message_text:
        return False
    clean_text = re.sub(r'[^\w\s]', '', message_text.lower())
    return any(
        re.search(rf'\b{re.escape(word.lower())}\b', clean_text)
        for word in mati
    )

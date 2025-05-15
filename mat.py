mati = ["Блять", "Сука", "Еблан", "Пидр", "Долбоёб", "Охуел"]


def mats(message_text):
    for word in mati:
        if word.lower() in message_text.lower():
            return True
    return False

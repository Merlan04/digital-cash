categories = {
    "еда": ["еда", "burger", "pizza", "кафе", "ресторан", "обед", "завтрак", "ужин"],
    "дорога": ["такси", "метро", "бензин", "транспорт", "проезд"],
    "подписки": ["netflix", "spotify", "подписка"],
    "покупки": ["магазин", "одежда", "шоппинг", "покупка"]
}


def detect_category(word):
    """Определяет категорию по слову"""
    word_lower = word.lower()

    # Ищем точное совпадение
    for cat, words in categories.items():
        for w in words:
            if w in word_lower:
                return cat

    # Если не нашли - возвращаем первое слово как категорию
    first_word = word_lower.split()[0]
    return first_word if first_word else "другое"
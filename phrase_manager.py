"""
Модуль работы с фразами:
- загрузка набора фраз из JSON
- выдача случайной фразы под текущий язык
- перечень доступных языков
"""

import json
import random
import logging
from settings import PHRASES_FILE, MAX_LANGUAGES

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PhraseManagerError(Exception):
    """Исключение для ошибок PhraseManager."""
    pass

class PhraseManager:
    def __init__(self):
        self.data = {}
        self.load_phrases()

    def load_phrases(self):
        """Загрузить фразы из JSON-файла."""
        try:
            with open(PHRASES_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            logger.info("Фразы загружены из %s", PHRASES_FILE)
        except FileNotFoundError:
            logger.error("phrases.json не найден: %s", PHRASES_FILE)
            raise PhraseManagerError("Не найден файл фраз")
        except json.JSONDecodeError as e:
            logger.error("Ошибка разбора JSON: %s", e)
            raise PhraseManagerError("Неверный формат phrases.json")

        # Проверка максимально допустимого числа языков
        if len(self.data) > MAX_LANGUAGES:
            logger.warning("Больше %d языков, обрезаем список", MAX_LANGUAGES)
            # Оставляем только первые MAX_LANGUAGES языков
            keys = list(self.data.keys())[:MAX_LANGUAGES]
            self.data = {k: self.data[k] for k in keys}

    def get_random(self, lang_code: str) -> str:
        """
        Вернуть случайную фразу для заданного кода языка.
        Если язык не найден — вернуть пустую строку и залогировать.
        """
        if lang_code not in self.data:
            logger.warning("Язык %s отсутствует в фразах", lang_code)
            return ""
        phrases = self.data[lang_code]
        if not phrases:
            logger.warning("Список фраз для %s пуст", lang_code)
            return ""
        choice = random.choice(phrases)
        logger.debug("Выбрана фраза [%s] для языка %s", choice, lang_code)
        return choice

    def list_languages(self) -> list:
        """Вернуть список доступных языков."""
        langs = list(self.data.keys())
        logger.debug("Доступные языки: %s", langs)
        return langs

    def reload(self):
        """Перезагрузить фразы из файла."""
        logger.info("Перезагрузка фраз")
        self.load_phrases()

# Самотестирование модуля
if __name__ == "__main__":
    pm = PhraseManager()
    print("Доступные языки:", pm.list_languages())
    for lang in pm.list_languages():
        print(lang, "->", pm.get_random(lang))

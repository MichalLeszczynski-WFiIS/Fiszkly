from django.test import TestCase
from words.utils import (
    Translator,
    MockTranslator,
    get_dictionary_entry,
    save_flashcard,
    save_categorized_flashcard,
)
from words.models import Flashcard, FlashcardGroup


class MockTranslatorTest(TestCase):
    def setUp(self):
        self.translator = MockTranslator("mock")

    def test_mock_translate(self):
        words = self.translator.translate(["test1", "test2"], "en", "pl")
        self.assertIsNotNone(words)
        for word in words:
            self.assertEqual(word["translation"], f"t_{word['original']}")


class DictionaryEntryTest(TestCase):
    def test_dictionary_entry(self):
        entry = get_dictionary_entry("dog")[0]["meaning"]
        self.assertIn("noun", entry)
        self.assertIn("transitive verb", entry)


class SaveFlashcardTest(TestCase):
    def test_save_flashcard(self):
        word = {
            "original": "test",
            "translation": "t_test",
            "sl": "en",
            "tl": "pl",
            "dictionary_entry": r"[example_dictionary_entry]",
            "author": None,
        }
        save_flashcard(word)
        flashcard = Flashcard.objects.get(original_word="test")
        self.assertEqual(flashcard.translated_word, "t_test")
        self.assertEqual(flashcard.original_language, "en")
        self.assertEqual(flashcard.translated_language, "pl")
        self.assertEqual(flashcard.author, None)

    def test_save_categorized_flashcard(self):
        word = {
            "original": "test",
            "translation": "t_test",
            "sl": "en",
            "tl": "pl",
            "dictionary_entry": r"[example_dictionary_entry]",
            "author": None,
        }
        category = FlashcardGroup(name="TestCategory")
        category.save()
        save_categorized_flashcard(word, category)

        flashcard = Flashcard.objects.filter(flashcardgroup__name="TestCategory")[0]
        self.assertEqual(flashcard.translated_word, "t_test")
        self.assertEqual(flashcard.original_language, "en")
        self.assertEqual(flashcard.translated_language, "pl")
        self.assertEqual(flashcard.author, None)


class BrowseWordsViewTest(TestCase):
    def test_browse_words(self):
        pass


class VerifyWordsViewTest(TestCase):
    def test_verify_words(self):
        pass

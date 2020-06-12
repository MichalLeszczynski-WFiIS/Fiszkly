from django.test import TestCase
from words.utils import (
    Translator,
    MockTranslator,
    get_dictionary_entry,
    save_flashcard,
    save_categorized_flashcard,
)
from words.models import Flashcard, FlashcardGroup
from fiszkly.tests_common import HaveFlashcardTestTemplate, LoggedInTestTemplate

WORD = {
    "original": "test",
    "translation": "t_test",
    "sl": "en",
    "tl": "pl",
    "dictionary_entry": r"[example_dictionary_entry]",
    "author": None,
}


class MockTranslatorTest(TestCase):
    def setUp(self):
        self.translator = MockTranslator("mock")

    def test_mock_translate(self):
        words = self.translator.translate(["test1", "test2"], "en", "pl")
        self.assertIsNotNone(words)
        for word in words:
            self.assertEqual(word["translation"], f"t_{word['original']}")

    def test_empty_mock_translate(self):
        words = self.translator.translate([], "en", "pl")
        self.assertEqual(words, [])


class TranslatorTest(TestCase):
    def setUp(self):
        self.translator = Translator("mock")

    def test_empty_translate(self):
        words = self.translator.translate([], "en", "pl")
        self.assertEqual(words, [])


class SaveFlashcardTest(TestCase):
    def test_save_flashcard(self):
        save_flashcard(WORD)
        flashcard = Flashcard.objects.get(original_word="test")
        self.assertEqual(flashcard.translated_word, "t_test")
        self.assertEqual(flashcard.original_language, "en")
        self.assertEqual(flashcard.translated_language, "pl")
        self.assertEqual(flashcard.author, None)

    def test_save_categorized_flashcard(self):
        category = FlashcardGroup(name="TestCategory")
        category.save()
        save_categorized_flashcard(WORD, category)

        flashcard = Flashcard.objects.filter(flashcardgroup__name="TestCategory")[0]
        self.assertEqual(flashcard.translated_word, "t_test")
        self.assertEqual(flashcard.original_language, "en")
        self.assertEqual(flashcard.translated_language, "pl")
        self.assertEqual(flashcard.author, None)


class BrowseGroupsViewTest(HaveFlashcardTestTemplate):
    def test_browse_words_specific(self):
        category = FlashcardGroup(name="TestCategory")
        category.save()
        response = self.client.post("/words", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("browse_groups.html")
        self.assertTrue(len(response.context["flashcard_groups"]) > 0)


class BrowseWordsViewTest(HaveFlashcardTestTemplate):
    def test_browse_words_all(self):
        response = self.client.post("/words/browse-words/all", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("browse_words.html")
        self.assertEqual(response.context["category"], "all")
        self.assertTrue(len(response.context["words"]) > 0)

    def test_browse_words_user(self):
        response = self.client.post("/words/browse-words/user", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("browse_words.html")
        self.assertEqual(response.context["category"], "user")
        self.assertTrue(len(response.context["words"]) == 0)

    def test_browse_words_specific(self):
        category = FlashcardGroup(name="TestCategory")
        category.save()
        save_categorized_flashcard(WORD, category)
        response = self.client.post("/words/browse-words/TestCategory", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("browse_words.html")
        self.assertEqual(response.context["category"], "TestCategory")
        self.assertTrue(len(response.context["words"]) > 0)


class VerifyWordsViewTest(LoggedInTestTemplate):
    def test_verify_words(self):
        session = self.client.session
        session["translated_words"] = [
            WORD,
        ]
        session.save()
        response = self.client.post(
            "/words/verify-words/", {"confirmed_words": [WORD["original"]]}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("verift_words.html")
        self.assertIsNotNone(response.context["flashcard_groups"])
        self.assertIsNotNone(response.context["messages"])
        self.assertIsNotNone(response.context["user_count"])

    def test_verify_words_category(self):
        session = self.client.session
        session["translated_words"] = [
            WORD,
        ]
        session.save()
        response = self.client.post(
            "/words/verify-words/",
            {"confirmed_words": [WORD["original"]], "category": "test"},
            follow=True,
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("verift_words.html")
        self.assertIsNotNone(response.context["flashcard_groups"])
        self.assertIsNotNone(response.context["messages"])
        self.assertIsNotNone(response.context["user_count"])

    def test_verify_words_get(self):
        session = self.client.session
        session["translated_words"] = [
            WORD,
        ]
        session.save()
        response = self.client.get("/words/verify-words/", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("verift_words.html")
        self.assertIsNotNone(response.context["translated_words"])
        self.assertIsNotNone(response.context["messages"])


class UploadWordsViewTest(LoggedInTestTemplate):
    def test_upload_words_form(self):
        response = self.client.post(
            "/words/upload-words/", {"language": ["pl"], "field": ["test"]}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("upload_words.html")
        self.assertIsNotNone(response.context["translated_words"])

    def test_upload_words_get(self):
        response = self.client.get("/words/upload-words", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("upload_words.html")
        self.assertIsNotNone(response.context["form"])

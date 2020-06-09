# Generated by Django 3.0.5 on 2020-05-31 22:10

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
from words.models import Flashcard, FlashcardGroup


def create_initial_data(apps, schema_editor):
    # groups
    fruits = FlashcardGroup(name="Fruits")
    fruits.save()
    adjectives = FlashcardGroup(name="Adjectives")
    adjectives.save()
    programming = FlashcardGroup(name="Programming")
    programming.save()

    # fruits
    fruits.flashcards.create(
        original_word="apricot",
        translated_word="morela",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    fruits.flashcards.create(
        original_word="blackcurrant",
        translated_word="czarna porzeczka",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    fruits.flashcards.create(
        original_word="peach",
        translated_word="brzoskwinia",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    fruits.flashcards.create(
        original_word="quince",
        translated_word="pigwa",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    fruits.flashcards.create(
        original_word="plum",
        translated_word="śliwka",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )

    # adjectives
    adjectives.flashcards.create(
        original_word="succinct",
        translated_word="zwięzły",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    adjectives.flashcards.create(
        original_word="viable",
        translated_word="wykonalny",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    adjectives.flashcards.create(
        original_word="crude",
        translated_word="surowy",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    adjectives.flashcards.create(
        original_word="inordinate",
        translated_word="nadmierny",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    adjectives.flashcards.create(
        original_word="sullen",
        translated_word="ponury",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )

    # programming
    programming.flashcards.create(
        original_word="concurrency",
        translated_word="współbieżność",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    programming.flashcards.create(
        original_word="stack",
        translated_word="stos",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    programming.flashcards.create(
        original_word="heap",
        translated_word="sterta",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    programming.flashcards.create(
        original_word="tuple",
        translated_word="krotka",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )
    programming.flashcards.create(
        original_word="closure",
        translated_word="domknięcie",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )

    # other
    Flashcard.objects.create(
        original_word="encouragement",
        translated_word="zachęta",
        original_language="en",
        translated_language="pl",
        dictionary_entry=r"[example_dictionary_entry]",
    )


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Flashcard",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("original_word", models.CharField(max_length=50)),
                ("translated_word", models.CharField(max_length=100)),
                ("original_language", models.CharField(max_length=2)),
                ("translated_language", models.CharField(max_length=2)),
                ("dictionary_entry", django.contrib.postgres.fields.jsonb.JSONField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FlashcardGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("flashcards", models.ManyToManyField(to="words.Flashcard")),
            ],
        ),
        migrations.RunPython(create_initial_data),
    ]

# Generated by Django 3.0.5 on 2020-05-11 17:05

from django.db import migrations

def create_flashcards(apps, schema_editor):
    Flashcard = apps.get_model("learning", "Flashcard")
    Flashcard.objects.create(translated=["miły"], original="nice", original_language="en")
    Flashcard.objects.create(translated=["hojny"], original="generous", original_language="en")
    Flashcard.objects.create(translated=["możliwe"], original="possible", original_language="en")
    Flashcard.objects.create(translated=["niezależny"], original="independent", original_language="en")
    Flashcard.objects.create(translated=["ciekawy"], original="curious", original_language="en")

class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]


    operations = [migrations.RunPython(create_flashcards)]

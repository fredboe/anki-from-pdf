import pathlib
import random
from typing import List

import genanki

note_fields = [
    {'name': 'Question'},
    {'name': 'Answer'},
]
note_template = {
    'name': 'Card',
    'qfmt': '{{Question}}',
    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
}

css_style = """
      .card {
       font-family: arial;
       font-size: 20px;
       text-align: center;
       color: black;
       background-color: white;
      }
      """


def create_deck(name: str, questions: List[str], answers: List[str]) -> genanki.Deck:
    """
    Creates a new anki deck with the specified name and the questions and answers as the flashcards.

    Parameters:
        name (str): The name of the generated deck
        questions (List[str]): The list of questions that are displayed at the front of the flashcards
        answers (List[str]): The list of answers that are displayed at the back of the flashcards
    """
    deck_id = random.randint(0, 2 ** 63 - 1)
    deck = genanki.Deck(deck_id=deck_id, name=name)
    model = genanki.Model(model_id=deck_id, name=name, fields=note_fields, templates=[note_template], css=css_style)

    for question, answer in zip(questions, answers):
        note = genanki.Note(
            model=model,
            fields=[question, answer]
        )
        deck.add_note(note)

    return deck


def create_package_from_deck(deck: genanki.Deck, image_paths: List[pathlib.Path]) -> genanki.Package:
    """
    Creates a new anki package from the specified deck and the specified media files.
    The package can later be imported in the anki application.

    Parameters:
        deck (genanki.Deck): The deck to create the package from
        image_paths (List[Path]): The paths to all the media files
    """
    package = genanki.Package(deck)
    package.media_files = image_paths
    return package

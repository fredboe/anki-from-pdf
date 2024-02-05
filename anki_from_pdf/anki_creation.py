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
    package = genanki.Package(deck)
    package.media_files = image_paths
    return package

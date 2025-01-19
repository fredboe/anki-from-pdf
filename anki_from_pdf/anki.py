import random
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz
import genanki


@dataclass
class CardWithPdf:
    model = genanki.Model(
        random.randint(1, 2 ** 32 - 1),
        'Simple Model with Media',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'}
        ],
        templates=[
            {
                'name': 'Card',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
        css="""
            .card {
                font-family: arial;
                font-size: 20px;
                text-align: center;
                color: black;
                background-color: white;
            }
            """
    )

    question: str
    answer: fitz.Document | str

    def mediafy(self, parent: Path, model=None) -> (List[Path], genanki.Note):  # (Media, Note)
        _id = random.randint(1, 2 ** 32 - 1)

        parent.mkdir(parents=True, exist_ok=True)
        model = model if model is not None else CardWithPdf.model
        if isinstance(self.answer, fitz.Document):
            medias = []
            for i in range(len(self.answer)):
                page = self.answer[i]
                scale_factor = 1080 / page.rect.width
                image = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))

                image_path = parent / f"slide_image_{_id}_{i}.png"
                medias.append(image_path)
                image.save(image_path)
            answer = "<br>".join([f"<img src='{image_path.name}'>" for image_path in medias])
        else:
            medias = []
            answer = self.answer

        return medias, genanki.Note(model=model, fields=[self.question, answer])


def create_package(name, notes: List[genanki.Note], medias: List[Path]) -> genanki.Package:
    deck = genanki.Deck(deck_id=random.randint(1, 2 ** 32 - 1), name=name)
    for note in notes:
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = medias
    return package

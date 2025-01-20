from anki_from_pdf.pdf import SlideShow
from anki_from_pdf import anki, utils

from pathlib import Path

path_to_slides = Path() / "Slides"
path_to_deck = Path() / "Anki"

slides1 = SlideShow.from_pdf(path_to_slides / "01.pdf")
slides2 = SlideShow.from_pdf(path_to_slides / "02.pdf")

cards = [
    slides1.take(0, 10).into_card(),
    slides2.take(9, 12).into_card(question="What is x^2?"),
]
cards_with_media = [card.mediafy(parent=path_to_deck) for card in cards]

medias, cards = utils.unzip(cards_with_media)
medias = utils.flatten(medias)

name = "Deck_Name"
anki.create_package(name, cards, medias).write_to_file(path_to_deck / f"{name}.apkg")

import argparse
import json
from pathlib import Path

from anki_from_pdf import utils
from anki_from_pdf.anki import create_package
from anki_from_pdf.description import DeckDescription
from anki_from_pdf.pdf import SlideShow


def main(args):
    with Path(args.description_file).open('r') as file:
        deck_description = DeckDescription(**json.load(file))

    path_to_deck = Path() / "deck"
    slide_shows = {pdf_id: SlideShow.from_pdf(path) for pdf_id, path in deck_description.pdfs.items()}

    cards_with_media = []
    for card_desc in deck_description.notes:
        slides = slide_shows[card_desc.pdf_id]
        card = slides.take(card_desc.pages[0], card_desc.pages[1]).into_card(question=card_desc.question)
        cards_with_media.append(card.mediafy(parent=path_to_deck))

    medias, cards = utils.unzip(cards_with_media)
    medias = utils.flatten(medias)

    package = create_package(args.name, cards, medias)
    package.write_to_file(path_to_deck / f"{args.name}.apkg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str,
                        help="Specify the name of the deck (type: str).")
    parser.add_argument("-d", "--description", type=str,
                        help="Specify the file containing the description of the deck (in json) (type: str).")
    args = parser.parse_args()
    main(args)

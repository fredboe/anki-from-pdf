import argparse
import json
import pathlib

from . import anki_creation
from .deck_description import DeckDescription


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str,
                        help="Specify the name of the deck (type: str).")
    parser.add_argument("--description_path", type=str,
                        help="Specify the path to the description of the deck (in json) (type: str).")
    args = parser.parse_args()

    with pathlib.Path(args.description_path).open('r') as file:
        deck_description = DeckDescription(**json.load(file))

    deck_description.save_pdfs_as_images()
    questions = deck_description.get_questions()
    answer_images = deck_description.get_answers()
    answers_strs = ["<br>".join([f"<img src='{image_path.name}'>" for image_path in images]) for images in
                    answer_images]

    deck = anki_creation.create_deck(args.name, questions, answers_strs)

    all_image_paths = [image_path for image_paths in answer_images for image_path in image_paths]
    all_existing_image_paths = [image_path for image_path in all_image_paths if image_path.exists()]
    package = anki_creation.create_package_from_deck(deck, all_existing_image_paths)

    (pathlib.Path() / "deck").mkdir(parents=True, exist_ok=True)
    package.write_to_file(pathlib.Path() / "deck" / f"{args.name}.apkg")


if __name__ == '__main__':
    main()

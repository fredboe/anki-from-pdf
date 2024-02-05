import pathlib
from typing import List, Dict, Tuple

from pdf2image import convert_from_path
from pydantic import BaseModel

from . import utils


class Note(BaseModel):
    """
    Structure of a note (flashcard).

    The structure consists of the question to ask on the front side. And the pages of a pdf that form the back side
    of the flashcard (as images).

    Attributes:
        question (str | None): The question to ask on the front side
        pdf_id (str): The id (key) of the pdf
        pages (Tuple[int, int]): The pages that form the back side, described as a range (the upper number is included)
    """
    question: str | None
    pdf_id: str
    pages: Tuple[int, int]


class DeckDescription(BaseModel):
    """
    Structure of a deck.

    The structure consists of the pdfs that are used to generate the questions and answers, as well as a list of the
    flashcards.

    Attributes:
        pdfs (Dict[str, Path]): The mapping from the pdf ids to the concrete files
        notes (List[Note]): The list of notes that form the flashcards
    """
    pdfs: Dict[str, pathlib.Path]
    notes: List[Note]

    def save_pdfs_as_images(self):
        """
        Split the pdfs into its pages and save each page as an image.
        The filepath is determined by the function `gen_image_path`.
        """
        for pdf_path in self.pdfs.values():
            images = convert_from_path(pdf_path)
            for page_num, image in enumerate(images):
                image_path = gen_image_path(pdf_path.stem, page_num)
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(image_path, "JPEG")

    def get_questions(self) -> List[str]:
        """
        Returns:
            A list of all the questions for each note (front side).
            If there is no question specified, then the question is automatically generated from the first page
            (largest font size).
        """
        questions = []
        for note in self.notes:
            question = note.question if note.question is not None else utils.extract_title(
                self.pdfs.get(note.pdf_id), note.pages[0])
            questions.append(question)
        return questions

    def get_answers(self) -> List[List[pathlib.Path]]:
        """
        Returns:
             A list of all the answers for each note (back side).
             One answer is a list of images that should be displayed.
        """
        answers = []
        for note in self.notes:
            pdf_name = self.pdfs.get(note.pdf_id).stem
            answer_images = [gen_image_path(pdf_name, page_num) for page_num in
                             range(note.pages[0], note.pages[1] + 1)]
            answers.append(answer_images)
        return answers


def gen_image_path(pdf_name: str, page_num: int) -> pathlib.Path:
    """
    Generates the path where to store an image.

    Returns:
        The path where to store the image (working_directory/deck/slide_image_{pdf_name}_{page_num}.jpg).
    """
    return pathlib.Path() / "deck" / f"slide_image_{pdf_name}_{page_num}.jpg"

from pathlib import Path
from typing import Tuple, Dict, List

from pydantic import BaseModel


class CardDescription(BaseModel):
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
    pdfs: Dict[str, Path]
    notes: List[CardDescription]

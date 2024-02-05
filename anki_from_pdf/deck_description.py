import pathlib
from typing import List, Dict, Tuple

from pdf2image import convert_from_path
from pydantic import BaseModel

from . import utils


class Note(BaseModel):
    question: str | None
    pdf_id: str
    pages: Tuple[int, int]


class DeckDescription(BaseModel):
    pdfs: Dict[str, pathlib.Path]
    notes: List[Note]

    def save_pdfs_as_images(self):
        for pdf_path in self.pdfs.values():
            images = convert_from_path(pdf_path)
            for page_num, image in enumerate(images):
                image_path = gen_image_path(pdf_path.stem, page_num)
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(image_path, "JPEG")

    def get_questions(self) -> List[str]:
        questions = []
        for note in self.notes:
            question = note.question if note.question is not None else utils.extract_title(
                self.pdfs.get(note.pdf_id), note.pages[0])
            questions.append(question)
        return questions

    def get_answers(self) -> List[List[pathlib.Path]]:
        answers = []
        for note in self.notes:
            pdf_name = self.pdfs.get(note.pdf_id).stem
            answer_images = [gen_image_path(pdf_name, page_num) for page_num in
                             range(note.pages[0], note.pages[1] + 1)]
            answers.append(answer_images)
        return answers


def gen_image_path(pdf_name: str, page_num: int) -> pathlib.Path:
    return pathlib.Path() / "deck" / f"slide_image_{pdf_name}_{page_num}.jpg"

import random
import re
from pathlib import Path
from typing import List, Tuple

import fitz
from bs4 import BeautifulSoup

from anki_from_pdf.anki import CardWithPdf


class SlideShow:
    _id: int
    document: fitz.Document

    def __init__(self, document: fitz.Document) -> None:
        self._id = random.randint(1, 2 ** 32 - 1)
        self.document = document

    def take(self, start: int = 0, end: int = -1) -> "SlideShow":
        return self.take_n([(start, end)])[0]

    def take_n(self, pages: List[Tuple[int, int]]) -> List["SlideShow"]:
        slides_s = []
        for start, end in pages:
            new_document = fitz.open()
            new_document.insert_pdf(self.document, from_page=start, to_page=end)
            slides_s.append(SlideShow(new_document))
        return slides_s

    def into_card(self, question: str | None = None, answer: str | None = None) -> CardWithPdf:
        if answer is None:
            answer = self.document
        if question is None:
            question = _extract_title_from_page(self.document.load_page(0))
        return CardWithPdf(question=question, answer=answer)

    @staticmethod
    def from_pdf(path: Path):
        return SlideShow(fitz.open(path))


def _extract_title_from_page(page: fitz.Page) -> str:
    """
    Extracts the potential title of a page within a PDF file,
    utilizing the largest font size present on the page as a heuristic.

    Parameters:
        page (Page): The page to find the title for

    Returns:
        A string representing the extracted title of the page, based on the heuristic of maximum font size.
        If no title was found, then "No title found" is returned.
    """

    def font_size_of_span(_span) -> float:
        font_size_match = re.search('font-size:\s*(\d+\.\d+)', _span['style'])
        if font_size_match:
            return float(font_size_match.group(1))
        else:
            return 0.0

    html_str = page.get_text("HTML")
    spans = BeautifulSoup(html_str, "html.parser").find_all("span", style=True)

    if spans:
        max_font_size = max(font_size_of_span(span) for span in spans)
        max_size_texts = [span.text for span in spans if font_size_of_span(span) == max_font_size]
        return " ".join(max_size_texts)
    else:
        return "No title found"

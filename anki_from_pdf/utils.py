import pathlib
import re

import fitz
from bs4 import BeautifulSoup


def extract_title_from_page(page: fitz.Page) -> str:
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
    max_font_size = max([font_size_of_span(span) for span in spans])
    spans_with_max_font = [span for span in spans if font_size_of_span(span) == max_font_size]
    if spans_with_max_font:
        return "<br>".join([str(span) for span in spans_with_max_font])
    else:
        return "No title found"


def extract_title(pdf_path: pathlib.Path, page_number: int) -> str:
    """
    Extracts the potential title of a page within a PDF file,
    utilizing the largest font size present on the page as a heuristic.

    Parameters:
        pdf_path (Path): The path to the pdf file
        page_number (int): The page number to find the title for

    Returns:
        A string representing the extracted title of the page, based on the heuristic of maximum font size.
        If no title was found, then "No title found" is returned.
    """
    document = fitz.open(pdf_path)
    try:
        return extract_title_from_page(document.load_page(page_number))
    except IndexError:
        return "No title found"

# anki-from-pdf

This project automates the creation of Anki decks from PDF files (specifically presentations).
Users can specify PDF documents and define how to split these documents into question-and-answer pairs for flashcards.
Installation

- Clone the repository: Start by cloning this repository to your local machine.
- Install dependencies: Navigate to the project directory and run ``poetry install`` to set up the necessary
  environment.

### Usage

Launch the deck generator by running: ``python3 -m anki_from_pdf --parameters=values``. To explore the full range of
command-line options, including how to specify the deck name and the path to the deck description file, use ``python3 -m
anki_from_pdf --help``. For instance, you might use:

```
python3 -m anki_from_pdf --name="Analysis 1" --description_file=deck_description.json
```

#### Deck Description File

The deck description file, formatted as JSON, dictates the organization of PDF content into Anki cards. Here's an
example (`example.json`):

```json
{
  "pdfs": {
    "presentation1": "path/to/pdf1.pdf",
    "presentation2": "path/to/pdf2.pdf"
  },
  "notes": [
    {
      "question": "How old are you?",
      "pdf_id": "presentation1",
      "pages": [
        0,
        10
      ]
    },
    {
      "question": null,
      "pdf_id": "presentation2",
      "pages": [
        11,
        19
      ]
    }
  ]
}
```

This configuration generates an Anki deck with two cards. The first card includes a specific question with answers
derived from the designated pages ``presentation1``. The second card generates its question automatically, aiming to
pinpoint the page's title by selecting the section with the largest font size as the likely title. The answer includes
the content from pages 11 to 19 of the ``presentation2``.

## License

MIT License
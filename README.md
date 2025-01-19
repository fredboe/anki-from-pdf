from anki_from_pdf.pdf import SlideShow

# anki-from-pdf

This project automates the creation of Anki decks from PDF files (specifically presentations).
Users can specify PDF documents and define how to split these documents into question-and-answer pairs for flashcards.

### Installation

- Clone the repository: Start by cloning this repository to your local machine.
- Install dependencies: Navigate to the project directory and run ``poetry install`` to set up the necessary
  environment.
- Build the package: Run ``poetry build`` to build the package.
- Install the package: Lastly you need to install the package with ``pip install dist/*.whl``.

### Usage

There are to options to use this package. The first one is to use it directly inside of python.
And the second option is to launch the main of the package and specify a json that describes the anki deck.

#### Using inside of python

For a complete view, have a look at the documentation inside the code.
Below I present a little example:

````python
# Import a pdf
slide_show = SlideShow.from_pdf(path_to_pdf)

# Specify an interval of the interesting pages
# And create an anki card that consists of the selected pages as the answer
card = silde_show.take(start=9, end=11).into_card()

# Save the media of the card (the pdf) on the disk and obtain a genanki.Note
media, note = card.mediafy(parent=path_to_deck)
deck.add_note(note)

package = genanki.Package(deck)
package.media_files = [media]
````

#### Using a Deck Description File

Launch the deck generator by running: ``python3 -m anki_from_pdf --parameters=values``. To explore the full range of
command-line options, including how to specify the deck name and the path to the deck description file, use ``python3 -m
anki_from_pdf --help``. For instance, you might use:

```
python3 -m anki_from_pdf --name="Analysis 1" --description_file=deck_description.json
```

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
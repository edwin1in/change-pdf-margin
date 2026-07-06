from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from gui import *
import warnings
import argparse
import sys

parser = argparse.ArgumentParser(
    prog="main.py", description="add margins to PDF file(s)"
)
parser.add_argument("--path", type=str, default="", help="PDF file path")
parser.add_argument("--lmargin", type=float, default=0, help="set left margin size")
parser.add_argument("--rmargin", type=float, default=0, help="set right margin size")
parser.add_argument("--tmargin", type=float, default=0, help="set top margin size")
parser.add_argument("--bmargin", type=float, default=0, help="set bottom margin size")
parser.add_argument(
    "--unit",
    type=str,
    default="px",
    choices=["px", "in", "cm", "mm"],
    help="set margin unit",
)
parser.add_argument("--output", type=str, help="file name of output")


def add_margin(
    pdfpath: str = "",
    lmargin: int = 0,
    rmargin: int = 0,
    tmargin: int = 0,
    bmargin: int = 0,
    output: str = "",
) -> None:
    try:
        images = convert_from_path(pdfpath)
    except FileNotFoundError:
        raise FileNotFoundError("PDF not found")
    except PDFInfoNotInstalledError:
        raise RuntimeError("Poppler is not installed or not in PATH")
    except PDFPageCountError:
        raise ValueError("Could not read number of pages in PDF")
    except PDFSyntaxError:
        raise ValueError("PDF is corrupted or invalid")

    if not images:
        raise ValueError("PDF contains no pages.")

    pdf_width = images[0].width
    pdf_height = images[0].height

    lmargin, rmargin, tmargin, bmargin = [
        max(0, m) for m in (lmargin, rmargin, tmargin, bmargin)
    ]

    c = canvas.Canvas(
        f"{output}.pdf",
        pagesize=(pdf_width + (lmargin + rmargin), pdf_height + (tmargin + bmargin)),
    )
    for img in images:
        # (0,0) origin point at the lower left corner of the page
        # Furthermore the first coordinate x goes to the right and the second coordinate y goes up, by default.
        c.drawImage(
            ImageReader(img), lmargin, bmargin, width=pdf_width, height=pdf_height
        )
        c.showPage()
    c.save()


def units_to_px(
    unit: str, margins: tuple[float, float, float, float]
) -> tuple[float, float, float, float]:
    ppi = 96

    factor = {"px": 1, "in": ppi, "cm": ppi / 2.54, "mm": ppi / 25.4}.get(unit)

    if factor is None:
        warnings.warn(
            f"Unknown unit '{unit}'. No conversion applied; using raw pixel values.",
            stacklevel=2,
        )
        return margins

    return tuple(x * factor for x in margins)


def main():
    args = parser.parse_args()

    if len(sys.argv) == 1:
        app = QApplication([])
        window = Window()
        window.show()
        app.exec()
    else:
        margins = units_to_px(
            args.unit, (args.lmargin, args.rmargin, args.tmargin, args.bmargin)
        )

        if args.output is None:
            args.output = args.path.rsplit(".", 1)[0]
        add_margin(args.path, *margins, args.output)


if __name__ == "__main__":
    main()

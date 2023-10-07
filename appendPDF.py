from reportlab.lib.units import cm
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.units import cm
from os import getcwd

PATH = getcwd()


class AppendPage:
    def __init__(self, original_pdf, next_pdf):
        self.original_pdf = PdfReader(open(original_pdf, "rb"))
        self.next_pdf = PdfReader(open(next_pdf, "rb"))
        self.output = PdfWriter()

    def merge(self):
        for i, page in enumerate(self.original_pdf.pages):
            self.output.add_page(self.original_pdf.pages[i])
        for i, page in enumerate(self.next_pdf.pages):
            self.output.add_page(self.next_pdf.pages[i])

    def generate(self, output_path):
        outputStream = open(output_path, "wb")
        self.output.write(outputStream)
        outputStream.close()


if __name__ == '__main__':
    original = f"{PATH}\\dist\\test.pdf"
    next_file = f"{PATH}\\dist\\CL.pdf"
    gen = AppendPage(original, next_file)
    gen.merge()
    gen.generate(f"{PATH}/dist/final.pdf")

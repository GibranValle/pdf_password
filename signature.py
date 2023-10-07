from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen.canvas import Canvas
import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter

PATH = os.getcwd()


class AddTextToFile:
    def __init__(self, template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.output = PdfWriter()
        self.packet = io.BytesIO()
        self.canvas1 = Canvas(self.packet, pagesize=letter)

    def addText(self, text, point):
        self.canvas1.drawString(point[0], point[1], text)

    def add_signature_OS(self, image, point, width=120, height=120):
        self.canvas1.drawImage(image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def add_signature_acta(self, image, point, width=120, height=120):
        self.canvas1.showPage()
        self.canvas1.drawImage(image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def merge(self):
        self.canvas1.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        for index, page in enumerate(self.template_pdf.pages):
            result = result_pdf.pages[index]
            page.merge_page(result)
            self.output.add_page(self.template_pdf.pages[index])

    def generate(self, dest):
        outputStream = open(dest, "wb")
        self.output.write(outputStream)
        outputStream.close()


def signature_install(file_path, output_path):
    image = f"{PATH}\\dist\\signature.png"
    gen = AddTextToFile(file_path)
    gen.add_signature_OS(image, (2.5 * cm, 0 * cm), 3.5 * cm, 1.5 * cm)
    gen.add_signature_acta(image, (9 * cm, 1.5 * cm), 3.5 * cm, 1.5 * cm)
    gen.merge()
    gen.generate(output_path)
    return output_path


def signature_preventive(file_path, output_path):
    image = f"{PATH}\\dist\\signature.png"
    gen = AddTextToFile(file_path)
    gen.add_signature_OS(image, (2.5 * cm, 0 * cm), 3.5 * cm, 1.5 * cm)
    gen.merge()
    gen.generate(output_path)
    return output_path


if __name__ == '__main__':
    image = f"{PATH}\\dist\\signature.png"
    gen = AddTextToFile(f"{PATH}\\dist\\test.pdf")
    # gen.addText("Hello!", (100, 200))
    # gen.addText("PDF!", (100, 300))
    gen.add_signature_OS(image, (2.5 * cm, 0 * cm), 3.5 * cm, 1.5 * cm)
    gen.add_signature_acta(image, (9 * cm, 1.5 * cm), 3.5 * cm, 1.5 * cm)
    gen.merge()
    gen.generate(f"{PATH}/dist/Output.pdf")

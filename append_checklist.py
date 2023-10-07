from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen.canvas import Canvas
import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter

PATH = os.getcwd()
DETAILS_Y = 19.15 * cm
DETAILS_X_A = 4 * cm
DETAILS_X_B = 16.25 * cm
DETAILS_HEIGHT = 0.7 * cm

STATUS_X = 11 * cm
STAYUS_Y = 15.95 * cm
STAYUS_Y1 = 6.4 * cm
STAYUS_Y2 = 4.75 * cm
STATUS_HEIGHT = 0.4625 * cm

OBS_X = 13 * cm

is_tomo = False
is_bpy = False
is_dirty = True


class AppendCheckList:
    def __init__(self, original_path, template_path):
        self.original_pdf = PdfReader(open(original_path, "rb"))
        self.template_pdf = PdfReader(open(template_path, "rb"))
        self.output = PdfWriter()
        self.packet = io.BytesIO()
        self.canvas1 = Canvas(self.packet, pagesize=letter)

    def setColor(self, color='blue', size=12):
        self.canvas1.setFillColor(color)
        self.canvas1.setStrokeColor(color)
        self.canvas1.setFont("Helvetica-Bold", size)

    def addText(self, text, point):
        self.canvas1.drawString(point[0], point[1], text)

    def merge(self):
        self.canvas1.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]
        self.template_pdf.pages[0].merge_page(result)
        for i, page in enumerate(self.original_pdf.pages):
            self.output.add_page(self.original_pdf.pages[i])
        self.output.add_page(self.template_pdf.pages[0])

    def generate(self, dest):
        outputStream = open(dest, "wb")
        self.output.write(outputStream)
        outputStream.close()


def append_checklist(original_path, template_path=f"{PATH}\\dist\\Innovality_CL.pdf", fields={}, is_clean=True):
    gen = AppendCheckList(original_path, template_path)
    gen.setColor()
    gen.addText("15002244", (DETAILS_X_A, DETAILS_Y))
    gen.addText("HOSPITAL NAME", (DETAILS_X_B, DETAILS_Y))
    gen.addText("30.10.2023", (DETAILS_X_A, DETAILS_Y - DETAILS_HEIGHT))
    gen.addText("TEST CITY", (DETAILS_X_B, DETAILS_Y - DETAILS_HEIGHT))
    gen.addText("Gibran Valle", (DETAILS_X_A, DETAILS_Y - DETAILS_HEIGHT * 2))

    gen.setColor('green', 9)

    for i in range(19):
        if i == 18:
            gen.setColor('red', 9)
            gen.addText("OK" if is_clean else 'REGULAR', (STATUS_X - 0.55 * cm, STAYUS_Y - STATUS_HEIGHT * i))
            gen.addText('El equipo se encontró muy sucio', (OBS_X, STAYUS_Y - STATUS_HEIGHT * i))
            gen.setColor('green', 9)
        else:
            gen.addText("OK", (STATUS_X, STAYUS_Y - STATUS_HEIGHT * i))

    for i in range(2):
        gen.addText("OK" if is_tomo else 'N/A', (STATUS_X, STAYUS_Y1 - STATUS_HEIGHT * i))

    for i in range(6):
        gen.addText("OK" if is_bpy else 'N/A', (STATUS_X, STAYUS_Y2 - STATUS_HEIGHT * i))

    # gen.addText("PDF!", (100, 300))
    gen.merge()
    gen.generate(f"{PATH}/dist/CL.pdf")

from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.constants import UserAccessPermissions
import io
from reportlab.pdfgen.canvas import Canvas
import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from classes.text_extract import text_extractor, extract_fields

PATH = os.getcwd()
PRINT = UserAccessPermissions.PRINT
EXTRACT = UserAccessPermissions.EXTRACT
# FILL_FORM_FIELDS = UserAccessPermissions.FILL_FORM_FIELDS
PRINT_TO_REPRESENTATION = UserAccessPermissions.PRINT_TO_REPRESENTATION
NEEDED = PRINT + EXTRACT + PRINT_TO_REPRESENTATION


class ModifyPDF:
    def __init__(self, template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.writer = PdfWriter()
        self.packet = io.BytesIO()
        self.canvas1 = Canvas(self.packet, pagesize=letter)
        self.signed_pdf = None

    def add_text(self, text, point):
        self.canvas1.drawString(point[0], point[1], text)

    def add_signature_service_order(self, image, point, width=120, height=120):
        self.canvas1.drawImage(image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def add_signature_minute(self, image, point, width=120, height=120):
        self.canvas1.showPage()
        self.canvas1.drawImage(image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def merge(self):
        self.canvas1.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        for index, page in enumerate(self.template_pdf.pages):
            result = result_pdf.pages[index]
            page.merge_page(result)
            self.writer.add_page(self.template_pdf.pages[index])

    def generate(self, output_path, encrypted: bool = False):
        if encrypted:
            if 'dist' in PATH:
                password_path = f"{PATH}\\password.txt"
            else:
                password_path = f"{PATH}\\dist\\password.txt"
            with open(password_path, "r") as file:
                password = file.readline()
            self.writer.encrypt(user_password='', owner_password=password, permissions_flag=NEEDED)

        with open(output_path, "wb") as file:
            self.writer.write(file)


def sign_file(file_path: str, encrypted: bool = False):
    output_path = file_path.replace('.pdf', '_sign_lock.pdf') if encrypted else file_path.replace('.pdf', '_sign.pdf')
    if 'dist' in PATH:
        image_path = f"{PATH}\\signature.png"
    else:
        image_path = f"{PATH}\\dist\\signature.png"

    text = text_extractor(file_path)
    fields = extract_fields(text)
    gen = ModifyPDF(file_path)
    if 'prev' in fields["problem"].lower():
        gen.add_signature_service_order(image_path, (2.5 * cm, 0 * cm), 3.5 * cm, 1.5 * cm)

    elif 'instal' in fields["problem"].lower():
        gen.add_signature_service_order(image_path, (2.5 * cm, 0 * cm), 3.5 * cm, 1.5 * cm)
        gen.add_signature_minute(image_path, (9 * cm, 1.5 * cm), 3.5 * cm, 1.5 * cm)

    gen.merge()
    gen.generate(output_path, encrypted)
    return output_path

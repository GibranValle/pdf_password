from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.constants import UserAccessPermissions
import io
from reportlab.pdfgen.canvas import Canvas
import os
from reportlab.lib.pagesizes import letter

PATH = os.getcwd()
PRINT = UserAccessPermissions.PRINT
EXTRACT = UserAccessPermissions.EXTRACT
# FILL_FORM_FIELDS = UserAccessPermissions.FILL_FORM_FIELDS
PRINT_TO_REPRESENTATION = UserAccessPermissions.PRINT_TO_REPRESENTATION
NEEDED = PRINT + EXTRACT + PRINT_TO_REPRESENTATION


class ModifyPDF:
    def __init__(self, file_path: str, image_path: str, password_path: str):
        self.file = file_path
        self.template_pdf = PdfReader(open(file_path, "rb"))
        self.image = image_path
        self.password = password_path
        self.writer = PdfWriter()
        self.packet = io.BytesIO()
        self.canvas1 = Canvas(self.packet, pagesize=letter)
        self.signed_pdf = None

    def add_text(self, text, point):
        self.canvas1.drawString(point[0], point[1], text)

    def add_signature_service_order(self, point, width=120, height=120):
        self.canvas1.drawImage(self.image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def add_signature_minute(self, point, width=120, height=120):
        self.canvas1.showPage()
        self.canvas1.drawImage(self.image, point[0], point[1], width=width, preserveAspectRatio=True, mask='auto')

    def merge(self):
        self.canvas1.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        for index, page in enumerate(self.template_pdf.pages):
            result = result_pdf.pages[index]
            page.merge_page(result)
            self.writer.add_page(self.template_pdf.pages[index])

    def generate(self, output_path: str = '', encrypted: bool = False):
        output = output_path
        if encrypted:
            with open(self.password, "r") as file:
                password = file.readline()
            self.writer.encrypt(user_password='', owner_password=password, permissions_flag=NEEDED)

        if len(output_path) == 0:
            if encrypted:
                output = self.file.replace('.pdf', '_sign_lock.pdf')
            else:
                output = self.file.replace('.pdf', '_sign.pdf')

        with open(output, "wb") as file:
            self.writer.write(file)
        return output

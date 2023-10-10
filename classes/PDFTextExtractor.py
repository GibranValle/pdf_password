from PyPDF2 import PdfReader
import re


class PDFTextExtractor:
    def __init__(self, file_path: str):
        self.file = file_path
        self.text = ''

    def text_extract(self):
        with open(self.file, 'rb') as file:
            print(self.file)
            pdf = PdfReader(file)
            page = pdf.pages[0]
            self.text = page.extract_text()

    def fields_extract(self):
        employee_number = re.search(r'0000(\d{4})', self.text).group(0)
        os_number = re.search(r'15(\d{6})', self.text).group(0)
        employee = re.search(rf'{employee_number}\s(.+)', self.text).group(1)
        state = re.search(r'\w+,\sM[eé]xico', self.text).group(0)
        problem = re.search(r'R\w+:\s(.+)', self.text).group(1)

        return {
            "order number": os_number,
            "employee": employee,
            "state": state,
            "problem": problem
        }

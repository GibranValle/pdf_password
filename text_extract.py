from PyPDF2 import PdfReader
import re


def text_extractor(file_path):
    with open(file_path, 'rb') as f:
        pdf = PdfReader(f)
        # get the first page
        page = pdf.pages[0]
        return page.extract_text()


def extract_fields(text):
    codes = re.findall(r'\d{8}', text)
    for code in codes:
        if '15' in code:
            os_number = code
        elif '0000' in code:
            employee_number = code
        else:
            serial = code

    employee = re.search(rf'{employee_number}\s(.+)', text).group(1)
    state = re.search(r'\w+\,\sM[eé]xico', text).group(0)
    problem = re.search(r'R\w+:\s(.+)', text).group(1)
    return {
        "order number": os_number,
        "employee": employee,
        "state": state,
        "problem": problem
    }


if __name__ == '__main__':
    from os import getcwd

    PATH = getcwd()
    test_path = f'{PATH}/dist/test.pdf'
    extracted = text_extractor(test_path)
    fields = extract_fields(extracted)
    print(fields)

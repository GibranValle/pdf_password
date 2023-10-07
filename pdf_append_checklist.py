import sys
import subprocess
from PyPDF2 import PdfWriter, PdfReader
import os
from signature import signature_install, signature_preventive
from text_extract import text_extractor, extract_fields
from append_checklist import append_checklist

PATH = os.getcwd()

PRINT = 4
EXTRACT = 16
# FILL_FORM_FIELDS = 256
FILL_FORM_FIELDS = 0
PRINT_TO_REPRESENTATION = 2048
NEEDED = PRINT + EXTRACT + FILL_FORM_FIELDS + PRINT_TO_REPRESENTATION

is_install = False
is_preventive = False
is_test = True


def pause():
    call = 'pause'
    output = subprocess.check_output(call, shell=True)
    print(output)


if __name__ == '__main__':
    with open(f"password.txt", "r") as file:
        password = file.readline()

    # get filepath of dragged file
    for i, arg in enumerate(sys.argv):
        if i == 1:
            file_path = f'{arg}'
            output_path = file_path.replace('.', '_lock.')

    if is_test:
        file_path = f'{PATH}\\dist\\test_prev.pdf'

    text = text_extractor(file_path)
    fields = extract_fields(text)
    if 'prev' in fields["problem"].lower():
        print('Preventive found')
        append_checklist(file_path, fields=fields, is_clean=True)

    pause()

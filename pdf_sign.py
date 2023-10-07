import sys
import subprocess
import os
from signature import signature_install, signature_preventive
from text_extract import text_extractor, extract_fields

PATH = os.getcwd()

PRINT = 4
EXTRACT = 16
# FILL_FORM_FIELDS = 256
FILL_FORM_FIELDS = 0
PRINT_TO_REPRESENTATION = 2048
NEEDED = PRINT + EXTRACT + FILL_FORM_FIELDS + PRINT_TO_REPRESENTATION


def pause():
    call = 'pause'
    output = subprocess.check_output(call, shell=True)
    print(output)


if __name__ == '__main__':
    with open(f"password.txt", "r") as file:
        password = file.readline()

    # get filepath of dragged file
    if len(sys.argv) == 1:
        file_path = f'{PATH}\\dist\\test_prev.pdf'
    else:
        for i, arg in enumerate(sys.argv):
            if i == 1:
                file_path = f'{arg}'

    output_path = file_path.replace('.', '_signed.')

    text = text_extractor(file_path)
    fields = extract_fields(text)
    if 'instal' in fields["problem"].lower():
        print('Installation found')
        signed_path = signature_install(file_path, output_path)
    elif 'prev' in fields["problem"].lower():
        print('Preventive found')
        signed_path = signature_preventive(file_path, output_path)

import sys
import subprocess
from PyPDF2 import PdfWriter, PdfReader

PRINT = 4
EXTRACT = 16
FILL_FORM_FIELDS = 256
PRINT_TO_REPRESENTATION = 2048
NEEDED = PRINT + EXTRACT + FILL_FORM_FIELDS + PRINT_TO_REPRESENTATION


def pause():
    call = 'pause'
    output = subprocess.check_output(call, shell=True)
    print(output)


if __name__ == '__main__':
    with open(f"password.txt", "r") as file:
        password = file.readline()

    for i, arg in enumerate(sys.argv):
        if i == 1:
            file_path = f'{arg}'
            output_path = file_path.replace('.', '_lock.')
    reader = PdfReader(f"{file_path}")
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt(user_password='', owner_password=password, permissions_flag=NEEDED)

    with open(f"{output_path}", "wb") as out_file:
        writer.write(out_file)

    pause()

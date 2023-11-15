import sys
import os
from reportlab.lib.units import cm  # type: ignore
from classes.ModifyPDF import ModifyPDF
from classes.PDFTextExtractor import PDFTextExtractor
import subprocess

PATH = os.getcwd()
ORDER_POINTS = (2.5 * cm, 0 * cm)
CHECKLIST_POINTS = (9 * cm, 14.75 * cm)
MINUTE_POINTS = (9 * cm, 1.5 * cm)
SIGNATURE_WIDTH = 3.5 * cm
SIGNATURE_WIDTH_SMALL = 2 * cm


class App:
    def __init__(self, file_path: str, image_path: str, password_path: str):
        self.file = file_path
        self.image = image_path
        self.extractor = PDFTextExtractor(self.file)
        self.extractor.text_extract()
        self.fields = self.extractor.fields_extract()
        self.password = password_path
        self.gen = None
        print(self.fields)

    def generate(self, output_path: str = "", encrypted: bool = False):
        self.gen = ModifyPDF(self.file, self.image, self.password)
        if "prev" in self.fields["problem"].lower():
            self.gen.add_signature_service_order(ORDER_POINTS, SIGNATURE_WIDTH)  # type: ignore
            self.gen.add_signature_checklist(CHECKLIST_POINTS, SIGNATURE_WIDTH_SMALL)  # type: ignore
        elif "instal" in self.fields["problem"].lower():
            self.gen.add_signature_service_order(ORDER_POINTS, SIGNATURE_WIDTH)  # type: ignore
            self.gen.add_signature_minute(MINUTE_POINTS, SIGNATURE_WIDTH)  # type: ignore
        elif "corr" in self.fields["problem"].lower():
            self.gen.add_signature_service_order(ORDER_POINTS, SIGNATURE_WIDTH)  # type: ignore
        self.gen.merge()
        return self.gen.generate(output_path, encrypted)

    @staticmethod
    def printMenu():
        print("------------------------------------------------")
        print("******* PDF sign and protect application *******")
        print("*********** FFMX by Gibran Valle ***************")
        print("------------------------------------------------")
        print("Please select and option:")
        print(" 0) quit")
        print(" 1) only sign document")
        print(" 2) sign and protect document")

    @staticmethod
    def printEnd(encrypted: bool = False):
        print("File signed and protected successfully!") if encrypted else print(
            "File signed successfully!"
        )
        print("------------------------------------------------")
        print("")


def main():
    os.system("cls")
    file_path = image_path = password_path = ""
    # get filepath if dragged file
    if not len(sys.argv) == 1:
        for i, arg in enumerate(sys.argv):
            if i == 1:
                file_path = f"{arg}"
                image_path = "signature.png"
                password_path = "password.txt"

    else:
        file_path = f"{PATH}\\dist\\test.pdf"
        image_path = f"{PATH}\\dist\\signature.png"
        password_path = f"{PATH}\\dist\\password.txt"

    app = App(file_path, image_path, password_path)

    while True:
        app.printMenu()
        selection = input("selected: ")
        if selection == "0":
            return
        elif selection == "1":
            encrypted = False
        elif selection == "2":
            encrypted = True
        else:
            os.system("cls")
            continue
        os.system("cls")
        print(f"selected: {selection}")
        print(app.generate(encrypted=encrypted))
        app.printEnd(encrypted)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("keyboard close")
    except:
        print("error")
        call = "pause"
        output = subprocess.check_output(call, shell=True)
        print(output)

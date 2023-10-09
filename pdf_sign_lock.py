import sys
import subprocess
import os
from classes.sign_protect import sign_file

PATH = os.getcwd()


def pause():
    print('File signed and protected...')
    print('Press any key to finish...')
    call = 'pause'
    output = subprocess.check_output(call, shell=True)
    print(output)


if __name__ == '__main__':
    # get filepath if dragged file
    if len(sys.argv) == 1:
        file_path = f'{PATH}\\dist\\test.pdf'
        sign_file(file_path, encrypted=True)
        print('File created successfully')

    else:
        for i, arg in enumerate(sys.argv):
            if i == 1:
                file_path = f'{arg}'
                sign_file(file_path, encrypted=True)
                pause()

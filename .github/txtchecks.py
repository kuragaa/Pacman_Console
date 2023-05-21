import os

def check_txt_files():
    txt_files = [file for file in os.listdir('.') if file.endswith('.txt')]

    for file in txt_files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 24:
                for line in lines:
                    if len(line.rstrip('\n')) > 59:
                        print(f"Line in file {file} exceeds the maximum length of 59 characters.")
                        exit(1)
                print(f"File {file} has the correct number of lines and line lengths.")
            else:
                print(f"File {file} does not have the correct number of lines.")
                exit(1)

if __name__ == '__main__':
    check_txt_files()
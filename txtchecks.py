import os

def check_txt_files():
    repo_root = os.environ['GITHUB_WORKSPACE']
    txt_files = [file for file in os.listdir(repo_root) if file.endswith('.txt')]

    for file in txt_files:
        file_path = os.path.join(repo_root, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 24:
                for line in lines:
                    if len(line.rstrip('\n')) > 59:
                        print(f"Line in file {file} exceeds the maximum length of 59 characters.")
                        continue
                print(f"File {file} has the correct number of lines and line lengths.")
            else:
                print(f"File {file} does not have the correct number of lines.")
                continue

if __name__ == '__main__':
    check_txt_files()


def test_txt_fiels():

    txt_files = ['maps/map.txt', 'screens/start.txt', 'screens/win.txt', 'screens/gameover.txt']

    for file in txt_files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            assert len(lines) <= 24, f"File {file} has more than 24 lines."

            for line in lines:
                assert len(line.rstrip('\n')) <= 59, f"Line in file {file} exceeds the maximum length of 59 characters."

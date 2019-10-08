if __name__ == "__main__":
    CSS = []
    dic = {}
    tmp_name = ""
    tmp_data = []
    new_section = True
    f = open("AppendixASingleDX.txt", mode='r', encoding='utf-8-sig')
    for line in f.readlines():
        line = line.strip('\n')
        if line=="":
            new_section = True
            dic[tmp_name] = tmp_data
            tmp_name = ""
            tmp_data = []
        elif new_section:
            new_section = False
            tmp_name = line[4:].strip()
        else:
            line = line.strip()
            tmp_data += line.split(' ')


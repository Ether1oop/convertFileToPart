import os


def verifyPart(strings):
    string_line = strings.split("\n")

    # 去注释
    for i in range(0,len(string_line)):
        line = string_line[i]
        if line == "":
            continue
        flag = line.find("//")
        if flag != -1:
            string_line[i] = line[:flag].strip()

    for i in range(0,len(string_line)):
        front = string_line[i].find("/*")
        if front != -1:
            rear = string_line[i][front + 2:].find("*/")
            if rear != -1:
                string_line[i] = string_line[i][:front] + string_line[i][rear + 2:]
            else:
                string_line[i] = string_line[i][:front]
                j = i + 1
                for j in range(i + 1, len(string_line)):
                    rear = string_line[j].find("*/")
                    if rear != -1:
                        string_line[j] = string_line[j][rear + 2:]
                        break
                if j < len(string_line):
                    for k in range(i + 1, j):
                        string_line[k] = ""
                else:
                    for k in range(i + 1, len(string_line)):
                        string_line[k] = ""

    # 找到emit所在行，向下检索，若遇到‘+’‘-’并且不包含emit的，则返回False，否则返回True
    emit_line_id = -1
    for i in range(0,len(string_line)):
        line = string_line[i]
        if line == "":
            continue
        if line[0] == '+' or line[0] == '-':
            if line.find(" emit ") != -1:
                emit_line_id = i
                break

    if emit_line_id == -1:
        return False

    for i in range(emit_line_id,len(string_line)):
        line = string_line[i]
        if line == "":
            continue
        if line[0] == "+" or line[0] == '-':
            if len(line) == 1:
                continue

            flag = line.find(" emit ")
            if flag != -1:
                _right = line[flag:].find(")")
                if _right != -1:
                    continue
                else:
                    j = i + 1
                    for j in range(i + 1, len(string_line)):
                        _right = string_line[j].find(")")
                        if _right != -1:
                            break
                    if j < len(string_line):
                        i = j
                        continue
                    else:
                        return True
            else:
                return False
    return True


def splitString(strings):
    file_lines = strings.split("\n")
    tags = []
    results = []

    for i in range(0, len(file_lines)):
        line = file_lines[i]
        front = line.find("@@")
        if front != -1:
            if line[front:].find("@@") != -1:
                tags.append(i)

    tags.append(len(file_lines))

    for i in range(0, len(tags) - 1):
        temp = "\n".join(file_lines[tags[i]: tags[i + 1] - 1])
        if verifyPart(temp):
            results.append(temp)

    return results


def getMaxIdFromList(working_dir):
    dir_list = []
    for item in os.listdir(working_dir):
        if item == '':
            continue
        if item == 'special.txt':
            continue
        if os.path.isfile(working_dir + "/" + item):
            dir_list.append(item)
    dir_list.sort(key=lambda x: int(x[:-4]))

    for i in range(len(dir_list) - 1, -1, -1):
        item = dir_list[i]
        if item == "special.txt":
            continue
        if os.path.isfile(working_dir + "/" + item):
            return int(item[:-4])

    return None


def getUrlFromSpecial(absolute_path):
    working_dir = "/".join(absolute_path.split("/")[:-1])
    _id = int(absolute_path.split("/")[-1][:-4])
    with open(working_dir + "/special.txt","r") as file:
        url_list = file.readlines()
    return url_list[_id - 1]


def generateNewFiles(absolute_path):
    working_dir = "/".join(absolute_path.split("/")[:-1])
    filename = absolute_path.split("/")[-1]
    if filename == "special.txt":
        return False

    with open(absolute_path, "r") as file:
        fileString = file.read()
    passages = splitString(fileString)
    url = getUrlFromSpecial(absolute_path)

    if len(passages) == 0:
        return False

    with open(absolute_path, "w") as file:
        file.write(passages[0])

    for i in range(1, len(passages)):
        new_id = getMaxIdFromList(working_dir)
        with open(working_dir + "/" + str(new_id + 1) + ".txt", "w") as file:
            file.write(passages[i])
        with open(working_dir + "/special.txt", "a") as file:
            file.write(url)



    # with open(working_dir + "/" + new_file_name) as file:
    #     file.write(passages)


def convertFileToPart(working_dir):
    for root, dirs, files in os.walk(working_dir):
        if 'special.txt' in files:
            files.remove("special.txt")
        files.sort(key=lambda x: int(x[:-4]))
        for item in files:
            generateNewFiles(os.path.join(root, item).replace("\\", "/"))


def randomSelect(working_dir):
    for root, dirs, files in os.walk(working_dir):
        for item in files:
            print(os.path.join(root,item))

# convertFileToPart("special_result")
# path = 'results/225.txt'
# generateNewFiles(path)
# generateNewFiles("results/333.txt")
randomSelect("results")
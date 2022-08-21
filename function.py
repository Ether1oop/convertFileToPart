import os


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
        results.append("\n".join(file_lines[tags[i]: tags[i + 1] - 1]))

    return results


def getMaxIdFromList(working_dir):
    dir_list = os.listdir(working_dir)
    dir_list.sort(key=lambda x: x[:-4])

    for i in range(len(dir_list) - 1, 0, -1):
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

    if len(passages) <= 1:
        return False

    for i in range(1, len(passages)):
        new_id = getMaxIdFromList(working_dir)
        with open(working_dir + "/" + str(new_id + 1) + ".txt", "w") as file:
            file.write(passages[i])
        with open(working_dir + "/special.txt", "a") as file:
            file.write(url)

    with open(absolute_path, "w") as file:
        file.write(passages[0])

    # with open(working_dir + "/" + new_file_name) as file:
    #     file.write(passages)


def convertFileToPart(working_dir):
    for root, dirs, files in os.walk(working_dir):
        for item in files:
            generateNewFiles(os.path.join(root, item).replace("\\", "/"))


convertFileToPart("special_result")
# path = 'special_result/EmitChangeParameter/2.txt'
# generateNewFiles(path)

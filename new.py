import re

import numpy as np


def main():
    log_file_path = "test.log"

    regex = '((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))'

    parseData(log_file_path, regex, read_line=True, reparse=True)


def searchIpInFile(ip, log_file_path, read_line=True):
    with open(log_file_path, "r") as file:
        match_list = []
        if read_line:
            for line in file:
                if re.search(ip, line):
                    match_list.append(line)
    print(match_list)
    file.close()


def parseData(log_file_path, regex, read_line=True, reparse=False):
    global countOther, countError, countPos
    with open(log_file_path, "r") as file:
        match_list = []
        if read_line:
            for line in file:
                for match in re.finditer(regex, line, re.S):
                    match_text = match.group()
                    if match_text not in match_list:
                        match_list.append(match_text)

        else:
            data = file.read()
            for match in re.finditer(regex, data, re.S):
                match_text = match.group()
                match_list.append(match_text)
    file.close()
    list1 = []

    if reparse:
        with open(log_file_path, "r") as file:
            lines = file.readlines()

        for m in match_list:
            addlist = []
            for l in lines:
                if m in l:
                    addlist.append(l)
                    lines.remove(l)

            if len(addlist) > 0:
                list1.append(addlist)

    for l in list1:
        arr = np.asarray(l)
        count = 0
        pos = 0
        error = 0
        other = 0
        for i in range(len(arr)):

            countPos = 0
            countError = 0
            countOther = 0
            ll = arr[i].split()
            if i == 0:
                startTime = ll[3] + ll[4]
            if i == len(arr) - 1:
                endTime = ll[3] + ll[4]
            site = ll[0]
            for x in ll:
                if x == "200":
                    countPos = 1
                    pos += 1
                    count = count + 1
                elif x == "404":
                    countError = 1
                    error += 1
                    count = count + 1
                elif x == "304":
                    other += 1
                    count = count + 1
        try:
            errorPercent = error / count * 100
        except ZeroDivisionError:
            errorPercent = 0

        try:
            posResponse = pos / count * 100
        except ZeroDivisionError:
            posResponse = 0

        print("The ", site, " has returned a total of ", pos, " 200 responses, "
                                                              "and ", error,
              " 404 responses, out of total ", count, " requests between ",
              startTime, " and time ", endTime,
              "That is a ", errorPercent, "%", "404 errors, and ",
              posResponse, "% of 200 responses.")

    file.close()

    return -1


if __name__ == '__main__':
    main()


# Task :- A Simple Tool For Log Processing.
# Date :- July/24/2020.

import re

import numpy as np


def main():
    filePath = "sample.log"

    regex = '((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))'

    parseData(filePath, regex, read_line=True, reparse=True)


def parseData(filePath, regex, read_line=True, reparse=False):
    global countOther, countError, countPos
    with open(filePath, "r") as file:
        ipList = []
        if read_line:
            for line in file:
                for ipMatch in re.finditer(regex, line, re.S):
                    ip = ipMatch.group()
                    if ip not in ipList:
                        ipList.append(ip)

        else:
            data = file.read()
            for ipMatch in re.finditer(regex, data, re.S):
                ip = ipMatch.group()
                ipList.append(ip)
    file.close()
    list1 = []

    if reparse:
        with open(filePath, "r") as file:
            lines = file.readlines()

        for ip in ipList:
            addlist = []
            for l in lines:
                if ip in l:
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
            errorPercent = round(error / count * 100, 2)
        except ZeroDivisionError:
            errorPercent = 0

        try:
            posResponse = round(pos / count * 100, 2)
        except ZeroDivisionError:
            posResponse = 0

        print("The ", site, " has returned a total of ", pos, " 200 responses, "
                                                              "and ", error,
              " 404 responses, out of total ", count, " requests between ",
              startTime, " and time ", endTime,
              "That is a ", errorPercent, "%", "404 errors, and ",
              posResponse, "% of 200 responses.")

    file.close()


if __name__ == '__main__':
    main()
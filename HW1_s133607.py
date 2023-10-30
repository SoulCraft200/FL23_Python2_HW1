"""


"""
from sys import exit


def main():
    studentTrans = readStudentTrans()
    studyPlan = readStudyPlan()
    inp = 6
    con = True
    while con:
        notCorrect = True
        while notCorrect:
            print("Menu:\n"
                  "1) Display the semester results is specific course.\n"
                  "2) Display the semester results for a specific semester.\n"
                  "3) Display the complete student transcript.\n"
                  "4) Check if the student is under probation.\n"
                  "5) Recommend next semester courses.\n"
                  "6) Exit.")
            inp = input("Choice: ")
            if not inp.isdigit():
                print("Invalid Input, Integers only!!!!")
            elif int(inp) <= 0 or int(inp) >= 7:
                print("Out of range!!!!")
            else:
                inp = int(inp)
                notCorrect = False
        if inp == 1:
            cr = input("Enter course code: ")
            getCourseInfo(studentTrans, cr.strip())
        elif inp == 2:
            sem = input("Enter semester number: ")
            getSemInfo(studyPlan, studentTrans, sem)
        elif inp == 3:
            getTrans(studyPlan, studentTrans)
        elif inp == 4:
            checkProb(studyPlan, studentTrans)
        elif inp == 5:
            recomSub(studyPlan,studentTrans)
        elif inp == 6:
            re = "y"
            notCorrect = True
            while notCorrect:
                re = input("Are you sure?(y/n): ")
                if re.lower().strip() == "y" or re.lower().strip() == "n":
                    notCorrect = False
                else:
                    print("Invalid Input.")
            if re.lower().strip() == "y":
                exit("Bye!!")


def readStudyPlan():
    studyList = []
    file = open("Study Plan.csv", "r")
    file.readline()
    for line in file:
        line = line.strip().split(",")
        if len(line) == 5:
            studyList.append({"Code": line[1], "Title": line[2], "Credit": int(line[3]), "Category": line[4].strip()})
    return studyList


def readStudentTrans():
    studyTrans = []
    file = open("Student Transcript.csv", "r")
    file.readline()
    for line in file:
        line = line.strip().split(",")
        if len(line) == 3:
            studyTrans.append({"Semester": line[0], "Code": line[1], "Grade": line[2].strip()})
    return studyTrans


def getCourseInfo(list, name):
    info = []
    for i in list:
        if i["Code"] == name:
            info.append(i["Semester"])
            info.append(i["Code"])
            info.append(i["Grade"])
            break
    if len(info) < 3:
        print("Course not taken.")
    else:
        print("*" * 50)
        print("Semester:", info[0])
        print("Code:", info[1])
        print("Grade:", info[2])
        print("*" * 50)


def gpa(mark):
    marks = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3, "B-": 2.7, "C+": 2.3, "C": 2, "C-": 1.7, "D+": 1.3, "D": 1, "F": 0}
    return marks[mark]


def getCredit(list, code):
    found = True
    for i in list:
        if i["Code"] == code:
            return int(i["Credit"])
            found = False
    if found:
        return 0


def getTitle(list, code):
    for i in list:
        if i["Code"] == code:
            return i["Title"]


def getSemInfo(list1, list2, sem, p):
    sumGpaCredit = 0
    sumCredit = 0
    if p == 1:
        print("*" * 110)
        print("%-20s%-60s%-20s%-20s" % ("Code", "Title", "Credit", "Grade"))
        print("*" * 110)
    for i in list2:
        if int(i["Semester"]) <= int(sem):
            if getCredit(list1, i["Code"]) != 0:
                sumGpaCredit += (getCredit(list1, i["Code"]) * gpa(i["Grade"]))
                sumCredit += getCredit(list1, i["Code"])
                if int(i["Semester"]) == int(sem) and p == 1:
                    print("%-20s%-60s%-20d%-20s" % (
                        i["Code"], getTitle(list1, i["Code"]), getCredit(list1, i["Code"]), i["Grade"]))
    if p == 1:
        print("*" * 110)
    if sumCredit != 0 and p == 1:
        cumGPA = round(sumGpaCredit / sumCredit, 2)
    else:
        cumGPA = 0
    if p == 1:
        print("CumGPA = ", cumGPA)
        print("Total Credits = ", sumCredit)
        print("*" * 110)

    return sumGpaCredit, sumCredit


def getTrans(list1, list2):
    output = open("OutPutTranscript.csv", "w")
    for e in range(1, int(list2[-1]["Semester"]) + 1):
        print("Semester", e)
        getSemInfo(list1, list2, e, 1)
        output.write(f"Semester {e}\n")
        sumGpaCredit = 0
        sumCredit = 0
        output.write("Code,Title,Credit,Grade\n")
        for i in list2:
            if int(i["Semester"]) <= int(e):
                if getCredit(list1, i["Code"]) != 0:
                    sumGpaCredit += (getCredit(list1, i["Code"]) * gpa(i["Grade"]))
                    sumCredit += getCredit(list1, i["Code"])
                    if int(i["Semester"]) == int(e):
                        output.write("%s,%s,%s,%s\n" % (
                            i["Code"], getTitle(list1, i["Code"]), getCredit(list1, i["Code"]), i["Grade"]))
        if sumCredit != 0:
            cumGPA = round(sumGpaCredit / sumCredit, 2)
        else:
            cumGPA = 0
        output.write(f"CumGPA,{cumGPA}\n")
        output.write(f"Total Credits, {sumCredit}\n")

    output.close()


def checkProb(list1, list2):
    sem = int(list2[-1]["Semester"])
    sumGpaCredit, sumCredit = getSemInfo(list1, list2, sem, 0)
    if sumCredit != 0:
        gp = round(sumGpaCredit / sumCredit, 2)
        if gp < 2.0:
            print("Under Probation, GPA", gp)
        else:
            print("Not Under Probation, GPA", gp)


def recomSub(list1, list2):
    count = 0
    print("Recommendation")
    print("*" * 110)
    print("%-20s%-60s%-20s%-20s" % ("Code", "Title", "Credit", "Category"))
    print("*" * 110)
    sub = []
    for i in list2:
        sub.append(i["Code"])
    for i in list1:
        if count <= 4 and i["Code"] not in sub:
            count +=1
            print("%-20s%-60s%-20d%-20s" % (i["Code"], i["Title"], i["Credit"], i["Category"]))
    print("*" * 110)


main()

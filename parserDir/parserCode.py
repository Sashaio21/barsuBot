import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import datetime


user = fake_useragent.UserAgent().random


header = {
    'user-agent' : user
}


def getData():
    dateNow = datetime.datetime.now()
    return str(dateNow - datetime.timedelta(days=dateNow.weekday())).split(" ")[0]


# def PrintTibleDate(TimeTableForWeek):
#     for key, value in TimeTableForWeek.items():
#         print(key)
#         for keyOneDay, valueOneDay in TimeTableForWeek[key].items():
#             for keyOneLesson, valueOneLesson in TimeTableForWeek[key][keyOneDay].items():
#                 if TimeTableForWeek[key][keyOneDay][keyOneLesson] != "Нет занятий":
#                     print(keyOneDay, ":")
#                     for keyGroups, valueGroups in TimeTableForWeek[key][keyOneDay][keyOneLesson].items():
#                         print(keyGroups)
#                         for KeyDataLesson, ValueDataLesson in TimeTableForWeek[key][keyOneDay][keyOneLesson][keyGroups].items():
#                             print(ValueDataLesson, end="  ")
#                         print()


def get_week_dates(start_date):
    """Возвращает список дат на неделю, начиная с указанной даты"""
    dayWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'pass']
    week_dates = []
    listDataWeek = []
    dictDataWeek = {}
    for i in range(7):
        day = start_date + datetime.timedelta(days=i)
        week_dates.append(day)
    count = 0
    for day in week_dates:
        d = day.strftime("%d.%m")
        listDataWeek.append(f"  {dayWeek[count]}\n{d}")
        dictDataWeek[dayWeek[count]] = d
        count+=1
    return dictDataWeek


def ParserDataForTeachers(teacher, date, department = "selectcard"):
    DataGroup = {
        'department': department,
        'teacher': teacher,
        'date': date
    }

    # TimeTableForWeekTeacher = {}
    dayWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'pass']
    dayWeek2 = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    link = "https://rasp.barsu.by/teach.php"
    responce = requests.post(link, headers=header, data=DataGroup).text
    soup = BeautifulSoup(responce, 'lxml')
    TimeTable = soup.find('tbody')
    OneLesson = TimeTable.find_all('tr')
    count = 0
    dictForRasp = {}
    tr = date
    dateStart = tr.split("-")
    today = datetime.date(int(dateStart[0]), int(dateStart[1]), int(dateStart[2]))
    week_dates = get_week_dates(today)
    for i in range(0 ,50, 9):
        # print(f"{dayWeek[count]}")
        OneLessonData = {}
        for j in range(0, 8):
            bufferPer = 0
            DataLesson = OneLesson[i+j].find_all('td')
            if len(DataLesson) == 6:
                bufferPer = 2
            # print(DataLesson[0+bufferPer].text)
            typeLesson = "-"
            nameLesson = "-"
            if len(DataLesson[2+bufferPer].text) != 1:
                if len((DataLesson[1+bufferPer].text).split("-")) > 1:
                    typeLesson = (DataLesson[1+bufferPer].text).split("-")[1]
                    nameLesson = (DataLesson[1+bufferPer].text).split("-")[0]
                OneLessonData[DataLesson[0+bufferPer].text] = {"type": typeLesson, "lesson": nameLesson, "group": (DataLesson[2+bufferPer].text), "audience": (DataLesson[3+bufferPer].text)}
            else:
                OneLessonData[DataLesson[0+bufferPer].text] = "Форточка"
            leftIndex = -1
            rightIndex = -1
            countLesson = -1
            countNoLesson = 0
            for l in OneLessonData.values():
                countLesson += 1
                if l != "Форточка":
                    countNoLesson = 0
                if l != "Форточка" and leftIndex == -1:
                    leftIndex = countLesson
                    countNoLesson = 0
                if l == "Форточка":
                    countNoLesson += 1  
            rightIndex = countLesson - countNoLesson
        dayyForRasp =f"  {dayWeek2[count]}\n{week_dates[dayWeek2[count]]}"
        if leftIndex == -1 and rightIndex == -1:
            dictForRasp[dayyForRasp] = "Нет занятий"
        else:
            g = 0 
            lessonData = {}
            for time, val in OneLessonData.items():
                g+=1
                if g > leftIndex and g <=rightIndex+1:
                    lessonData[time.replace("-", "\n").replace(" ", "").replace(".", ":")] = val
            dictForRasp[dayyForRasp] = lessonData
        count+=1
    # with open("tes4454t.html", "w", encoding="utf-8") as file:
    #     file.write(responce)
    # print(dictForRasp)
    return(dictForRasp)





def ParserDataForStudent(facultet, speciality, group, date):
    DataGroup = {
        'faculty': facultet,
        'speciality': speciality,
        'groups': group,
        'weekbegindate' : date
    }

    TimeTableForWeek = {}

    dayWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'pass']

    link = "https://rasp.barsu.by/stud.php"

    responce = requests.post(link, headers=header, data=DataGroup).text

    soup = BeautifulSoup(responce, 'lxml')
    TimeTable = soup.find('tbody', class_ = 'min-p')
    
    t  = 0
    dayWeek2 = []
    NewTable = TimeTable.find_all('tr')
    offset = 0
    if len(NewTable) != 49:
        offset = 1
    days = TimeTable.find_all("td")
    for ifd in range(0, len(days), 18):
        # print(days[ifd].text.replace(" ", ""))
        finalNameDay = ""
        nameDay = days[ifd].text.replace(" ", "")
        finalNameDay = finalNameDay+nameDay[0]
        finalNameDay = finalNameDay+nameDay[1].lower()

        dayWeek2.append(finalNameDay)
    # print(dayWeek2)
    NewTable.append("pass")
    count = 0
    ListWeek = []
    for i in range(len(dayWeek2)):
        i = i*10
        LessonForOneDay = {
        }
        for j in range(offset, 8):
            perhapsСhanges = False
            if str(NewTable[i+j]).find("#ffb2b9") != -1:
                perhapsСhanges = True
            OneLesson = str(NewTable[i+j]).replace('<td bgcolor="#ffffff">', "time").\
            replace('<td bgcolor="#ffb2b9">', "time").\
            replace("пг: ", "<br/>subgroup").\
            replace("<td>", "").replace("</tr>","").\
            replace('<tr align="center" bgcolor="#9dc6f2">', "").\
            replace("</td>", "").\
            replace(' - ', '<br/>').\
            replace("\n", "").\
            replace("  ", "")
            OneLesson = OneLesson.split("time")
            OneLesson[1] = OneLesson[1].split("subgroup")
            for l in range(0, len(OneLesson[1])):
                if len(OneLesson[1]) > 1:
                    if l+1 != len(OneLesson[1]):
                        bufferText = OneLesson[1][l+1][0:OneLesson[1][l+1].find("<br/>")]
                        OneLesson[1][l] = OneLesson[1][l]+ bufferText
                OneLesson[1][l] = OneLesson[1][l].split("<br/>")
            if len(OneLesson[1])==3:
                OneLesson[1].pop(2)
            if len(OneLesson[1]) > 1:
                OneLesson[1][1].pop(0)
                # print(OneLesson[1])
                if len(OneLesson[1][1]) == 1:
                    OneLesson[1].pop(1)
            OneLessonDict = {}
            for g in range(8):
                SubGroup = {}
                if len(OneLesson[1]) > 1:
                    TwoSubgroups = {}
                    for q in range(2):
                        LessonData = {}
                        LessonData["lessonOne"] = OneLesson[1][q][0]
                        LessonData["typeLesson"] = OneLesson[1][q][1]
                        LessonData["prepod"] = OneLesson[1][q][2]
                        LessonData["audience"] = OneLesson[1][q][3]
                        LessonData["perhapsСhanges"] = perhapsСhanges
                        TwoSubgroups[f"{OneLesson[1][q][4]}-пг"] = LessonData
                    OneLessonDict["lesson"] = TwoSubgroups
                else:
                    if len(OneLesson[1][0]) < 4:
                        OneLessonDict['lesson'] = "Нет занятий"
                    else:
                        LessonData = {}
                        LessonData["lessonOne"] = OneLesson[1][0][0]
                        LessonData["typeLesson"] = OneLesson[1][0][1]
                        LessonData["prepod"] = OneLesson[1][0][2]
                        LessonData["audience"] = OneLesson[1][0][3]
                        LessonData["perhapsСhanges"] = perhapsСhanges
                        SubGroup["Вся группа"] = LessonData
                        OneLessonDict['lesson'] = SubGroup
            LessonForOneDay[OneLesson[0]]  = OneLessonDict


        TimeTableForWeek[dayWeek[count]] = LessonForOneDay
        ListWeek.append(LessonForOneDay)
        count+=1
    tr = date
    dateStart = tr.split("-")
    today = datetime.date(int(dateStart[0]), int(dateStart[1]), int(dateStart[2]))
    week_dates = get_week_dates(today)
    dictForImage = {}
    countWeek = 0
    for key, value in TimeTableForWeek.items():
        dataOneLesson = {}
        for keyOneLesson, valueOneLesson in value.items():
            listOneLesson = []
            if valueOneLesson["lesson"] != "Нет занятий":
                for keyDataLesson, valueDataLesson in valueOneLesson["lesson"].items():
                    datalesonDict = {}
                    subgroup = keyDataLesson
                    if keyDataLesson == "Вся группа":
                        subgroup = "" 
                    datalesonDict["type"] = valueDataLesson["typeLesson"]
                    datalesonDict["subgroup"] = subgroup
                    datalesonDict["lesson"] = valueDataLesson["lessonOne"]
                    datalesonDict["teacher"] = valueDataLesson["prepod"]
                    datalesonDict["audience"] = valueDataLesson["audience"]
                    listOneLesson.append(datalesonDict)
            else:
                continue
            dataOneLesson[keyOneLesson.replace("-", "\n").replace(" ", "").replace(".", ":")] = listOneLesson
        dayyForRasp =f"  {dayWeek2[countWeek]}\n{week_dates[dayWeek2[countWeek]]}"
        dictForImage[dayyForRasp] = dataOneLesson
        countWeek+=1
    # print(dictForImage)
    return dictForImage


# ParserDataForTeachers('Мирошникова Ю.Ф.', '2023-09-04')
# ParserDataForStudent("Инженерный факультет", "Информационные системы и технологии", "ИСТ31", "2023-09-04")
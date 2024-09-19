import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import datetime
from requests import Session

user = fake_useragent.UserAgent().random

header = {
    'user-agent' : user
}



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
        'department': department.encode('utf-8'),
        'teacher': str(teacher).encode('utf-8'),
        'date': date
    }
    s = Session()
    s.headers.update(DataGroup)


    # TimeTableForWeekTeacher = {}
    dayWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'pass']
    dayWeek2 = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    link = "https://rasp.barsu.by/teach.php"
    responce2 = s.get(link).text
    print(responce2)
    with open("aaaaaa.html", "w", encoding="utf-8") as file:
        file.write(responce2)
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
    print(responce)


ParserDataForTeachers("Шапович Е.Г.", "2023-09-04")
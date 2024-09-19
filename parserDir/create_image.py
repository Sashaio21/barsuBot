from PIL import Image, ImageDraw, ImageFont
# from parserCode import ParserDataForStudent, ParserDataForTeachers



def createPhotoWithTimeTable(schedule, who):
    wight = 5
    # Define the schedule dictionary with events and timings for a week
    # schedule = ParserDataForStudent(fac, speciality, group, data)
    img = Image.new("RGB", (850+wight, 2500), color=(247, 247, 247))
    # Create a drawing context and set the font
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 19)
    fontDay = ImageFont.truetype("arial.ttf", 18)
    fontBig = ImageFont.truetype("arial.ttf", 22)  
    # Define the outline color and width
    outline_color = (0, 0, 255)
    outline_width = 4
    new_height = 0
    bufferOffset = 0
    # Draw the schedule events and timings on the image
    y_offset = 45
    if schedule == {}:
        return "Расписание отсутствует"
    else:
        if who == "student":
            for day, events in schedule.items():
                # Draw a rectangle around each week
                draw.line((10, y_offset-3, 840+wight,  y_offset-3), fill=outline_color, width=outline_width)
                y_offset += 12 # Отступ всего дня сверху
                new_height = new_height + y_offset
                draw.text((25, y_offset), day, fill=(0, 0, 0), font=fontDay)
                # print(len(events))
                countLesson = 0
                for time, event_list in events.items():
                    countLesson+=1
                    draw.text((25+65, y_offset), time + "", fill=(0, 0, 0), font=font)
                    if len(event_list) ==1:
                        y_offset += 10
                    elif len(event_list) !=1:
                        y_offset +=0
                    new_height = new_height + y_offset
                    for event in event_list:
                        draw.text((150, y_offset), "" + event["subgroup"], fill=(8, 0, 0), font=font)
                        draw.text((235, y_offset), "" + event["type"].split(" ")[0], fill=(8, 0, 0), font=font)
                        draw.text((280, y_offset), "" + event["lesson"], fill=(8, 0, 0), font=font)
                        draw.text((550, y_offset), "" + event["teacher"], fill=(8, 0, 0), font=font)
                        draw.text((720, y_offset), "" + event["audience"], fill=(8, 0, 0), font=font)
                        y_offset += 22
                    if len(event_list) ==1:
                        y_offset +=22
                    elif len(event_list) !=1:
                        y_offset +=11
                    if countLesson != len(events):
                        draw.line((20+60, y_offset-7, 830+wight,  y_offset-7), fill='gray', width=1)
                y_offset += 15
        else:
            for day, events in schedule.items():
                # Draw a rectangle around each week
                draw.line((10, y_offset-3, 840+wight,  y_offset-3), fill=outline_color, width=outline_width)
                y_offset += 12 # Отступ всего дня сверху
                new_height = new_height + y_offset
                draw.text((25, y_offset), day, fill=(0, 0, 0), font=fontDay)
                # print(len(events))
                countLesson = 0
                if events =="Нет занятий":
                    y_offset += 10
                    draw.text((280, y_offset), "   Занятия\nотсутствуют", fill=(8, 0, 0), font=fontBig)
                    y_offset += 55
                else:
                    count = 0
                    for time, event_list in events.items():
                        count+=1
                        y_offset += 3
                        if event_list != "Форточка":
                            countLesson+=1
                            draw.text((25+65, y_offset), time + "", fill=(0, 0, 0), font=font)
                            if len(event_list) ==1:
                                y_offset += 0
                            elif len(event_list) !=1:
                                y_offset +=0
                            new_height = new_height + y_offset
                            draw.text((235, y_offset), "" + event_list["type"], fill=(8, 0, 0), font=font)
                            draw.text((280, y_offset), "" + event_list["lesson"], fill=(8, 0, 0), font=font)
                            draw.text((550, y_offset), "" + event_list["group"], fill=(8, 0, 0), font=font)
                            draw.text((720, y_offset), "" + event_list["audience"], fill=(8, 0, 0), font=font)
                            y_offset += 22 + 35
                            draw.line((20+60, y_offset-7, 830+wight,  y_offset-7), fill='gray', width=1)
                        else:
                            draw.text((25+65, y_offset), time + "", fill=(0, 0, 0), font=font)
                            draw.text((280, y_offset), "Форточка", fill=(8, 0, 0), font=fontBig)
                            y_offset += 22 + 30
                            # if countLesson != len(events):
                            draw.line((20+60, y_offset-7, 830+wight,  y_offset-7), fill='gray', width=1)
                        if len(event_list) == count-1:
                            y_offset -= 5
                        else:
                            y_offset += 10
                y_offset += 15
        # Save the image
        box = ()
        # print(countLesson)
        # Crop the image
        width, height = img.size

        # new_height = 500
        left = 0
        top = 30
        right = width
        bottom = (y_offset-15)
        img = img.crop((left, top, right, bottom))
        img.save("parserDir/image/timetable.png")
        return "parserDir/image/timetable.png"


# createPhotoWithTimeTable(ParserDataForTeachers('Мирошникова Ю.Ф.', '2023-09-04'), "teachers")

# dictForImage = {'  Пн\n03.04': {'13:25\n14:45': [{'type': 'ПЗ', 'subgroup': '', 'lesson': 'Электротехника', 'teacher': 'Дубень И.В.', 'audience': '3/215 Парк'}], '14:55\n16:15': [{'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'КМММ', 'teacher': 'Раковцы Г.М.', 'audience': '5/301 Парк'}, {'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 'Программирование1С', 'teacher': 'Кравчук О.Д.', 'audience': '4/307 Парк'}], '16:30\n17:50': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'КМММ', 'teacher': 'Раковцы Г.М.', 
# 'audience': '5/401 Парк'}], '18:00\n19:20': [{'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'КМММ', 'teacher': 'Раковцы Г.М.', 'audience': '5/301 Парк'}, {'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 'ПрогрРобототехнСист', 'teacher': 'Калько А.И.', 'audience': '4/307 Парк'}]}, '  Вт\n04.04': {'13:25\n14:45': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'Электротехника', 'teacher': 'Дубень И.В.', 'audience': '3/215 Парк'}], '14:55\n16:15': [{'type': 'ПЗ', 'subgroup': '', 'lesson': 'ФизКультура', 'teacher': 'Филимонова Н.И.', 'audience': ' '}], '16:30\n17:50': [{'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 'КомпСети', 'teacher': 'Шапович Е.Г.', 'audience': '3/209 Парк'}, {'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'ПрогрРобототехнСист', 'teacher': 'Калько А.И.', 'audience': '5/301 Парк'}], '18:00\n19:20': [{'type': 'КР (рк)', 'subgroup': '', 'lesson': 'ПрогрРобототехнСист', 'teacher': 'Калько А.И.', 'audience': '5/301 Парк'}], '19:30\n20:50': [{'type': 'ПЗ', 'subgroup': '', 'lesson': 'ИнфЧас', 'teacher': 'Калько А.И.', 'audience': '5/401 Парк'}]}, '  Ср\n05.04': {'14:55\n16:15': [{'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 
# 'КМММ', 'teacher': 'Раковцы Г.М.', 'audience': '4/307 Парк'}, {'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'Программирование1С', 'teacher': 'Кравчук О.Д.', 'audience': '4/318 Парк'}], '16:30\n17:50': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'Философия', 'teacher': 'Жук Г.В.', 'audience': '4/409 Парк'}], '18:00\n19:20': [{'type': 'СЗ', 'subgroup': '', 'lesson': 'Философия', 'teacher': 'Жук Г.В.', 'audience': '4/410 Парк'}]}, '  Чт\n06.04': {'13:25\n14:45': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'Программирование1С', 'teacher': 'Кравчук О.Д.', 'audience': '5/401 Парк'}], '14:55\n16:15': [{'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 'ИнтПакРешПрЗ', 'teacher': 'Кравчук О.Д.', 'audience': '5/301 Парк'}, {'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'ИнтПакРешПрЗ', 'teacher': 'Шах А.В.', 'audience': '5/308 Парк'}], '16:30\n17:50': [{'type': 'ЛЗ', 'subgroup': '2-пг', 'lesson': 'КомпСети', 'teacher': 'Шапович Е.Г.', 'audience': '5/301 Парк'}, {'type': 'ЛЗ', 'subgroup': '1-пг', 'lesson': 'ТехнМашИПриб', 'teacher': 'Дерман Е.А.', 'audience': '3/208 Парк'}], '18:00\n19:20': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'ТехнМашИПриб', 'teacher': 'Дерман Е.А.', 'audience': '5/401 Парк'}]}, '  Пт\n07.04': {'13:25\n14:45': [{'type': 'ПЗ', 'subgroup': '', 'lesson': 'ФизКультура', 'teacher': 
# 'Филимонова Н.И.', 'audience': ' '}], '14:55\n16:15': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'ИстНаукиИТех', 'teacher': 'Кривуть В.И.', 'audience': '4/409 Парк'}], '16:30\n17:50': [{'type': 'ЛК', 'subgroup': '', 'lesson': 'ОхранаТруда', 'teacher': 'Новик А.Н.', 'audience': '5/201 Парк'}], '18:00\n19:20': [{'type': 'ПЗ', 'subgroup': '', 'lesson': 'ОхранаТруда', 'teacher': 'Новик А.Н.', 'audience': '5/201 Парк'}]}}

# createPhotoWithTimeTable(ParserDataForStudent("selectcard", "selectcard", 'ИСТ31', '2023-09-04'), "student")
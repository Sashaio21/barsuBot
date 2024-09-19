import psycopg2
from aiogram import Dispatcher, types 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command, Text
import json
from aiogram.types import Message, CallbackQuery
from createBot import bot
from keyboards.inlinebutton import create_button, firstKB
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from parserDir.create_image import createPhotoWithTimeTable
from parserDir.parserCode import ParserDataForStudent, ParserDataForTeachers
from dbPostgre.dbInit import createRecord, getData, AvailabilityUser, deleteRecord


listSelectedTeachers = []
listTeachers = ['', 'Гулевич Г.В.', 'Житкевич Г.Я.', 'Короб А.Н.', 'Лабун Д.В.', 'Недашковская Н.С.', 'Прудникова А.Н.', 'Селюжицкий В.Ю.', 'Хитрова И.А.', 'Белохвостик А.А.', 'Даниленко Э.И.', 'Долгая М.Г.', 'Крутько Р.В.', 'Людвикевич О.Н.', 'Пашкевич К.В.', 'Петрушко Л.Н.', 'Рутман Е.Я.', 'Шуленкова И.В.', 'Бужинская Н.А.', 'Василевич Н.А.', 'Дубешко Н.Г.', 'Захарченя Н.Ф.', 'Кондратюк С.В.', 'Королева Н.А.', 'Купцова М.Г.', 'Махляр А.П.', 'Никашина Г.А.', 'Петрушко Т.В.', 'Подлесная А.С.', 'Савеня В.Н.', 'Шовгеня М.М.', 'Земринько А.П.', 'Калько А.И.', 'Качкар Г.В.', 'Кравчук О.Д.', 'Мирошникова Ю.Ф.', 'Нерода Ю.П.', 'Петлицкая Т.С.', 'Раковцы Г.М.', 'Сергеева Ю.В.', 'Соловей Е.В.', 'Шапович Е.Г.', 'Шах А.В.', 'Андрияшко М.В.', 'Демидович А.В.', 'Мелеховец Ю.А.', 'Петровский Н.А.', 'Прокуда О.Ю.', 'Ревковская Л.Н.', 'Танана Ю.Н.', 'Ханкевич С.М.', 'Черняк Ю.В.', 'Гребень Т.М.', 'Дырда Ж.Н.', 'Жих И.В.', 'Занько К.А.', 'Захарченя Н.И.', 'Зубрицкая Л.С.', 'Карачун Т.В.', 'Колушенкова А.В.', 'Копытич И.Г.', 'Криштоп И.С.', 'Лавренкова М.Д.', 'Леон О.В.', 'Любанец И.И.', 'Пинюта И.В.', 'Прадун А.В.', 'Пятакова Т.С.', 'Самаукина А.П.', 'Су Яньпин', 'Сун Хаобинь', 'Цеханович И.Г.', 'Якименко Е.В.', 'Вируцкая С.В.', 'Дегиль Н.И.', 'Ермакович Л.И.', 'Жук Г.В.', 'Захарова Э.В.', 'Иванченко Т.Н.', 'Казакевич Т.В.', 'Капуза Л.Г.', 'Кветко З.Н.', 'Клещева Е.А.', 'Котько П.Д.', 'Кривуть М.Л.', 'Литвинский А.В.', 'Лукашевич Т.М.', 'Миранкова Е.В.', 'Пономарёва Е.И.', 'Романчук Н.В.', 'Руднева А.Э.', 'Самусевич Н.В.', 'Сенюта Н.В.', 'Берташ А.И.', 'Ващилко Н.П.', 'Герасимович Е.Н.', 'Иценко А.Г.', 'Кипель А.С..', 'Кишея И.Л.', 'Ковалевич Е.С.', 'Король М.А.', 'Коховец Д.Н.', 'Красько Е.А.', 'Курило М.В.', 'Левкевич В.Г.', 'Левкевич Л.Н.', 'Лешкевич А.К.', 'Лешкевич Е.В.', 'Лукьянчик А.С.', 'Макоед В.Н.', 'Мартынюк Н.С.', 'Новаш Т.С.', 'Ножка И.А.', 'Радионова И.Б.', 'Рзаева Ж.В.', 'Рудая Д.В.', 'Самусик А.И.', 'Тхорик Н.С.', 'Филимонова Н.И.', 'Чурилов Е.В.', 'Шавель Н.Н.', 'Шило О.В', 'Ярошевич Н.В.', 'Яценко Т.Е.', 'Алексеевич В.Н.', 'Аллито Х.М.', 'Гордейчик С.В.', 'Громова И.В.', 'Дыдышко Ж.Л.', 'Климук В.В.', 'Костюкевич Е.А.', 'Лизакова Р.А.', 'Лукьянчик Е.Г.', 'Низовец Д.В.', 'Рябова К.И.', 'Харкевич И.С.', 'Хованская М.М.', 'Черняк Е.В.', 'Алифанов А.В.', 'Богданова Т.Я', 'Богданович И.А.', 'Бушкевич Р.В.', 'Винничек К.С.', 'Водопьян Н.В.', 'Волчек О.М.', 'Горавский И.А.', 'Дерман Е.А.', 'Дремук В.А.', 'Ковальчук И.В.', 'Кондратчик Н.Ю.', 'Литвинович Т.П.', 'Малевич А.В.', 'Наливко О.И.', 'Рогозина Е.В.', 'Сидор Е.С.', 'Сотник Л.Л.', 'Бурдейко В.А.', 'Дремук В.А.', 'Дубень И.В.', 'Кочурко В.И.', 'Кунаш М.В.', 'Потапов В.А.', 'Приходько С.Л.', 'Бартошевич И.А.', 'Булатая Е.В.', 'Ванюк Ю.В.', 'Васильчук Е.Н.', 'Воробей А.Н.', 'Грицкевич Е.И.', 'Карпович-Скопинцева В.К.', 'Киселева Е.В.', 'Кондратеня О.И.', 'Коновалик В.К.', 'Корзун З.И.', 'Круглякова Н.Н.', 'Лобковская Е.А.', 'Манкевич Ж.Б.', 'Мясоед А.П.', 
'Нагорная Т.В.', 'Панкевич Е.Ю.', 'Рогожинская Т.А.', 'Рыжова Ю.И.', 'Савко А.А.', 'Татаринович Е.В.', 'Белая Е.И.', 'Ермалович Н.В.', 'Зуева К.А.', 'Костина Ж.В.', 'Милостивая О.И.', 'Прокофьева Л.В.', 'Пучинская Т.М.', 'Томчик Д.С.', 'Чуносова И.С.', 'Шавель О.М.', 'Шлег А.В.']


def getDateForRasp():
    dateNow = datetime.datetime.now()
    dateNextWeek = str(dateNow + datetime.timedelta(days=7 - dateNow.weekday())).split(" ")[0]
    dateNowWeek = str(dateNow - datetime.timedelta(days=dateNow.weekday())).split(" ")[0]
    weekDates = [dateNowWeek, dateNextWeek]
    return weekDates


whoWeek = ["Текущая", "Следующая"]


with open('groups.txt') as json_file:
    data1 = json.load(json_file)
listGroup = json.loads(data1)


fakultets = ['Институт повышения квалификации и переподготовка', 'Факультет педагогики и психологии', 'Факультет экономики и права', 'Инженерный факультет', 'Лингвистический факультет']
selectFakultets = ""


class FSMTibleDate(StatesGroup):
    start = State()
    facultety = State()
    speciality = State()
    group = State()
    week = State()
    photo = State()
    nameTeacher = State()
    searchTeacher = State()
    # sendPhoto = State()


# Создание списков для выбора
def createList(OldList):
    NewList = []
    for OneElList in OldList:
        NewList.append(OneElList)
    return NewList


# Запуск машины состояний 
async def start_fsm(message : Message):
    if AvailabilityUser(message.chat.id) == None:
        await FSMTibleDate.start.set()
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Для кого расписание?", reply_markup=firstKB)
    else:
        markup = create_button(whoWeek, 2)  
        
        await FSMTibleDate.week.set()
        await bot.send_message(message.chat.id,"Выберете неделю", reply_markup=markup)
        # await answer()


    
async def firstOption(callback : CallbackQuery, state : FSMContext):
    if callback.data == "cancel":
        # fakultets.clear()
        async with state.proxy() as data:
            data.clear()
        await callback.message.delete()
        await callback.answer()
        await state.finish()
    else:
        async with state.proxy() as data:
            data["who_you"] = callback.data
        if callback.data == "student":
            await FSMTibleDate.facultety.set()
            markup = create_button(createList(listGroup["Fakultetions"]), 1)
            
            await callback.message.edit_text("Введите факультет",  reply_markup=markup)
        else:
            await FSMTibleDate.searchTeacher.set()
            await callback.message.edit_text("Введите фамилию преподавателя")
            


async def optionsTeacher(message : Message):
    await message.delete()
    v = 0
    for name in listTeachers:
        if name[0:name.find(" ")] == message.text:
            listSelectedTeachers.append(name)
    if listSelectedTeachers == []:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await bot.send_message(message.chat.id, f"Неверно введена фамилия :(\nВведите ещё раз")
        await FSMTibleDate.searchTeacher.set()
    else:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await FSMTibleDate.group.set() 
        markup = create_button(createList(listSelectedTeachers), 2)
        await bot.send_message(message.chat.id, "Выберете преподавателя", reply_markup=markup)




# Сброс настроек
async def ResetData(message : Message):
    deleteRecord(message.chat.id)


# Выбор специальности
async def who_facultety(callback : CallbackQuery, state : FSMContext):
    if callback.data == "cancel":
        # fakultets.clear()
        async with state.proxy() as data:
            data.clear()
        await callback.message.delete()
        await callback.answer()
        await state.finish()
    else:
        async with state.proxy() as data:
            data["facultety"] = callback.data
            specialitys = []
            for speciality in listGroup["Fakultetions"][fakultets[int(data["facultety"])]]:
                specialitys.append(speciality)
            data["ListSpeciality"] = specialitys
        await FSMTibleDate.next()
        specialitys.clear()
        markup = create_button(data["ListSpeciality"], 1)
        await callback.message.edit_text("Введите специальность",  reply_markup=markup)
        await callback.answer()


# Выбор группы
async def who_speciality(callback : CallbackQuery, state : FSMContext):
    if callback.data == "cancel":
        async with state.proxy() as data:
            data.clear()
        await callback.message.delete()
        await callback.answer()
        await state.finish()
    else:
        async with state.proxy() as data:
            data["speciality"] = callback.data
            groups = []
            for group in listGroup["Fakultetions"][fakultets[int(data["facultety"])]][data["ListSpeciality"][int(data["speciality"])]]:
                groups.append(group)
            data["ListGroups"] = groups
        await FSMTibleDate.next()
        
        markup = create_button(data["ListGroups"],5)
        await callback.message.edit_text("Введите группу", reply_markup=markup)
        await callback.answer()


# Выбор недели
async def who_group(callback : CallbackQuery, state : FSMContext):
    if callback.data == "cancel":
        listSelectedTeachers.clear()
        async with state.proxy() as data:
            data.clear()
        await callback.message.delete()
        await callback.answer()
        await state.finish()
    else:
        async with state.proxy() as data:
            data["group"] = callback.data
        markup = create_button(whoWeek, 2)  
        await FSMTibleDate.next()
        await callback.message.edit_text("Выберете неделю", reply_markup=markup)
        await callback.answer()

# Получение данных и отправка расписания
async def who_week(callback : CallbackQuery, state : FSMContext):
    if callback.data == "cancel":
        async with state.proxy() as data:
            data.clear()
        await callback.message.delete()
        await callback.answer()
        await state.finish()
    else:
        async with state.proxy() as data:
            data["week"] = callback.data
        await FSMTibleDate.next()
        Type=""
        
        if AvailabilityUser(callback.message.chat.id) == None:
            Type = data["who_you"]
            if data["who_you"] == "student":            
                selectFakultets = fakultets[int(data["facultety"])]
                selectSpeciality = data["ListSpeciality"][int(data["speciality"])]
                selectGroup = data["ListGroups"][int(data["group"])]
                createRecord(callback.message.chat.id, selectFakultets,selectSpeciality,selectGroup, who=Type)
            else:
                name = listSelectedTeachers[int(data["group"])] 
                createRecord(callback.message.chat.id, faculty="",speciality="", group="",nameTeacher=name, who=Type)
        else:
            dataForRasp = (getData(callback.message.chat.id))
            # print(list(dataForRasp))
            Type = dataForRasp[5]
            if Type == "student":            
                selectFakultets = dataForRasp[1].replace("_"," ")
                selectSpeciality = dataForRasp[2].replace("_"," ")
                selectGroup = dataForRasp[3].replace("_"," ")
                print(selectFakultets, selectSpeciality, selectGroup)
            else:
                name = dataForRasp[4].replace("_"," ")
                print(name)
        listSelectedTeachers.clear()
        getDateForRasp()[int(data["week"])]
        selectWeek = getDateForRasp()[int(data["week"])]
        print(selectWeek)
        await callback.message.edit_text(f"Немного подождите...") 
        if Type == "student":
            photo = createPhotoWithTimeTable(ParserDataForStudent(selectFakultets, selectSpeciality, selectGroup, selectWeek), "student")
        else:
            photo = createPhotoWithTimeTable(ParserDataForTeachers(name, selectWeek), "teachers")
        dateWeek =".".join(list(reversed(selectWeek.split('-'))))
        if photo == "Расписание отсутствует":
            async with state.proxy() as data:
                data.clear()
            if Type == "student":
                await callback.message.edit_text(f"Расписание на {dateWeek} для группы {selectGroup} пока отсутствует.\nПопробуйте позже") 
            else:
                await callback.message.edit_text(f"Расписание на {dateWeek} для преподавателя {name} пока отсутствует.\nПопробуйте позже") 
        else:
            photo_file = types.InputFile(photo)
            if Type == "student":
                await callback.message.edit_text(f"Расписани для группы {selectGroup}\n({dateWeek})")
            else:
                await callback.message.edit_text(f"Расписани для преподавателя {name}\n({dateWeek})")
            await bot.send_photo(chat_id=callback.message.chat.id, photo=photo_file)
            async with state.proxy() as data:
                data.clear()
            # fakultets.clear()
            await state.finish()
        

async def cancel_fms(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data.clear()
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()



def register_FSM(dp : Dispatcher):
    dp.register_message_handler(cancel_fms ,state="*", commands="cancel")
    dp.register_message_handler(ResetData, Text(equals="Сбросить", ignore_case=True), state=None)
    dp.register_message_handler(start_fsm, Text(equals="Узнать расписание", ignore_case=True), state=None)
    dp.register_message_handler(optionsTeacher, state=FSMTibleDate.searchTeacher)
    dp.register_callback_query_handler(firstOption, state=FSMTibleDate.start)
    dp.register_callback_query_handler(who_facultety, state=FSMTibleDate.facultety)
    dp.register_callback_query_handler(who_speciality, state=FSMTibleDate.speciality)
    dp.register_callback_query_handler(who_group, state=FSMTibleDate.group)
    dp.register_callback_query_handler(who_week,state=FSMTibleDate.week)
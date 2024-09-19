import json





dataUsers = {
}

# dataUsers.append("dsfsdfsd")

# dataUsers["35345434"] = {}

def addRecord(id="", who="", faculty="", speciality="", group="", name = ""):
    dataUsers[id] = {"кто":who, "Факультет":faculty, "Специальность":speciality, "Группа":group, "Имя":name}
    with open('dataUsers.json', 'w') as outfile:
        json.dump(dataUsers, outfile)





addRecord("asads5454", "23gffgddg","dfgdfg","fdgdgdg")
addRecord("3422w22222222234423423423534", "23gffgddg","dfgdfg","fdgdgdg")
print(dataUsers)
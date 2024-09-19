import requests
from bs4 import BeautifulSoup
import fake_useragent
import json

user = fake_useragent.UserAgent().random

header = {
    'user-agent' : user
}


link = "https://rasp.barsu.by/teach.php"
responce = requests.post(link, headers=header).text
# print(responce)

soup = BeautifulSoup(responce, 'lxml')

ListGroupsTeacher = ""

BlockWithFakultet = soup.find('select', id="kafedra")
Fakultetions = BlockWithFakultet.find_all('option')
Fakultetions.pop(0)
fakultetDict = {}
for kafedra in Fakultetions:
    # print(kafedra.text)
    BlockWithSpecialitys = soup.find('select', id="teacher")
    teachers = BlockWithSpecialitys.find_all("option", class_ = kafedra.text)
    for i in range(len(teachers)):
        # print(teachers[i].text)
        ListGroupsTeacher = ListGroupsTeacher +"_"+teachers[i].text
        # teachers[i] = teachers[i].text
    # print(teachers)


# print(ListGroupsTeacher)
ggg = (ListGroupsTeacher)

# ListGroupsJSON = json.dumps(ListGroupsTeacher, indent=2)

with open('teachers.txt', 'w') as outfile:
    outfile.write(str(ggg))
# print(ListGroupsJSON)

# print()
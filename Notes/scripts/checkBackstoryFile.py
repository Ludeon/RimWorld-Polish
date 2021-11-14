# coding=utf-8
import re
import xml.etree.ElementTree as ET
from threading import Thread

import requests

dict_files = [
    "loteric",
    "loterica",
    "lotericach",
    "lotericami",
    "loterice",
    "lotericem",
    "lotericom",
    "lotericowi",
    "lotericowie",
    "lotericu",
    "lotericów",
    "aspergera",
    "arcknight",
    "industries",
    "thrumbo",
    "rest",
    "corestars",
    "entertainment",
    "company",
    "ceti",
    "rugby",
    "rampage",
    "ticonderoga",
    "noob",
    "khalderii",
    "rural",
    "aracena",
    "glitterworld",
    "glitterworldu",
    "glitterworldzkiej",
    "glitterworldzka",
    "glitterworldzie",
    "glitterworldów",
    "glitterworldzka",
    "glitterworldzki",
    "glitterworldzkich",
    "glitterworldzkie",
    "glitterworldzkiego",
    "glitterworldzkiej",
    "glitterworldzkiemu",
    "glitterworldzkim",
    "glitterworldzkimi",
    "nanogenetyczna",
    "nanogenetyczne",
    "nanogenetycznego",
    "nanogenetycznej",
    "nanogenetycznemu",
    "nanogenetyczni",
    "nanogenetyczno",
    "nanogenetyczny",
    "nanogenetycznych",
    "nanogenetycznym",
    "nanogenetycznymi",
    "nanogenetyczną",
    "archotyczna",
    "archotyczne",
    "archotycznego",
    "archotycznej",
    "archotycznemu",
    "archotyczni",
    "archotyczno",
    "archotyczny",
    "archotycznych",
    "archotycznym",
    "archotycznymi",
    "archotyczną",
    "urbworld",
    "urbworldu",
    "urbworldy",
    "urbworldzkiej",
    "urbworldzka",
    "urbworldzie",
    "urbworldów",
    "urbworldzka",
    "urbworldzki",
    "urbworldzkich",
    "urbworldzkie",
    "urbworldzkiego",
    "urbworldzkiej",
    "urbworldzkiemu",
    "urbworldzkim",
    "urbworldzkimi",
    "urbworldach",
    "rimworld",
    "rimworldu",
    "rimworldzkiej",
    "rimworldzka",
    "rimworldzie",
    "rimworldów",
    "rimworldzka",
    "rimworldzki",
    "rimworldzkich",
    "rimworldzkie",
    "rimworldzkiego",
    "rimworldzkiej",
    "rimworldzkiemu",
    "rimworldzkim",
    "rimworldzkimi",
    "rimworldach",
    "rimworldami",
    "xenno",
    "xennoa",
    "xennoach",
    "xennoami",
    "xennoie",
    "xennoo",
    "xennoom",
    "xennoy",
    "xennoą",
    "xennoę",
    "zartz",
    "zartza",
    "zartzach",
    "zartzami",
    "zartzie",
    "zartzo",
    "zartzom",
    "zartzy",
    "zartzą",
    "zartzę",
    "medievalworld",
    "medievalworldu",
    "medievalworldzkiej",
    "medievalworldzka",
    "medievalworldzie",
    "medievalworldów",
    "medievalworldzka",
    "medievalworldzki",
    "medievalworldzkich",
    "medievalworldzkie",
    "medievalworldzkiego",
    "medievalworldzkiej",
    "medievalworldzkiemu",
    "medievalworldzkim",
    "medievalworldzkimi",
    "midworld",
    "midworldu",
    "midworldzkiej",
    "midworldzka",
    "midworldzie",
    "midworldów",
    "midworldzka",
    "midworldzki",
    "midworldzkich",
    "midworldzkie",
    "midworldzkiego",
    "midworldzkiej",
    "midworldzkiemu",
    "midworldzkim",
    "midworldzkimi",
    "dron",
    "dronach",
    "dronami",
    "dronem",
    "dronie",
    "dronom",
    "dronowi",
    "dronu",
    "drony",
    "dronów",
    "mechy",
    "egzoplanety",
    "egzoplanetą",
    "egzoplanetę",
    "egzoplanecie",
    "egzoplanet",
    "egzoplaneta",
    "egzoplanetach",
    "egzoplanetami",
    "egzoplaneto",
    "egzoplanetom",
    "ksenosocjologia",
    "ksenosocjologiach",
    "ksenosocjologiami",
    "ksenosocjologie",
    "ksenosocjologii",
    "ksenosocjologio",
    "ksenosocjologiom",
    "ksenosocjologią",
    "ksenosocjologię",
    "robocista",
    "robocistach",
    "robocistami",
    "robocisto",
    "robocistom",
    "robocisty",
    "robocistów",
    "robocistą",
    "robocistę",
    "robociści",
    "robociście",
    "mechanicie",
    "mechanit",
    "mechanitach",
    "mechanitami",
    "mechanitem",
    "mechanitom",
    "mechanitowi",
    "mechanitu",
    "mechanity",
    "mechanitów",
    "zrekrutowany",
    "xenohumanoidalna",
    "xenohumanoidalne",
    "xenohumanoidalnego",
    "xenohumanoidalnej",
    "xenohumanoidalnemu",
    "xenohumanoidalni",
    "xenohumanoidalny",
    "xenohumanoidalnych",
    "xenohumanoidalnym",
    "xenohumanoidalnymi",
    "xenohumanoidalną",
    "cybernetyczna",
    "cybernetyczne",
    "cybernetycznego",
    "cybernetycznej",
    "cybernetycznemu",
    "cybernetyczni",
    "cybernetyczno",
    "cybernetyczny",
    "cybernetycznych",
    "cybernetycznym",
    "cybernetycznymi",
    "cybernetyczną",
    "mawoła",
    "mawołach",
    "mawołami",
    "mawołem",
    "mawołom",
    "mawołowi",
    "mawołu",
    "mawoły",
    "mawołów",
    "mawół",
    "xenoczłowiecze",
    "xenoczłowiek",
    "xenoczłowieka",
    "xenoczłowiekiem",
    "xenoczłowiekowi",
    "xenoczłowieku",
    "xenoludzi",
    "xenoludziach",
    "xenoludzie",
    "xenoludziom",
    "xenoludźmi",
    "kowalów",
    "dung",
    "mucker",
    "destriańskiej",
    "vr",
    "glitteropedii",
    "sandy",
    "boomrat",
    "grady",
    "loughman",
    "modelingowa",
    "irithir",
    "technofobicznym",
    "bioetycy",
    "multiplanetarnego",
    "zarthy",
    "zeglar",
    "wielbicielów",
    "ksenobiologii",
    "g-nome",
    "gizmo",
    "zanieszczyszczeniem",
    "headjacka",
    "futrzastych",
    "jaszczurkopodobnych",
    "hiveworld",
    "hiveworldu",
    "hiveworldzkiej",
    "hiveworldzka",
    "hiveworldzie",
    "hiveworldów",
    "hiveworldzka",
    "hiveworldzki",
    "hiveworldzkich",
    "hiveworldzkie",
    "hiveworldzkiego",
    "hiveworldzkiej",
    "hiveworldzkiemu",
    "hiveworldzkim",
    "hiveworldzkimi",
    "vinny",
    "dichterów",
    "terawatowych",
    "zrekrutowana",
    "callos",
    "transptaków",
    "ashmarines",
    "vanu",
    "współzałogantów",
    "deathjacka",
    "pozaplanetarnej",
    "abordażowania",
    "starforce",
    "kalthas",
    "vidtube",
    "aracenie",
    "r&d",
    "mawolą",
    "mosteiro",
    "dos",
    "jerónimos",
    "piratka",
    "socjointelektualną",
    "przysięgła",
    "caspian",
]


def check_str(string):
    url = "https://www.ortograf.pl/js/tiny_mce/plugins/atd-tinymce/server/proxy.php"
    data = {
        "disabled": "WHITESPACE_RULE",
        "text": str(string),
        "language": "pl"
    }
    response = requests.post(url, data)
    if response.status_code != 200:
        print("*******************ERROR***************")
    root = ET.fromstring(response.text)
    for child in root.iter("error"):
        x_from = int(child.attrib["fromx"])
        x_to = int(child.attrib["tox"])
        word = string[x_from:x_to]
        if str(word).lower() in dict_files:
            continue
        result = {
            "msg": child.attrib["msg"],
            "context": child.attrib["context"],
            "word": word
        }
        if len(child.attrib["replacements"]) > 0:
            result["replacements"] = child.attrib["replacements"]
        print(result)


def check_title(title_list):
    threads = []
    world_list = []
    for title in title_list:
        if len(title) > 20:
            print("{} ma więcej niż 20 znaków".format(title))
        world_list.extend(title.split(" "))
    world_list = list(dict.fromkeys(world_list))
    world_list = list(filter(None, world_list))
    for world in world_list:
        world = str(world[0]).upper() + world[1:] + "."
        process = Thread(target=check_str, args=[world])
        process.start()
        threads.append(process)
    for process in threads:
        process.join()


PATTERN = "(\{PAWN_gender \? ?([^:]*): ?([^\}]*) ?\})"


def check_desc(title_list, desc_list):
    men_list = []
    women_list = []
    for i in range(0, len(desc_list)):
        desc = desc_list[i]
        list_gender = re.findall(PATTERN, desc)
        men_str = str(desc).replace("[PAWN_nameDef]", "Kuba").replace("\\n\\n", " ")
        women_str = str(desc).replace("[PAWN_nameDef]", "Aga").replace("\\n\\n", " ")
        for gender in list_gender:
            men_str = men_str.replace(gender[0], gender[1].strip())
            women_str = women_str.replace(gender[0], gender[2].strip())
        men_list.append(men_str)
        women_list.append(women_str)
    for i in range(0, len(title_list)):
        print("**{}**".format(title_list[i]))
        check_str(men_list[i])
        check_str(women_list[i])


# regex - \{PAWN_gender \? ?([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]*) ?: ?([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]*) ?\}

def get_list():
    with open("./../../Backstories/Backstories.xml", 'r', encoding="utf8") as xml_file:
        root = ET.parse(xml_file).getroot()
    title_list = []
    title_short_list = []
    desc_list = []
    for child in root.iter("title"):
        title_list.append(child.text)
    for child in root.iter("titleShort"):
        title_short_list.append(child.text)
    for child in root.iter("desc"):
        desc_list.append(child.text)
    return title_list, title_short_list, desc_list


title_list, title_short_list, desc_list = get_list()
# check_title(title_list)
# check_title(title_short_list)
check_desc(title_list, desc_list)

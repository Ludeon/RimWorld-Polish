import requests
from bs4 import BeautifulSoup, NavigableString
from lxml import etree

BASE_WIKI_URL = "https://pl.wiktionary.org/wiki/"


def get_women_word(word):
    print(word + ":", end=" ")
    word_split = word.split()
    word_change = False
    for w in word_split:
        soup = BeautifulSoup(requests.get(BASE_WIKI_URL + w).text, features="lxml")
        women_form = get_women_form(soup, w)
        if women_form is not None:
            word = word.replace(w, women_form)
            word_change = True
            continue
        women_table = get_world_from_table(soup, w)
        if women_table is not None:
            word = word.replace(w, women_table)
            word_change = True
            continue
        women_form2 = get_women_form2(soup, w)
        if women_form2 is not None:
            word = word.replace(w, women_form2)
            word_change = True
            continue
    if word_change:
        print("- " + word)
        return word
    else:
        print()
        return "TODO"


def get_women_form(soup, w):
    list_dd = soup.find_all("dd")
    for dd in list_dd:
        is_correct = False
        for c in dd.contents:
            if c.name == "i" and c.text == "forma żeńska":
                is_correct = True
                break
        if not is_correct:
            continue
        return dd.find_all("a")[0].text
    return None


def get_women_form2(soup, w):
    list_dd = soup.find_all("dd")
    result = ""
    for dd in list_dd:
        for i in range(0, len(dd.contents)):
            actual = dd.contents[i]
            if actual.name == "a" and i + 3 < len(dd.contents):
                if isinstance(dd.contents[i+3], NavigableString):
                    continue
                is_women = dd.contents[i + 3].find_all("span", {"title": "rodzaj żeński"})
                if len(is_women) > 0:
                    result += actual.text + ","
    if len(result)>1:
        return result[:-1]
    else:
        return None


def get_world_from_table(soup: BeautifulSoup, word):
    div_table = soup.find_all("div", {"class": "collapse-odmiana"})
    if len(div_table) == 0:
        return
    if_is_z = div_table[0].find_all("span", attrs={"class": "short-content"}, text="ż")
    if len(if_is_z) == 0:
        return
    tables = soup.find_all("table", {"style": "border:none;"})
    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 0:
                continue
            if tds[1].string == word:
                if "colspan" in tds[1].attrs:
                    return tds[2].string
                else:
                    return tds[3].string
    return None


with open("./../../Backstories/Backstories.xml", 'r', encoding="utf8") as xml_file:
    file = etree.parse(xml_file)
root = file.getroot()
for item in root:
    titleFemale = etree.Element("titleFemale")
    titleFemale.text = get_women_word(item.find("title").text)
    titleShortFemale = etree.Element("titleShortFemale")
    titleShortFemale.text = get_women_word(item.find("titleShort").text)
    item.insert(2, titleFemale)
    item.insert(5, titleShortFemale)
file.write("./../../Backstories/Backstories2.xml", encoding="utf8", pretty_print=True)

# get_women_word("pomocnik")

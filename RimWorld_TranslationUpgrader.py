import os
import sys
import xml.etree.ElementTree as ET
import shutil
from datetime import date

import rwtutil

__author__ = 'Sakuukuli'


def print_help():
    """ Print information about the script.
    """
    print("RimWorld Translation Upgrader script")
    print("Compares a translation to the templates and adds missing tags and removes obsolete tags.")
    print("Usage: RimWorld_TranslationUpgrader.py <Directory> <Output>, where <Directory> is the translation to upgrade"
          "and <Output> is the output folder.")


# Save the arguments
arguments = sys.argv[1:]
# Save the directory in a variable
if len(arguments) == 2:
    transPath = os.path.abspath(arguments[0])
    outPath = os.path.abspath(arguments[1])
# If incorrect number of arguments then print help
elif not arguments:
    print_help()
    sys.exit(2)
else:
    rwtutil.print_help_error()
    sys.exit(2)

# Check if the entered RimWorld installation folder was correct
if transPath == outPath:  # input and output paths are the same
    print("Input and output directories can't be the same.")
    sys.exit(2)
# input path doesn't exist
if not os.path.exists(transPath):
    print("Directory is invalid.")
    sys.exit(2)
# input path doesn't have 'DefInjected' and 'Keyed' folders
if not (os.path.exists(os.path.join(transPath, "DefInjected")) and os.path.exists(os.path.join(transPath, "Keyed"))):
    print("Directory is invalid.")
    sys.exit(2)
# templates don't exist
if not (os.path.exists("DefInjected") and os.path.exists("Keyed")):
    print("Templates are missing.")
    sys.exit(2)
# check if the output path exists
if os.path.exists(outPath):
    # check if it's empty
    if os.listdir(outPath):
        # if it's not, make a subfolder with the name of the translation
        if os.path.basename(outPath) != os.path.basename(transPath):
            outPath = os.path.join(outPath, os.path.basename(transPath))
        while os.path.exists(outPath):
            outPath += " new"
    else:
        # remove the empty directory for shutil.copytree to create it again
        os.rmdir(outPath)

# Print information about the script
print("--------------------------------------------------------------------")
print("RimWorld Translation Upgrader script")
print("")
print("Translation to upgrade is in \"" + transPath + "\"")
print("Output directory is \"" + outPath + "\"")
print("--------------------------------------------------------------------")
print("")

print("Copying files to output folder...", end=" ")
shutil.copytree(transPath, outPath)
print("OK")

# simplify old format multiline path translations
rwtutil.simplify_path_translations(outPath)

# Go through all the folders one by one
# transPath is the full path to the current def directory, dirnames is a list of directories in the current directory
# and filenames is a list of files

transTagsDict_byTag = rwtutil.collect_tags_and_text_to_dict(outPath)  # List of tags in translation, in a dict with tag as a key and list of tuples of occurences (text, file)
templateTagsDict_byTag = rwtutil.collect_tags_and_text_to_dict(os.curdir)  # List of tags in templates, in a dict with tag as a key and list of tuples of occurences (text, file)
print("")

os.rename(os.path.join(outPath, "DefInjected"), os.path.join(outPath, "DefInjected temp"))
os.rename(os.path.join(outPath, "Keyed"), os.path.join(outPath, "Keyed temp"))

shutil.copytree("DefInjected", os.path.join(outPath, "DefInjected"))
shutil.copytree("Keyed", os.path.join(outPath, "Keyed"))

untranslatedList = []  # List of tags with unmodified texts, in tuples (file, tag, text)
obsoleteList = []  # List of obsolete tags, in tuples (file, tag, text)
unmatchedTags = 0

print("Comparing tags...", end=" ")
for transtag in transTagsDict_byTag.keys():
    if transtag in templateTagsDict_byTag.keys():
        unmatchedTags = len(transTagsDict_byTag[transtag])
        for transtext, transfile in transTagsDict_byTag[transtag]:
            for templatetext, templatefile in templateTagsDict_byTag[transtag]:
                if templatefile == transfile and templatetext == transtext:
                    untranslatedList.append((templatefile, transtag, templatetext))
                    unmatchedTags -= 1
        if unmatchedTags > 0:
            for transtext, transfile in transTagsDict_byTag[transtag]:
                for templatetext, templatefile in templateTagsDict_byTag[transtag]:
                    if templatetext == transtext and (transfile, transtag, transtext) not in untranslatedList:
                        untranslatedList.append((transfile, transtag, transtext))
        unmatchedTags = 0

    else:
        for transtext, transfile in transTagsDict_byTag[transtag]:
            obsoleteList.append((transfile, transtag, transtext))
print("OK")

print("Replacing templates...", end=" ")
temppath = ""
foundExactMatch = False
for dirpath, dirnames, filenames in os.walk(outPath):

    if not (os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected' or os.path.basename(dirpath) == 'Keyed'):
        continue

    for filename in [f for f in filenames if f.endswith('.xml')]:
        if os.path.basename(dirpath) == "Keyed":
            temppath = "Keyed"
        elif os.path.basename(os.path.split(dirpath)[0]) == "DefInjected":
            temppath = os.path.join("DefInjected", os.path.basename(dirpath))

        # os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, filename + ".temp"))

        # Parse the .xml file with ElementTree
        parser = ET.XMLParser(encoding="utf-8")
        defTree = ET.parse(os.path.join(dirpath, filename), parser=parser)
        defRoot = defTree.getroot()

        for child in defRoot:
            if child.tag in transTagsDict_byTag.keys():
                for transtext, transfile in transTagsDict_byTag[child.tag]:
                    temptest = os.path.split(transfile)[1]
                    if os.path.split(transfile)[1] == filename:
                        child.text = transtext
                        foundExactMatch = True
                if not foundExactMatch:
                    child.text = transTagsDict_byTag[child.tag][0][0]
                foundExactMatch = False
            else:
                untranslatedList.append((os.path.join(temppath, filename), child.tag, child.text))

        rwtutil.write_tree_to_file(defTree, filename, dirpath)

print("OK")
print("")

untranslatedNum = len(untranslatedList)
obsoleteNum = len(obsoleteList)

untranslatedList = rwtutil.sort_list_of_tags_by_file(untranslatedList)
obsoleteList = rwtutil.sort_list_of_tags_by_file(obsoleteList)

if untranslatedList:
    untranslatedFile = open(os.path.join(outPath, "untranslated-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+', encoding="utf8")

    untranslatedFile.write("List of untranslated tags in this translation. It includes tags which have the same \n"
                           "appearance as their english equivalents, such as 'dementia' and 'tundra'.\n\n")
    for file, taglist in untranslatedList:
        untranslatedFile.write(file + "\n")
        for tag, text in taglist:
            untranslatedFile.write("    <" + tag + ">" + text + "</" + tag + ">\n")
        untranslatedFile.write("\n")

    untranslatedFile.close()

if obsoleteList:
    obsoleteFile = open(os.path.join(outPath, "obsolete-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+', encoding="utf8")

    obsoleteFile.write("List of obsolete tags in this translation. These tags have been removed from the game \n"
                       "or have changed their name.\n\n")
    for file, taglist in obsoleteList:
        obsoleteFile.write(file + "\n")
        for tag, text in taglist:
            obsoleteFile.write("    <" + tag + ">" + text + "</" + tag + ">\n")
        obsoleteFile.write("\n")

    obsoleteFile.close()

shutil.rmtree(os.path.join(outPath, "DefInjected temp"))
shutil.rmtree(os.path.join(outPath, "Keyed temp"))

print("Upgrade complete! Found {} untranslated tags and {} obsolete tags.".format(untranslatedNum, obsoleteNum))

import os
import sys
import xml.etree.ElementTree as ET
import shutil
import rwtutil

from datetime import date

__author__ = 'Sakuukuli'


def print_help():
    """ Print information about the script.
    """
    print("RimWorld Translation Upgrader script")
    print("Compares a translation to the templates and adds missing tags and removes obsolete tags.")
    print(
            "Usage: RimWorld_TranslationUpgrader.py <Directory> <Output>, where <Directory> is the translation to upgrade and <Output> is the output folder.")


def print_help_error():
    """ Print information about the script in case of incorrect usage.
    """
    print("")
    print("Invalid number of arguments.")
    print("REMEMBER: Enclose folder names in double quotes.")


def print_progress(message, progress, total):
    """Prints the number of files processed, total number of files and a percentage.

    Replaces itself automatically and animates.
    The format is progress/total percent%

    :param message: Progress label
    :param progress: Number of files processed
    :param total: Total number of files
    """
    # Calculate the percent, multiply with 1.0 to force floating point math
    percent = 1.0 * progress / total
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}: {}/{} {}%'.format(message, progress, total, round(percent * 100)))
    sys.stdout.flush()


def print_counter(message, progress):
    """Prints the number of files processed, total number of files and a percentage.

    Replaces itself automatically and animates.
    The format is progress/total percent%

    :param message: Progress label
    :param progress: Number of files processed
    """
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}: {}'.format(message, progress))
    sys.stdout.flush()


def collect_tags_and_text(translationdir):
    """Collect tags in a translation folder into a dict

    Dict has tags as keys and each tag has a list of tuples (text, file) as occurences

    :param translationdir:
    :return:
    """
    tempdict = {}
    temppath = ""
    for dirpath, dirnames, filenames in os.walk(translationdir):

        if not (os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected' or os.path.basename(dirpath) == 'Keyed'):
            continue

        # Go through all the files one by one
        for filename in [f for f in filenames if f.endswith('.xml')]:
            if os.path.basename(dirpath) == "Keyed":
                temppath = "Keyed"
            elif os.path.basename(os.path.split(dirpath)[0]) == "DefInjected":
                temppath = os.path.join("DefInjected", os.path.basename(dirpath))

            # Parse the .xml file with ElementTree
            deffile = ET.parse(os.path.join(dirpath, filename))
            defroot = deffile.getroot()

            for child in defroot:
                if child.tag not in tempdict.keys():
                    tempdict[child.tag] = [(child.text, os.path.join(temppath, filename))]
                else:
                    tempdict[child.tag].append((child.text, os.path.join(temppath, filename)))
        if translationdir == ".":
            print_counter("Collecting tags from templates", len(tempdict))
        else:
            print_counter("Collecting tags from " + translationdir, len(tempdict))

    return tempdict


def sort_tags_and_text_by_file(file_tag_list):
    filelist = []
    filetaglist = []
    newlist = []

    for file, tag, text in file_tag_list:
        if file not in filelist:
            filelist.append(file)

    for file in filelist:
        for f, tag, text in file_tag_list:
            if f == file:
                filetaglist.append((tag, text))

        newlist.append((file, filetaglist))
        filetaglist = []

    return sorted(newlist)


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
    print_help_error()
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

transTagsDict_byTag = collect_tags_and_text(
        outPath)  # List of tags in translation, in a dict with tag as a key and list of tuples of occurences (text, file)
print("")
templateTagsDict_byTag = collect_tags_and_text(
        os.curdir)  # List of tags in templates, in a dict with tag as a key and list of tuples of occurences (text, file)
print("")
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
                    untranslatedList.append((transfile, transtag, transtext))
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

        os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, filename + ".temp"))

        # Parse the .xml file with ElementTree
        defFile = ET.parse(os.path.join(dirpath, filename + ".temp"))
        defRoot = defFile.getroot()

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

        defFile.write(os.path.join(dirpath, filename), encoding="utf-8", xml_declaration=True)

        os.remove(os.path.join(dirpath, filename + ".temp"))
print("OK")
print("")

untranslatedNum = len(untranslatedList)
obsoleteNum = len(obsoleteList)

untranslatedList = sort_tags_and_text_by_file(untranslatedList)
obsoleteList = sort_tags_and_text_by_file(obsoleteList)

if untranslatedList:
    untranslatedFile = open(os.path.join(outPath, "untranslated-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+')

    untranslatedFile.write("List of untranslated tags in this translation. It includes tags which have the same \n"
                           "appearance as their english equivalents, such as 'dementia' and 'tundra'.\n\n")
    for file, taglist in untranslatedList:
        untranslatedFile.write(file + "\n")
        for tag, text in taglist:
            untranslatedFile.write("    <" + tag + ">" + text + "<" + tag + ">\n")
        untranslatedFile.write("\n")

    untranslatedFile.close()

if obsoleteList:
    obsoleteFile = open(os.path.join(outPath, "obsolete-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+')

    obsoleteFile.write("List of obsolete tags in this translation. These tags have been removed from the game \n"
                       "or have changed their name.\n\n")
    for file, taglist in obsoleteList:
        obsoleteFile.write(file + "\n")
        for tag, text in taglist:
            obsoleteFile.write("    <" + tag + ">" + text + "<" + tag + ">\n")
        obsoleteFile.write("\n")

    obsoleteFile.close()

shutil.rmtree(os.path.join(outPath, "DefInjected temp"))
shutil.rmtree(os.path.join(outPath, "Keyed temp"))

print("Upgrade complete! Found {} untranslated tags and {} obsolete tags.".format(untranslatedNum, obsoleteNum))

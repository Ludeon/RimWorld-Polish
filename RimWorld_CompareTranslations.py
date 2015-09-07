import os
import sys
import xml.etree.ElementTree as ETree

__author__ = 'Sakuukuli'


def print_help():
    """ Print information about the script.
    """
    print("RimWorld Translation Comparison Script")
    print("Compares two translation directories and finds differences in tags.")
    print("Usage: RimWorld_CompareTranslations.py <Directory 1> <Directory 2>")


def print_help_error():
    """ Print information about the script in case of incorrect usage.
    """
    print("")
    print("Invalid number of arguments.")
    print("Enclose folder names in double quotes.")


def collect_tags(translationdir):
    """

    :param translationdir:
    :return:
    """
    templist = []
    for dirpath, dirnames, filenames in os.walk(translationdir):

        if os.path.basename(dirpath) == 'Keyed':
            # Go through all the files one by one
            for filename in [f for f in filenames if f.endswith('.xml')]:

                # Parse the .xml file with ElementTree
                deffile = ETree.parse(os.path.join(dirpath, filename))
                defroot = deffile.getroot()

                for child in defroot:
                    templist.append((os.path.join('Keyed', filename), child.tag))

        if os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected':
            # Go through all the files one by one
            for filename in [f for f in filenames if f.endswith('.xml')]:

                # Parse the .xml file with ElementTree
                deffile = ETree.parse(os.path.join(dirpath, filename))
                defroot = deffile.getroot()

                for child in defroot:
                    templist.append((os.path.join('DefInjected', os.path.basename(dirpath), filename), child.tag))

    return templist


def sort_tags_by_file(file_tag_list):
    filelist = []
    filetaglist = []
    newlist = []

    for file, tag in file_tag_list:
        if file not in filelist:
            filelist.append(file)

    for file in filelist:
        for f, tag in file_tag_list:
            if f == file:
                filetaglist.append(tag)

        newlist.append((file, filetaglist))
        filetaglist = []

    return newlist


# Save the arguments
arguments = sys.argv[1:]
# Save the directories in variables
if len(arguments) == 2:
    firstDirPath = arguments[0]
    secondDirPath = arguments[1]
# If incorrect number of arguments then print help
elif not arguments:
    print_help()
    sys.exit(2)
else:
    print_help_error()
    sys.exit(2)

# Print information about the script
print("--------------------------------------------------------------------")
print("RimWorld Translation Comparison Script")
print("")
print("Directory 1 is \"" + firstDirPath + "\"")
print("Directory 2 is \"" + secondDirPath + "\"")
print("--------------------------------------------------------------------")
print("")

# Check if the entered RimWorld installation folder was correct
if not os.path.exists(firstDirPath):
    print("Directory 1 is invalid.")
    sys.exit(2)
elif not os.path.exists(secondDirPath):
    print("Directory 2 is invalid.")
    sys.exit(2)

# Go through all the folders one by one
# dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
# and filenames is a list of files

firstList = collect_tags(firstDirPath)
secondList = collect_tags(secondDirPath)

firstUnique = []
secondUnique = []

for element in firstList:
    if element not in secondList:
        firstUnique.append(element)

for element in secondList:
    if element not in firstList:
        secondUnique.append(element)

firstUnique = sort_tags_by_file(firstUnique)
secondUnique = sort_tags_by_file(secondUnique)

print("Tags only in \"" + firstDirPath + "\":")
for file, taglist in firstUnique:
    print("    " + file)
    for tag in taglist:
        print("        " + tag)
print("Tags only in \"" + secondDirPath + "\":")
for file, taglist in secondUnique:
    print("    " + file)
    for tag in taglist:
        print("        " + tag)
print("")

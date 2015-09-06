import os
import sys
import xml.etree.ElementTree as ETree

__author__ = 'Sakuukuli'


def printhelp():
    """ Print information about the script.
    """
    print("RimWorld Translation Comparison Script")
    print("Compares two translation directories and finds differences in tags.")
    print("Usage: RimWorld_CompareTranslations.py <Directory 1> <Directory 2>")


def printhelperror():
    """ Print information about the script in case of incorrect usage.
    """
    print("")
    print("Invalid number of arguments.")
    print("Enclose folder names in double quotes.")


def list_tags(translationdir):
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
                    templist.append((child.tag, os.path.join('Keyed', filename)))

        if os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected':
            # Go through all the files one by one
            for filename in [f for f in filenames if f.endswith('.xml')]:

                # Parse the .xml file with ElementTree
                deffile = ETree.parse(os.path.join(dirpath, filename))
                defroot = deffile.getroot()

                for child in defroot:
                    templist.append((child.tag, os.path.join('DefInjected', os.path.basename(dirpath), filename)))

    return templist


# Save the arguments
arguments = sys.argv[1:]
# Save the directories in variables
if len(arguments) == 2:
    firstDirPath = arguments[0]
    secondDirPath = arguments[1]
# If incorrect number of arguments then print help
elif not arguments:
    printhelp()
    sys.exit(2)
else:
    printhelperror()
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

firstList = list_tags(firstDirPath)
secondList = list_tags(secondDirPath)

firstUnique = []
secondUnique = []

for element in firstList:
    if element not in secondList:
        firstUnique.append(element)

for element in secondList:
    if element not in firstList:
        secondUnique.append(element)


print(firstUnique)
print(secondUnique)
print("")

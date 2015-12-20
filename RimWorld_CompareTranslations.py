import os
import sys
import xml.etree.ElementTree as ET

import rwtutil

__author__ = 'Sakuukuli'


def print_help():
    """ Print information about the script.
    """
    print("RimWorld Translation Comparison Script")
    print("Compares two translation directories and finds differences in tags.")
    print("Usage: RimWorld_CompareTranslations.py <Directory 1> <Directory 2>")


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
    rwtutil.print_help_error()
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

print("Collecting tags...")
firstDict = rwtutil.collect_tags_and_text_to_dict(firstDirPath)
print("{} tags found in the first directory.".format(len(firstDict)))
secondDict = rwtutil.collect_tags_and_text_to_dict(secondDirPath)
print("{} tags found in the second directory.".format(len(secondDict)))
print("")

print("Comparing directories...", end=' ')
firstUniqueList = []
secondUniqueList = []

for tag in firstDict.keys():
    if tag not in secondDict.keys():
        for text, file in firstDict[tag]:
            firstUniqueList.append((tag, text, file))
    # print_progress('Comparing the first directory to the second one', i, len(firstList))

for tag in secondDict.keys():
    if tag not in firstDict.keys():
        for text, file in secondDict[tag]:
            secondUniqueList.append((tag, text, file))
    # print_progress('Comparing the second directory to the first one', i, len(firstList))
print("OK")

firstUniqueList = rwtutil.sort_list_of_tags_by_file(firstUniqueList)
print("{} tags unique to the first directory.".format(len(firstUniqueList)))
secondUniqueList = rwtutil.sort_list_of_tags_by_file(secondUniqueList)
print("{} tags unique to the second directory.".format(len(secondUniqueList)))
print("")

if firstUniqueList:
    print("Tags only in \"" + firstDirPath + "\":")
    for file, taglist in firstUniqueList:
        print("    " + file)
        for tag, text in taglist:
            print("        " + tag)
    print("")
if secondUniqueList:
    print("Tags only in \"" + secondDirPath + "\":")
    for file, taglist in secondUniqueList:
        print("    " + file)
        for tag, text in taglist:
            print("        " + tag)
print("")

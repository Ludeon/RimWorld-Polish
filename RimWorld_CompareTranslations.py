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


def print_progress(message, progress, total):
    """Prints the number of files processed, total number of files and a percentage.

    Replaces itself automatically and animates.
    The format is progress/total percent%

    :param progress: Number of files processed
    :param total: Total number of files
    """
    # Calculate the percent, multiply with 1.0 to force floating point math
    percent = 1.0 * progress / total
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}: {}/{} {}%'.format(message, progress, total, round(percent * 100)))
    sys.stdout.flush()


def collect_tags(translationdir):
    """

    :param translationdir:
    :return:
    """
    templist = []
    temppath = ""
    for dirpath, dirnames, filenames in os.walk(translationdir):

        for filename in [f for f in filenames if f.endswith('.xml')]:
            if os.path.basename(dirpath) == "Keyed":
                temppath = "Keyed"
            elif os.path.basename(os.path.split(dirpath)[0]) == "DefInjected":
                temppath = os.path.join("DefInjected", os.path.basename(dirpath))

            # Parse the .xml file with ElementTree
            deffile = ETree.parse(os.path.join(dirpath, filename))
            defroot = deffile.getroot()

            for child in defroot:
                templist.append((os.path.join(temppath, filename), child.tag))

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

print("Collecting tags...")
firstList = collect_tags(firstDirPath)
print("{} tags found in the first directory.".format(len(firstList)))
secondList = collect_tags(secondDirPath)
print("{} tags found in the second directory.".format(len(secondList)))
print("")

print("Comparing directories...")
firstUnique = []
secondUnique = []

for i, element in enumerate(firstList):
    if element not in secondList:
        firstUnique.append(element)
    # print_progress('Comparing the first directory to the second one', i, len(firstList))

for i, element in enumerate(secondList):
    if element not in firstList:
        secondUnique.append(element)
    # print_progress('Comparing the second directory to the first one', i, len(firstList))

firstUnique = sort_tags_by_file(firstUnique)
print("{} tags unique to the first directory.".format(len(firstUnique)))
secondUnique = sort_tags_by_file(secondUnique)
print("{} tags unique to the second directory.".format(len(secondUnique)))
print("")

if firstUnique:
    print("Tags only in \"" + firstDirPath + "\":")
    for file, taglist in firstUnique:
        print("    " + file)
        for tag in taglist:
            print("        " + tag)
    print("")
if secondUnique:
    print("Tags only in \"" + secondDirPath + "\":")
    for file, taglist in secondUnique:
        print("    " + file)
        for tag in taglist:
            print("        " + tag)
print("")

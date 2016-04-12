import os
import sys
import xml.etree.ElementTree as ET
from datetime import date

import rwtutil

__author__ = 'Sakuukuli'


def print_help():
    """ Print information about the script.
    """
    print("RimWorld Translation Change Comparison Script")
    print("Compares two translation directories and finds tags whose text has changed.")
    print("Usage: RimWorld_FindChanged.py <Directory 1> <Directory 2>")


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
changedlist = []
renamedlist = []
movedlist = []

for firsttag in firstDict.keys():
    if firsttag in secondDict.keys():
        for firsttext, firstfile in firstDict[firsttag]:
            for secondtext, secondfile in secondDict[firsttag]:
                if secondfile == firstfile and secondtext != firsttext:
                    changedlist.append(((firstfile, firsttag, firsttext), (firstfile, firsttag, secondtext)))
                elif secondfile != firstfile:
                    movedlist.append(((firstfile, firsttag, firsttext), (firstfile, firsttag, secondtext)))

    else:
        for firsttext, firstfile in firstDict[firsttag]:
            for secondtag in secondDict.keys():
                for secondtext, secondfile in secondDict[secondtag]:
                    if firsttext == secondtext and firstfile == secondfile and firsttag != secondtag:
                        renamedlist.append(((firstfile, firsttag, firsttext), (secondfile, secondtag, secondtext)))


print("OK")
print("")

changedlist = rwtutil.sort_list_of_changes_by_file(changedlist)
# renamedlist = rwtutil.sort_list_of_tags_by_file(renamedlist)
# movedlist = rwtutil.sort_list_of_tags_by_file(movedlist)

if changedlist:
    changedFile = open(os.path.join(firstDirPath, "changed-from-" + os.path.basename(secondDirPath) + "-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+', encoding="utf8")

    changedFile.write("List of tags that have changed text in them. Comparing changes from \"" + secondDirPath + "\" to \"" + firstDirPath + "\".\n\n")
    for (firstfile, taglist) in changedlist:
        changedFile.write(firstfile + "\n")
        for firsttag, firsttext, secondtext in taglist:
            changedFile.write("    TAG " + firsttag + " TEXT: \n        " + secondtext + " CHANGED TO " + firsttext + "\n")
        changedFile.write("\n")

    changedFile.close()
#
# if movedlist:
#     obsoleteFile = open(os.path.join(firstDirPath, "obsolete-" + date.today().strftime("%Y-%m-%d") + ".txt"), 'w+', encoding="utf8")
#
#     obsoleteFile.write("List of obsolete tags in this translation. These tags have been removed from the game \n"
#                        "or have changed their name.\n\n")
#     for file, taglist in movedlist:
#         obsoleteFile.write(file + "\n")
#         for tag, text in taglist:
#             obsoleteFile.write("    <" + tag + ">" + text + "</" + tag + ">\n")
#         obsoleteFile.write("\n")
#
#     obsoleteFile.close()

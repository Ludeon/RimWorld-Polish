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
# Save the directory in a variable
if len(arguments) == 1:
    dirPath = arguments[0]
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
print("Directory is \"" + dirPath + "\"")
print("--------------------------------------------------------------------")
print("")

# Check if the entered RimWorld installation folder was correct
if not os.path.exists(dirPath):
    print("Directory is invalid.")
    sys.exit(2)
elif not (os.path.exists("DefInjected") and os.path.exists("Keyed")):
    print("Templates are invalid.")
    sys.exit(2)

# Go through all the folders one by one
# dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
# and filenames is a list of files

transDict = rwtutil.collect_tags_and_text_to_dict(dirPath)
templateDict = rwtutil.collect_tags_and_text_to_dict(os.curdir)

print("Comparing directories...", end=' ')
untranslatedList = []

for transtag in transDict.keys():
    if transtag in templateDict.keys():
        unmatchedTags = len(transDict[transtag])
        for transtext, transfile in transDict[transtag]:
            for templatetext, templatefile in templateDict[transtag]:
                if templatefile == transfile and templatetext == transtext:
                    untranslatedList.append((transfile, transtag, transtext))
                    unmatchedTags -= 1
        if unmatchedTags > 0:
            for transtext, transfile in transDict[transtag]:
                for templatetext, templatefile in templateDict[transtag]:
                    if templatetext == transtext and (transfile, transtag, transtext) not in untranslatedList:
                        untranslatedList.append((transfile, transtag, transtext))
        unmatchedTags = 0

print("OK")
print("")

untranslatedList = rwtutil.sort_list_of_tags_by_file(untranslatedList)

if untranslatedList:
    print("Untranslated tags in \"" + dirPath + "\":")
    for file, taglist in untranslatedList:
        print("    " + file)
        for tag, text in taglist:
            print("        " + tag + ": " + text)  # with text
            # print("        " + tag)  # no text
    print("")
print("")

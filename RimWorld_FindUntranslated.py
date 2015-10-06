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


def collect_tags_and_text(translationdir):
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
                    templist.append((os.path.join('Keyed', filename), child.tag, child.text))

        if os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected':
            # Go through all the files one by one
            for filename in [f for f in filenames if f.endswith('.xml')]:

                # Parse the .xml file with ElementTree
                deffile = ETree.parse(os.path.join(dirpath, filename))
                defroot = deffile.getroot()

                for child in defroot:
                    templist.append((os.path.join('DefInjected', os.path.basename(dirpath), filename), child.tag, child.text))

    return templist


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

    return newlist


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
    print_help_error()
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
    print("Directory 1 is invalid.")
    sys.exit(2)
elif not (os.path.exists("DefInjected") and os.path.exists("Keyed")):
    print("Templates are invalid.")
    sys.exit(2)

# Go through all the folders one by one
# dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
# and filenames is a list of files

print("Collecting tags...")
firstList = collect_tags_and_text(dirPath)
print("{} tags found in the first directory.".format(len(firstList)))
secondList = collect_tags_and_text(os.curdir)
print("{} tags found in the second directory.".format(len(secondList)))
print("")

print("Comparing directories...")
untranslated = []

for firstfile, firsttag, firsttext in firstList:
    for secondfile, secondtag, secondtext in secondList:
        if firsttag == secondtag and firsttext == secondtext:
            untranslated.append((firstfile, firsttag, firsttext))

untranslated = sort_tags_and_text_by_file(untranslated)

if untranslated:
    print("Untranslated tags in \"" + dirPath + "\":")
    for file, taglist in untranslated:
        print("    " + file)
        for tag, text in taglist:
            print("        " + tag + ": " + text)
    print("")
print("")

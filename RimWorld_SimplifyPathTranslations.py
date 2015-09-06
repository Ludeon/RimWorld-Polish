import os
import sys
import xml.etree.ElementTree as ETree

__author__ = 'Sakuukuli'


def printhelp():
    """ Print information about the script.
    """
    print("RimWorld Path Translation Simplification Script")
    print("Simplifies multi-line path translations to the new simpler syntax.")
    print("Usage: RimWorld_SimplifyPathTranslations.py <Directory>")


def printhelperror():
    """ Print information about the script in case of incorrect usage.
    """
    print("")
    print("Invalid number of arguments.")
    print("Enclose folder names in double quotes.")


def format_path(path):
    path = path.replace('[', '.')
    path = path.replace(']', '')
    return path


def replace_escapechars(text):
    escapechars = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>'}
    for i, j in escapechars.items():
        text = text.replace(i, j)
    return text


# Save the arguments
arguments = sys.argv[1:]
# Save the directories in variables
if len(arguments) == 1:
    translationDirPath = arguments[0]
# If incorrect number of arguments then print help
elif not arguments:
    printhelp()
    sys.exit(2)
else:
    printhelp()
    printhelperror()
    sys.exit(2)

# Print information about the script
print("--------------------------------------------------------------------")
print("RimWorld Translation Comparison Script")
print("")
print("Directory is \"" + translationDirPath + "\"")
print("--------------------------------------------------------------------")
print("")

translationDirPath = os.path.join(translationDirPath, 'DefInjected')

# Check if the entered RimWorld installation folder was correct
if not os.path.exists(translationDirPath):
    print("Directory is invalid.")
    sys.exit(2)

# Go through all the folders one by one
# dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
# and filenames is a list of files

for dirpath, dirnames, filenames in os.walk(translationDirPath):

    for filename in [f for f in filenames if f.endswith('.xml')]:

        # Parse the .xml file with ElementTree
        defFile = ETree.parse(os.path.join(dirpath, filename))
        defRoot = defFile.getroot()

        tempfilename = filename + '.temp'

        if defRoot.find('rep'):
            for index, repElement in enumerate(defRoot):
                if repElement.tag == 'rep':
                    path = repElement.find('path').text
                    trans = repElement.find('trans').text
                    whitespace = repElement.tail

                    path = format_path(path)

                    defRoot.remove(repElement)

                    defRoot.insert(index, ETree.Element(path))
                    defRoot[index].text = trans
                    defRoot[index].tail = whitespace

            defFile.write(os.path.join(dirpath, tempfilename), encoding="utf-8", xml_declaration=False, method="html")

            defFile = open(os.path.join(dirpath, filename), 'w+')
            processedFile = open(os.path.join(dirpath, tempfilename), 'r')
            processedFileText = replace_escapechars(processedFile.read())
            defFile.write('<?xml version="1.0" encoding="utf-8" ?>\n')
            defFile.write(processedFileText)
            defFile.write('\n')

            defFile.close()
            processedFile.close()

            os.remove(os.path.join(dirpath, tempfilename))

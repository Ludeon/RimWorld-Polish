import os
import sys
import xml.etree.ElementTree as ET

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
    """Changes a path to a tag from 'rulesStrings[0]' to 'rulesStrings.0'.

    :param path: A path as a string
    :return: Formatted path
    """
    path = path.replace('[', '.')
    path = path.replace(']', '')
    return path


def replace_escapechars(text):
    """ Replaces HTML escape characters with their real equivalents.

    :param text: Text to format
    :return: Formatted text
    """
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
print("RimWorld Path Simplification Script")
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

    # Only parse .xml files
    for filename in [f for f in filenames if f.endswith('.xml')]:

        # Parse the .xml file with ElementTree
        defTree = ET.parse(os.path.join(dirpath, filename))
        defRoot = defTree.getroot()

        # Check if the file has path translations
        if defRoot.find('rep'):
            # Go through all the elements in the xml file
            for index, repElement in enumerate(defRoot):
                # Check if this element is a path translation
                if repElement.tag == 'rep':
                    # Store the information in the element
                    path = repElement.find('path').text
                    trans = repElement.find('trans').text
                    whitespace = repElement.tail

                    # Change the path to the new format
                    path = format_path(path)

                    # Remove the element in the old format
                    defRoot.remove(repElement)

                    # Insert an element in the new format in its place
                    defRoot.insert(index, ET.Element(path))
                    defRoot[index].text = trans
                    defRoot[index].tail = whitespace

            # Write the tree into a temporary file
            tempfilename = filename + '.temp'
            # Do not add a header, because it will be '<?xml version='1.0' encoding='utf-8'?>\n'
            defTree.write(os.path.join(dirpath, tempfilename), encoding="utf-8", xml_declaration=False)

            # Open the file for writing
            defFile = open(os.path.join(dirpath, filename), 'w+')
            tempFile = open(os.path.join(dirpath, tempfilename), 'r')
            # Add header in the RimWorld way
            defFile.write('<?xml version="1.0" encoding="utf-8" ?>\n')
            defFile.write(replace_escapechars(tempFile.read()))
            defFile.write('\n')

            # Clean up
            defFile.close()
            tempFile.close()
            os.remove(os.path.join(dirpath, tempfilename))

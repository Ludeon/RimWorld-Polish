import os
import sys
import xml.etree.ElementTree as ETree

__author__ = 'Sakuukuli'


def printhelp():
    print("RimWorld Translation Template Script")
    print("Copies all Def's from the RimWorld Core mod folder and creates DefInject templates for them.")
    print("Usage: RimWorld_DefsToDefInject.py <RimWorld installation folder> <Folder for templates>")
    print("")
    print("Invalid number of arguments.")


def update_progress(progress, total):
    percent = 1.0 * progress / total
    sys.stdout.write('\r{}/{} {}%'.format(progress, total, round(percent * 100)))
    sys.stdout.flush()


def writeheader(file):
    """ Writes the first lines of a DefInjected file.
    Arguments:
        filename: name of the file to write to
    """
    file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    file.write('<LanguageData>\n')
    file.write('    \n')


def writedeflabel(file, labeltype, defname, deflabel):
    """ Writes the translation data of a DefInjected file in the correct syntax:
    <Ocean.label>ocean</Ocean.label>
    <Ocean.description>Open ocean. Great for fish - not so great for you.</Ocean.description>

    Arguments:
        filename: Name of the file to write to
        labelType: A designation string for the label, for example 'description'
        defname: The name of the def the label belongs to
        deflabel: The untranslated text in the label
    """
    file.write('    <' + defname + '.' + labeltype + '>' + deflabel + '</' + defname + '.' + labeltype + '>\n')


def writefooter(file):
    """ Writes the last lines of a DefInjected file.
    Arguments:
        filename: Name of the file to write to
    """
    file.write('</LanguageData>\n')


# Save the arguments
arguments = sys.argv[1:]
# Save the directories in variables
if len(arguments) == 2:
    defsDirPath = arguments[0]
    translationDirPath = arguments[1]
# If no directories entered then print help
else:
    printhelp()
    sys.exit(2)

# Print information about the script
print("--------------------------------------------------------------------")
print("RimWorld Translation Template Script")
print("")
print("RimWorld installation folder is \"" + defsDirPath + "\"")
print("Templates will be created in folder \"" + translationDirPath + "\"")
print("--------------------------------------------------------------------")
print("")

# Move to the directories where the files are
defsDirPath += '\\Mods\\Core\\Defs'
translationDirPath += '\\DefInjected'

# Define list of labels that need to be translated
labels = ['label', 'description', 'pawnLabel', 'gerundLabel', 'skillLabel', 'reportString', 'verb', 'gerund',
          'deathMessage', 'pawnsPlural', 'jobString', 'quotation', 'beginLetterLabel', 'beginLetter', 'recoveryMessage',
          'inspectLine', 'graphLabelY', 'labelMechanoids', 'labelShort', 'fixedName', 'letterLabel', 'letterText',
          'letterLabelEnemy', 'arrivalTextEnemy', 'letterLabelFriendly', 'arrivalTextFriendly']

# Check if the entered RimWorld installation folder was correct
if os.path.exists(defsDirPath):

    print("Valid installation folder.")
    print("")

    # Create the translation folder
    if not os.path.exists(translationDirPath):
        os.makedirs(translationDirPath)

    numfiles = 0
    for p, d, fs in os.walk(defsDirPath):
        for f in fs:
            if f.endswith('.xml'):
                numfiles += 1

    # Start going through all the folders
    # dirpath is the full path to the current def directory
    index = 0
    # sys.stdout.write('\r1/{} 0%'.format(numfiles))
    # sys.stdout.flush()
    for dirpath, dirnames, filenames in os.walk(defsDirPath):

        # Save the name of the directory to create, but remove the s at the end
        # ThingDefs -> ThingDef
        defInjectDirectory = os.path.basename(dirpath)[:-1]

        for filename in [f for f in filenames if f.endswith('xml')]:

            defFile = ETree.parse(os.path.join(dirpath, filename))
            defRoot = defFile.getroot()

            # Assume that the file doesn't have anything to translate
            haslabels = False
            # Go through the lines one by one and check if there is something to translate
            # If there is, change haslabels to True and stop searching
            # Some of the things to translate are either uppercase or lowercase
            for child in defRoot:
                for label in labels:
                    if child.find(label) is not None:
                        haslabels = True
                        break
                if haslabels:
                    break

            # If the file has something to traslate
            if haslabels:

                # Create the directory in the translationDir if it doesn't exist
                if not os.path.exists(os.path.join(translationDirPath, defInjectDirectory)):
                    os.mkdir(os.path.join(translationDirPath, defInjectDirectory))

                # Assume that an already existing file is incorrect
                # and remove it to start fresh
                if os.path.exists(os.path.join(translationDirPath, defInjectDirectory, filename)):
                    os.remove(os.path.join(translationDirPath, defInjectDirectory, filename))

                # Open the file for writing
                defInjectFile = open(os.path.join(translationDirPath, defInjectDirectory, filename), 'w+')

                # Write the header of the file
                writeheader(defInjectFile)

                labelDict = []
                defName = ""
                # Start going through the file line by line
                for child in defRoot:
                    defElement = child.find('defName')
                    if defElement is not None:
                        defName = defElement.text
                    else:
                        defElement = child.find('DefName')
                        if defElement is not None:
                            defName = defElement.text
                    for label in labels:
                        labelElement = child.find(label)
                        if labelElement is not None:
                            labelDict.append((labelElement.tag, labelElement.text))
                    for label, text in labelDict:
                        writedeflabel(defInjectFile, label, defName, text)
                        labelDict = []

                    # Move to the next line in the template
                    defInjectFile.write('    \n')

                # Clean up after parsing the file
                # Write the end of the xml file
                writefooter(defInjectFile)
                # Close the translateable file
                defInjectFile.close()

            index += 1

            update_progress(index, numfiles)

else:
    print("Invalid RimWorld installation folder.")
    sys.exit(2)

print("")
print("")

print("Succesfully processed all files.")

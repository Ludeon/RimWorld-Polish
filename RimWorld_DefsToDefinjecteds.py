import os
import sys
import xml.etree.ElementTree as ETree

__author__ = 'Sakuukuli'


def printhelp():
    """ Print information about the script in case of incorrect usage.
    :return:
    """
    print("RimWorld Translation Template Script")
    print("Copies all Def's from the RimWorld Core mod folder and creates DefInject templates for them.")
    print("Usage: RimWorld_DefsToDefInjecteds.py <RimWorld installation folder> <Folder for templates>")


def printhelperror():
    """ Print information about the script in case of incorrect usage.
    :return:
    """
    print("")
    print("Invalid number of arguments.")
    print("Enclose folder names in double quotes.")


def print_progress(progress, total):
    """Prints the number of files processed, total number of files and a percentage.

    Replaces itself automatically and animates.
    The format is progress/total percent%
    :param progress: Number of files processed
    :param total: Total number of files
    :return:
    """
    # Calculate the percent, multiply with 1.0 to force floating point math
    percent = 1.0 * progress / total
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}/{} {}%'.format(progress, total, round(percent * 100)))
    sys.stdout.flush()


def writeheader(file):
    """Writes the first lines of a DefInjected file.
    :param file: File to write to
    :return:
    """
    file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    file.write('<LanguageData>\n')
    file.write('    \n')


def writedeflabel(file, defname, labeltype, deflabel):
    """ Writes the translation data of a DefInjected file in the correct syntax:
    <Ocean.label>ocean</Ocean.label>
    <Ocean.description>Open ocean. Great for fish - not so great for you.</Ocean.description>
    :param file: File to write to
    :param defname: Name of the Def to write
    :param labeltype: Tag of the label to write
    :param deflabel: Text inside tags
    :return:
    """
    # Revert capitalization
    labeltype = labeltype[:1].lower() + labeltype[1:]
    file.write('    <' + defname + '.' + labeltype + '>' + deflabel + '</' + defname + '.' + labeltype + '>\n')


def writepathreplace(file, defname, path, text):
    """ Writes the translation data of a DefInjected file.

    Uses the new simplified syntax:
    <Misc.comps.0.labelTreatedWell>bandaged</Misc.comps.0.labelTreatedWell>

    :param file: File to write to
    :param defname: Name of the Def to write
    :param path: Path to the label to write
    :param text: Text inside tags
    """
    file.write('    <' + defname + '.' + path + '>' + text + '</' + defname + '.' + path + '>\n')


def writefooter(file):
    """ Writes the last lines of a DefInjected file.
    :param file: File to write to
    :return:
    """
    file.write('</LanguageData>\n')


# Save the arguments
arguments = sys.argv[1:]
# Save the directories in variables
if len(arguments) == 2:
    defsDirPath = arguments[0]
    translationDirPath = arguments[1]
# If incorrect number of arguments then print help
elif len(arguments) == 0:
    printhelp()
    sys.exit(2)
else:
    printhelperror()
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
labels = ['label', 'labelMechanoids', 'labelShort', 'skillLabel', 'description', 'pawnLabel', 'gerundLabel', 'reportString', 'verb', 'gerund',
          'deathMessage', 'pawnsPlural', 'jobString', 'quotation', 'beginLetterLabel', 'beginLetter', 'recoveryMessage',
          'inspectLine', 'graphLabelY', 'fixedName', 'letterLabel', 'letterText',
          'letterLabelEnemy', 'arrivalTextEnemy', 'letterLabelFriendly', 'arrivalTextFriendly', 'Description']
nestedstartlabels = ['injuryProps']
nestedlabels = ['destroyedLabel', 'destroyedOutLabel']
liststartlabels = ['helpTexts', 'comps', 'stages', 'degreeDatas', 'rulePack']
nestedliststartlabels = ['rulesStrings']
listlabels = ['label', 'description', 'labelTreatedWell', 'labelTreated', 'labelTreatedWellInner', 'labelTreatedInner',
              'labelSolidTreatedWell', 'labelSolidTreated', 'oldLabel']

# Check if the entered RimWorld installation folder was correct
if not os.path.exists(defsDirPath):
    print("Invalid RimWorld installation folder.")
    sys.exit(2)
else:
    print("Valid installation folder.")
    print("")

    # Create the translation folder
    if not os.path.exists(translationDirPath):
        os.makedirs(translationDirPath)

    # Count the number of files
    numfiles = 0
    for p, d, fs in os.walk(defsDirPath):
        for f in fs:
            if f.endswith('.xml'):
                numfiles += 1

    # Go through all the folders one by one
    # dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
    # and filenames is a list of files
    processedfiles = 0
    for dirpath, dirnames, filenames in os.walk(defsDirPath):

        # Save the name of the directory to create, but remove the s at the end
        # ThingDefs -> ThingDef
        defInjectDirectory = os.path.basename(dirpath)[:-1]

        # Go through all the files one by one
        for filename in [f for f in filenames if f.endswith('xml')]:

            # Parse the .xml file with ElementTree
            defFile = ETree.parse(os.path.join(dirpath, filename))
            defRoot = defFile.getroot()

            # Assume that the file doesn't have anything to translate
            haslabels = False
            # Go through the tags one by one and check if there is something to translate
            # If there is, change haslabels to True and stop searching
            for child in defRoot:
                defElement = child.find('defName')
                if defElement is None:
                    defElement = child.find('DefName')
                    if defElement is None:
                        continue

                for label in labels:
                    if child.find(label) is not None:
                        haslabels = True
                        break

                if haslabels:
                    break
                # If there were no tags found check for list thingies
                else:
                    for liststartlabel in liststartlabels:
                        if child.find(liststartlabel) is not None:
                            haslabels = True
                            break

            # If the file has something to translate
            if haslabels:
                # Create the directory in the translationDir if it doesn't exist
                if not os.path.exists(os.path.join(translationDirPath, defInjectDirectory)):
                    os.mkdir(os.path.join(translationDirPath, defInjectDirectory))

                # Assume that an already existing file is incorrect and remove it to start fresh
                if os.path.exists(os.path.join(translationDirPath, defInjectDirectory, filename)):
                    os.remove(os.path.join(translationDirPath, defInjectDirectory, filename))

                # Open the file for writing
                defInjectFile = open(os.path.join(translationDirPath, defInjectDirectory, filename), 'w+')

                # Write the header of the file
                writeheader(defInjectFile)

                defName = ""
                defNamePrev = ""
                labelDict = []
                # Go through the file tag by tag
                # child is ThingDef, TraitDef etc.
                for child in defRoot:
                    # Look for the defName of the Def
                    defElement = child.find('defName')
                    # Check if we found anything
                    if defElement is not None:
                        # Save the defname
                        defName = defElement.text
                    else:
                        # Check for alternate capitalization
                        defElement = child.find('DefName')
                        if defElement is not None:
                            defName = defElement.text
                        else:
                            continue

                    if defNamePrev == 'MossyTerrain' and defName == 'Ice':
                        stonelist = ['Sandstone', 'Granite', 'Limestone', 'Slate', 'Marble']
                        roughnesslist = [('Rough', 'rough'), ('RoughHewn', 'rough-hewn'), ('Smooth', 'smooth')]
                        for stone in stonelist:
                            for roughness in roughnesslist:
                                writedeflabel(defInjectFile, stone + '_' + roughness[0], 'label', roughness[1] + ' ' + stone.lower())

                            defInjectFile.write('    \n')

                    # Go through the labels one by one
                    for label in labels:
                        # Look for the label in tags
                        labelElement = child.find(label)
                        # Check if we found anything
                        if labelElement is not None:
                            # Add the label and its text to the list
                            labelDict.append((labelElement.tag, labelElement.text))
                    # Go through the list of collected labels
                    for label, text in labelDict:
                        # Write the lines to the file
                        writedeflabel(defInjectFile, defName, label, text)
                        # Clear the list of collected labels
                        labelDict = []
                    # Go through list thingies one by one
                    for liststartlabel in liststartlabels:
                        # Check if there are them
                        if child.find(liststartlabel) is not None:
                            liststart = child.find(liststartlabel)
                            # Store the elements of the list
                            listelements = liststart.findall('li')
                            if len(listelements) != 0:
                                for i, listelement in enumerate(listelements):
                                    if listelement.text is not None:
                                        # If the list element has no children, it has the text to translate in itself
                                        if len(list(listelement)) == 0:
                                            # Write the path replacement syntax to the file
                                            writepathreplace(defInjectFile, defName, liststartlabel + '.' + str(i), listelement.text)
                                        else:
                                            # Go through the in-list labels
                                            for listlabel in listlabels:
                                                # Look for them in the list
                                                if listelement.find(listlabel) is not None:
                                                    # Store the label tag
                                                    listsubelement = listelement.find(listlabel)
                                                    # Write the path replacement syntax to the file
                                                    writepathreplace(defInjectFile, defName, liststartlabel + '.' + str(i) + '.' + listsubelement.tag, listsubelement.text)
                            else:
                                for nestedliststartlabel in nestedliststartlabels:
                                    nestedliststart = liststart.find(nestedliststartlabel)
                                    nestedlistelements = nestedliststart.findall('li')
                                    if len(nestedlistelements) != 0:
                                        for i, nestedlistelement in enumerate(nestedlistelements):
                                            if nestedlistelement.text is not None:
                                                # If the list element has no children, it has the text to translate in itself
                                                if len(list(nestedlistelement)) == 0:
                                                    # Write the path replacement syntax to the file
                                                    writepathreplace(defInjectFile, defName, liststartlabel + '.' + nestedliststartlabel + '.' + str(i), nestedlistelement.text)

                    for nestedstartlabel in nestedstartlabels:
                        nestedstart = child.find(nestedstartlabel)
                        if nestedstart is not None:
                            for nestedlabel in nestedlabels:
                                nestedelement = nestedstart.find(nestedlabel)
                                if nestedelement is not None:
                                    writepathreplace(defInjectFile, defName, nestedstartlabel + '.' + nestedelement.tag, nestedelement.text)
                    if child.get('ParentName') in ['BasePawn', 'BaseAnimal', 'BaseMechanoid']:
                        labelElement = child.find('label')
                        if defName not in ['Chicken', 'Megascarab', 'Mechanoid_Centipede', 'Mechanoid_Scyther']:
                            writedeflabel(defInjectFile, defName + '_Leather', 'label', labelElement.text + ' leather')
                            writedeflabel(defInjectFile, defName + '_Leather', 'description', 'Leather made from the skin of a ' + labelElement.text + '.')
                        if defName not in ['Mechanoid_Centipede', 'Mechanoid_Scyther']:
                            writedeflabel(defInjectFile, defName + '_Meat', 'label', labelElement.text + ' meat')
                            writedeflabel(defInjectFile, defName + '_Meat', 'description', 'Raw flesh of a ' + labelElement.text + '.')
                        writedeflabel(defInjectFile, defName + '_Corpse', 'label', labelElement.text + ' corpse')
                        writedeflabel(defInjectFile, defName + '_Corpse', 'description', 'Dead body of a ' + labelElement.text + '.')
                    if child.get('ParentName') == 'StoneBlocksBase':
                        labelElement = child.find('label')
                        writedeflabel(defInjectFile, defName, 'stuffProps.stuffAdjective', labelElement.text[:-7])
                    if child.get('ParentName') == 'TileStoneBase':
                        writedeflabel(defInjectFile, defName, 'description', 'Solid stone tiles for a castle feeling. Pretty to look at, but they take a long time to lay.')
                    if child.get('ParentName') == 'TableBase':
                        writedeflabel(defInjectFile, defName, 'description', 'People eat off tables when chairs are placed facing them.')
                    if child.get('ParentName') == 'ResourceBase':
                        if child.find('stuffProps') is not None:
                            labelElement = child.find('label')
                            writedeflabel(defInjectFile, defName, 'stuffProps.stuffAdjective', labelElement.text)

                    # Move to the next line in the template
                    defInjectFile.write('    \n')
                    defNamePrev = defName

                # Clean up after parsing the file
                # Write the end of the xml file
                writefooter(defInjectFile)
                # Close the translatable file
                defInjectFile.close()

            processedfiles += 1

            print_progress(processedfiles, numfiles)

print("")
print("")

print("Successfully processed all files.")

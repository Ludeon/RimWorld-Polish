import os
import sys
import getopt
import re

__author__ = 'Sakuukuli'


def printhelp():
    """  Prints instructions in case of incorrect usage
    or when asked to.
    """
    print "RimWorld Translation Template Script"
    print "Copies all Def's from the RimWorld Core mod folder and creates DefInject templates for them."
    print "Usage: RimWorld_DefsToDefInject.py <RimWorld installation folder> <Folder for templates>"
    print ""
    print "Use -h to get this message."


def writeheader(filename):
    """ Writes the first lines of a DefInjected file.
    Arguments:
        filename: name of the file to write to
    """
    filename.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    filename.write('<LanguageData>\n')
    filename.write('    \n')


def writedeflabel(filename, labelType, defname, deflabel):
    """ Writes the translation data of a DefInjected file in the correct syntax:
    <Ocean.label>ocean</Ocean.label>
    <Ocean.description>Open ocean. Great for fish - not so great for you.</Ocean.description>

    Arguments:
        filename: Name of the file to write to
        labelType: A designation string for the label, for example 'description'
        defname: The name of the def the label belongs to
        deflabel: The untranslated text in the label
    """
    filename.write('    <' + defname + '.' + labelType + '>' + deflabel + '</' + defname + '.' + labelType + '>\n')


def writefooter(filename):
    """ Writes the last lines of a DefInjected file.
    Arguments:
        filename: Name of the file to write to
    """
    filename.write('</LanguageData>\n')


# Save the arguments
arguments = sys.argv[1:]
# Parse the arguments and look for the -h option
try:
    opts, args = getopt.getopt(arguments, "h")
# Print help in case of an error
except getopt.GetoptError:
    printhelp()
    sys.exit(2)

# If -h option was passed print the help
for opt in opts:
    if opt == '-h':
        printhelp()
        sys.exit()

# Save the directories in variables
if len(arguments) == 2:
    defsDir = arguments[0]
    translationDir = arguments[1]
# If no directories entered then print help
else:
    printhelp()
    sys.exit(2)

# Print information about the script
print "--------------------------------------------------------------------"
print "RimWorld Translation Template Script"
print ""
print "RimWorld installation folder is \"" + defsDir + "\""
print "Templates will be created in folder \"" + translationDir + "\""
print "--------------------------------------------------------------------"

# Move to the directories where the files are
defsDir += '\\Mods\\Core\\Defs\\'
translationDir += '\\DefInjected\\'

# Check if the entered RimWorld installation folder was correct
if os.path.exists(defsDir):

    # Create the translation folder
    if not os.path.exists(translationDir):
        os.makedirs(translationDir)

    # Start going through all the folders
    # directory is the name of the current def directory
    for directory in [d for d in os.listdir(defsDir) if os.path.isdir(os.path.join(defsDir, d))]:
        fullpath = os.path.join(defsDir, directory)
        for filename in [f for f in os.listdir(fullpath) if os.path.isfile(os.path.join(fullpath, f))]:
            if filename.endswith(".xml"):
                #                filelist.append(os.path.join(root, filename))
                data = open(os.path.join(fullpath, filename), 'r')
                lines = data.readlines()

                # Assume that the file doesn't have anything to translate
                haslabels = False
                # Go through the lines one by one and check if there is something to translate
                # If there is, change haslabels to True and stop searching
                # There are some thigs to translate which are either uppercase or lowercase
                for line in lines:
                    if '<label>' in line or '<Label>' in line:
                        haslabels = True
                        break
                    elif '<description>' in line or '<Description>' in line:
                        haslabels = True
                        break
                    elif '<pawnLabel>' in line or '<PawnLabel>' in line:
                        haslabels = True
                        break
                    elif '<gerundLabel>' in line or '<GerundLabel>' in line:
                        haslabels = True
                        break
                    elif '<skillLabel>' in line or '<SkillLabel>' in line:
                        haslabels = True
                        break
                    elif '<reportString>' in line or '<ReportString>' in line:
                        haslabels = True
                        break
                    elif '<verb>' in line or '<verb>' in line:
                        haslabels = True
                        break
                    elif '<gerund>' in line or '<gerund>' in line:
                        haslabels = True
                        break

                # If the file has something to traslate
                if haslabels:

                    # Save the name of the directory to create, but remove the s at the end
                    defInjectDirectory = directory[:-1] + '\\'

                    # Create the directory in the translationDir if it doesn't exist
                    if not os.path.exists(translationDir + defInjectDirectory + '\\'):
                        os.mkdir(translationDir + defInjectDirectory + '\\')

                    # Assume that an already existing file is incorrect
                    # and remove it to start fresh
                    if os.path.exists(translationDir + defInjectDirectory + '\\' + filename):
                        os.remove(translationDir + defInjectDirectory + '\\' + filename)

                    # Open the file for writing
                    defInjectFile = open(translationDir + defInjectDirectory + '\\' + filename, 'w+')
                    # Write the header of the file
                    writeheader(defInjectFile)

                    # Store whether we are in a comment or not
                    ignoring = False
                    # Start going through the file line by line
                    for i, line in enumerate(lines):
                        # If there is a def on the line, look in the next lines for something to translate
                        # if we are not inside a comment
                        if ('<defName>' in line or '<DefName>' in line) and not ignoring:
                            # Store the name of the def
                            defName = re.findall('<defName>(.*?)</defName>', line, re.IGNORECASE)[0]
                            # Look in the next lines for something to traslate
                            for j, line in enumerate(lines[i + 1:]):
                                # If there is something else defined, we know that there is nothing left to translate
                                # so stop looking
                                if '<defName>' in line or '<DefName>' in line:
                                    break
                                # If there is a list of things which are defined, ignore it completely
                                # I don't know how to parse them yet
                                elif '<li>' in line:
                                    break
                                # If there is something to translate, write it to the DefInjected file
                                # If it is a label
                                elif '<label>' in line or '<Label>' in line:
                                    # Store the name of the thing to translate
                                    labelType = 'label'
                                    # Store the untranslated string from between the tags
                                    template = re.findall('<label>(.*?)</label>', line, re.IGNORECASE)[0]
                                    # Write the line
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<description>' in line or '<Description>' in line:
                                    labelType = 'description'
                                    template = re.findall('<description>(.*?)</description>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<pawnLabel>' in line or '<PawnLabel>' in line:
                                    labelType = 'pawnLabel'
                                    template = re.findall('<pawnLabel>(.*?)</pawnLabel>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<gerundLabel>' in line or '<GerundLabel>' in line:
                                    labelType = 'gerundLabel'
                                    template = re.findall('<gerundLabel>(.*?)</gerundLabel>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<skillLabel>' in line or '<SkillLabel>' in line:
                                    labelType = 'skillLabel'
                                    template = re.findall('<skillLabel>(.*?)</skillLabel>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<reportString>' in line or '<ReportString>' in line:
                                    labelType = 'reportString'
                                    template = re.findall('<reportString>(.*?)</reportString>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<verb>' in line or '<Verb>' in line:
                                    labelType = 'verb'
                                    template = re.findall('<verb>(.*?)</verb>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)
                                elif '<gerund>' in line or '<Gerund>' in line:
                                    labelType = 'gerund'
                                    template = re.findall('<gerund>(.*?)</gerund>', line, re.IGNORECASE)[0]
                                    writedeflabel(defInjectFile, labelType, defName, template)

                            # Move to the next line
                            defInjectFile.write('    \n')
                        # If a comment starts on this line
                        elif not ignoring and '<!--' in line:
                            # and it doesn't end on the same line
                            if not '-->' in line:
                                # then don't parse the comment
                                ignoring = True
                            else:
                                # Else if a comment starts and ends on the same lane
                                # it is something useful so write it in the file too
                                defInjectFile.write('  ' + line)
                                defInjectFile.write('    \n')
                        # else if a comment ends on this line
                        elif ignoring and '-->' in line:
                            # Start parsing again
                            ignoring = False

                    # Clean up after parsing the file
                    # Write the end of the xml file
                    writefooter(defInjectFile)
                    # Close the translateable file
                    defInjectFile.close()
                    # Close the original Def file
                    data.close()

# If the specified directory doesn't exist,
# print an error
else:
    print "Invalid RimWorld installation folder"
    sys.exit(2)

import os
import sys
import getopt
import re

__author__ = 'Sakuukuli'


def printhelp():
    print "RimWorld Translation Template Script"
    print "Copies all Def's from the RimWorld Core mod folder and creates DefInject templates for them."
    print "Usage: RW_DefsToDefInject.py <RimWorld installation folder> <Folder for templates>"
    print ""
    print "Use -h to get this message."


def writeheader(filename):
    filename.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    filename.write('<LanguageData>\n')
    filename.write('    \n')


def writedeflabel(filename, labelType, defname, deflabel):
    filename.write('    <' + defname + '.' + labelType + '>' + deflabel + '</' + defname + '.' + labelType + '>\n')


def writefooter(filename):
    filename.write('</LanguageData>\n')


arguments = sys.argv[1:]
try:
    opts, args = getopt.getopt(arguments, "h")
except getopt.GetoptError:
    printhelp()
    sys.exit(2)

for opt in opts:
    if opt == '-h':
        printhelp()
        sys.exit()

if len(arguments) != 0:
    defsDir = arguments[0]
    translationDir = arguments[1]
else:
    printhelp()
    sys.exit(2)

print "--------------------------------------------------------------------"
print "RimWorld Translation Template Script"
print "RimWorld installation folder is \"" + defsDir + "\""
print "Templates will be created in folder \"" + translationDir + "\""
print "--------------------------------------------------------------------"

defsDir += '\\Mods\\Core\\Defs\\'
translationDir += '\\DefInjected\\'

if os.path.exists(defsDir):

    if not os.path.exists(translationDir):
        os.makedirs(translationDir)

    for directory in [d for d in os.listdir(defsDir) if os.path.isdir(os.path.join(defsDir, d))]:
        fullpath = os.path.join(defsDir, directory)
        for filename in [f for f in os.listdir(fullpath) if os.path.isfile(os.path.join(fullpath, f))]:
            if filename.endswith(".xml"):
                #                filelist.append(os.path.join(root, filename))
                data = open(os.path.join(fullpath, filename), 'r')
                lines = data.readlines()

                haslabels = False
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

                if haslabels:

                    defInjectDirectory = directory[:-1] + '\\'

                    if not os.path.exists(translationDir + defInjectDirectory + '\\'):
                        os.mkdir(translationDir + defInjectDirectory + '\\')

                    if os.path.exists(translationDir + defInjectDirectory + '\\' + filename):
                        os.remove(translationDir + defInjectDirectory + '\\' + filename)

                    defInjectFile = open(translationDir + defInjectDirectory + '\\' + filename, 'w+')
                    writeheader(defInjectFile)

                    ignoring = False
                    for i, line in enumerate(lines):
                        if ('<defName>' in line or '<DefName>' in line) and not ignoring:
                            defName = re.findall('<defName>(.*?)</defName>', line, re.IGNORECASE)[0]
                            for j, line in enumerate(lines[i + 1:]):
                                if '<defName>' in line or '<DefName>' in line:
                                    break
                                elif '<li>' in line:
                                    break
                                elif '<label>' in line or '<Label>' in line:
                                    labelType = 'label'
                                    template = re.findall('<label>(.*?)</label>', line, re.IGNORECASE)[0]
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

                            defInjectFile.write('    \n')
                        elif not ignoring and '<!--' in line:
                            if not '-->' in line:
                                ignoring = True
                            else:
                                defInjectFile.write('  ' + line)
                                defInjectFile.write('    \n')
                        elif ignoring and '-->' in line:
                            ignoring = False

                    writefooter(defInjectFile)
                    defInjectFile.close()
                    data.close()

else:
    print "Invalid RimWorld installation folder"
    sys.exit(2)

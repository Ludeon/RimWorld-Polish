import os
import sys
import xml.etree.ElementTree as ET

import rwtutil

__author__ = 'Sakuukuli'


def printhelp():
    """ Print information about the script.
    """
    print("RimWorld Path Translation Simplification Script")
    print("Simplifies multi-line path translations to the new simpler syntax.")
    print("Usage: RimWorld_SimplifyPathTranslations.py <Directory>")


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
    rwtutil.print_help_error()
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

print("Simplifying...", end=' ')
rwtutil.simplify_path_translations(translationDirPath)
print("OK")

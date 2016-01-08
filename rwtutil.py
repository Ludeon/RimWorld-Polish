import os,sys
import xml.etree.ElementTree as ET

__author__ = 'Sakuukuli'


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

    :param message: Progress label
    :param progress: Number of files processed
    :param total: Total number of files
    """
    # Calculate the percent, multiply with 1.0 to force floating point math
    percent = 1.0 * progress / total
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}: {}/{} {}%'.format(message, progress, total, round(percent * 100)))
    sys.stdout.flush()


def print_counter(message, progress):
    """Prints the number of files processed, total number of files and a percentage.

    Replaces itself automatically and animates.
    The format is progress/total percent%

    :param message: Progress label
    :param progress: Number of files processed
    """
    # Write the line, '\r' moves the write head back to the start for overwriting.
    sys.stdout.write('\r{}: {}'.format(message, progress))
    sys.stdout.flush()


def collect_tags_and_text_to_dict(translationdir):
    """Collect tags in a translation folder into a dict

    Dict has tags as keys and each tag has a list of tuples (text, file) as occurences

    :param translationdir:
    :return:
    """
    tempdict = {}
    temppath = ""
    for dirpath, dirnames, filenames in os.walk(translationdir):

        if not (os.path.basename(os.path.split(dirpath)[0]) == 'DefInjected' or os.path.basename(dirpath) == 'Keyed'):
            continue

        # Go through all the files one by one
        for filename in [f for f in filenames if f.endswith('.xml')]:
            if os.path.basename(dirpath) == "Keyed":
                temppath = "Keyed"
            elif os.path.basename(os.path.split(dirpath)[0]) == "DefInjected":
                temppath = os.path.join("DefInjected", os.path.basename(dirpath))

            # Parse the .xml file with ElementTree
            deffile = ET.parse(os.path.join(dirpath, filename))
            defroot = deffile.getroot()

            for child in defroot:
                if child.tag not in tempdict.keys():
                    tempdict[child.tag] = [(child.text, os.path.join(temppath, filename))]
                else:
                    tempdict[child.tag].append((child.text, os.path.join(temppath, filename)))
        if translationdir == ".":
            print_counter("Collecting tags from templates", len(tempdict))
        else:
            print_counter("Collecting tags from " + translationdir, len(tempdict))

    print("")
    return tempdict


def sort_list_of_tags_by_file(tag_list):
    filelist = []
    filetaglist = []
    newlist = []

    for file, tag, text in tag_list:
        if file not in filelist:
            filelist.append(file)

    for file in filelist:
        for f, tag, text in tag_list:
            if f == file:
                filetaglist.append((tag, text))

        newlist.append((file, filetaglist))
        filetaglist = []

    return sorted(newlist)


def simplify_path_translations(translationdirpath):
    """ Change the multiline path translations to the new simpler format

    :param translationdirpath: Path to the translation to change
    :return:
    """
    # Go through all the folders one by one
    # dirpath is the full path to the current def directory, dirnames is a list of directories in the current directory
    # and filenames is a list of files
    for dirpath, dirnames, filenames in os.walk(translationdirpath):

        # Only parse .xml files
        for filename in [f for f in filenames if f.endswith('.xml')]:

            # Parse the .xml file with ElementTree
            deftree = ET.parse(os.path.join(dirpath, filename))
            defroot = deftree.getroot()

            # Check if the file has path translations
            if defroot.find('rep'):
                # Go through all the elements in the xml file
                for index, repElement in enumerate(defroot):
                    # Check if this element is a path translation
                    if repElement.tag == 'rep':
                        # Store the information in the element
                        path = repElement.find('path').text
                        trans = repElement.find('trans').text
                        whitespace = repElement.tail

                        # Change the path to the new format
                        path = format_path(path)

                        # Remove the element in the old format
                        defroot.remove(repElement)

                        # Insert an element in the new format in its place
                        defroot.insert(index, ET.Element(path))
                        defroot[index].text = trans
                        defroot[index].tail = whitespace

                write_tree_to_file(deftree, filename, dirpath)


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


def write_tree_to_file(tree, filename, dirpath):
    # Write the tree into a temporary file
    tempfilename = filename + '.temp'
    # Do not add a header, because it will be different from the RimWorld conventions
    tree.write(os.path.join(dirpath, tempfilename), encoding="utf-8", xml_declaration=False)

    # Open the file for writing
    deffile = open(os.path.join(dirpath, filename), 'w+')
    tempfile = open(os.path.join(dirpath, tempfilename), 'r')
    # Add header in the RimWorld way
    deffile.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    deffile.write(replace_escapechars(tempfile.read()))
    deffile.write('\n')

    # Clean up
    deffile.close()
    tempfile.close()
    os.remove(os.path.join(dirpath, tempfilename))
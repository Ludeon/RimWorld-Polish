import os
import xml.etree.ElementTree as ET


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

                # Write the tree into a temporary file
                tempfilename = filename + '.temp'
                # Do not add a header, because it will be '<?xml version='1.0' encoding='utf-8'?>\n'
                deftree.write(os.path.join(dirpath, tempfilename), encoding="utf-8", xml_declaration=False)

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


def format_path(path):
    path = path.replace('[', '.')
    path = path.replace(']', '')
    return path


def replace_escapechars(text):
    escapechars = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>'}
    for i, j in escapechars.items():
        text = text.replace(i, j)
    return text

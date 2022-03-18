import xml.etree.ElementTree as ET
import sys
from colored import fg, attr

def show_arg_error():
    print(fg('red') + '[!] ERROR: ' + 'Invalid Format\nShould be of the format `python permissions.py FOLDER_NAME`'+ attr('reset'))

def main():
    #Get the argument from the command line
    if len(sys.argv) != 2:
        show_arg_error()
        exit()

    folder_name = sys.argv[1]

    root = ET.parse("output\\"+folder_name+"\\AndroidManifest.xml").getroot()
    permissions = root.findall("uses-permission")

    for perm in permissions:
        for att in perm.attrib:
            print(perm.attrib[att])

main()
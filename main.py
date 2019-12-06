import sys
import math
import json
import xml.etree.ElementTree as eTree

MAX_FC_STATICS = 226


def print_help():
    print("Program arguments include 1) the input file name, 2) the output " +
          "file name, and optionally 3) the desired static rectangle width. " +
          "Examples:\n" +
          "main.py my_input.json my_output.xml 10\n" +
          "main.py my_input.json my_output.xml")


def main():
    if len(sys.argv) < 3:
        print_help()
        return

    try:
        with open(sys.argv[1], "r") as fin:
            content = fin.read()
    except IOError as e:
        print(str(e))
        return

    try:
        j = json.loads(content)
    except TypeError as e:
        print(str(e))
        return

    level_name = j["label"]
    lines = j["linesArray"]

    if len(lines) > MAX_FC_STATICS:
        print("WARNING: FC levels can only contain a maximum of " +
              str(MAX_FC_STATICS) + " static objects. " + "Your track has " +
              str(len(lines)) + " lines.")

    root = eTree.Element("root")
    eTree.SubElement(root, "name").text = level_name
    level = eTree.SubElement(root, "level")
    level_blocks = eTree.SubElement(level, "levelBlocks")

    for line in lines:
        x1 = line[2]
        y1 = line[3]
        x2 = line[4]
        y2 = line[5]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        rotation = math.atan2(y2 - y1, x2 - x1)
        width = math.hypot(x2 - x1, y2 - y1)
        height = 10 if not len(sys.argv) > 3 else int(sys.argv[3])

        rect = eTree.SubElement(level_blocks, "StaticRectangle")
        eTree.SubElement(rect, "rotation").text = str(rotation)
        position = eTree.SubElement(rect, "position")
        eTree.SubElement(position, "x").text = str(cx)
        eTree.SubElement(position, "y").text = str(cy)
        eTree.SubElement(rect, "width").text = str(width)
        eTree.SubElement(rect, "height").text = str(height)
        eTree.SubElement(rect, "goalBlock").text = "false"
        eTree.SubElement(rect, "joints")

    # Add an element for goal pieces
    eTree.SubElement(level, "PlayerBlocks")

    # Add a build and goal area
    areas = ["start", "end"]
    for area in areas:
        area_elem = eTree.SubElement(level, area)
        position = eTree.SubElement(area_elem, "position")
        eTree.SubElement(position, "x").text = "0"
        eTree.SubElement(position, "y").text = "0"
        eTree.SubElement(area_elem, "width").text = "100"
        eTree.SubElement(area_elem, "height").text = "100"

    xml_string = eTree.tostring(root, short_empty_elements=True)
    file_write_name = sys.argv[2]
    try:
        with open(file_write_name, "wb") as fout:
            fout.write(xml_string)
    except IOError as e:
        print(str(e))
        return

    print("Your FC level has been created successfully in " + file_write_name +
          ".")


if __name__ == "__main__":
    main()

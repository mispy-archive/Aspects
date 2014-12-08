#!/usr/bin/env python

MAX_PROVINCES = 10000

from PIL import Image

def province_color(line):
    """Gets the RGB tuple from a definition.csv line"""
    spl = line.strip('#').split(';')
    return (int(spl[1]), int(spl[2]), int(spl[3]))

def province_num(line):
    """Gets the province number from a definition.csv line"""
    spl = line.strip('#').split(';');
    if not spl[0]:
        return 0
    else:
        return int(spl[0])

# Track all colors present in provinces.bmp
# (int, int, int) => True
bmp_colors = {}

image = Image.open("provinces.bmp")
for tpl in image.getcolors(MAX_PROVINCES):
    bmp_colors[tpl[1]] = True

province_defs = file("definition.csv").read().splitlines()[1:-1]

# Track all colors in definition.csv
# (int, int, int) => True
def_colors = {
    # Black and white are special and don't need definitions
    (0, 0, 0): True,
    (255, 255, 255): True
}

# Accumulate definition lines to override the originals
output_defs = []

# Toggle existing province defs that have been removed/readded
for line in province_defs:
    if not line:
        continue
    color = province_color(line)
    def_colors[color] = True

    if color in bmp_colors and line.startswith("#"):
        # Inactive but shouldn't be
        print "Activating {}".format(line)
        output_defs.append(line[1:-1])
    elif color not in bmp_colors and not line.startswith("#"):
        # Active but needs to be removed
        print "Commenting out {}".format(line)
        output_defs.append("#"+line)
    else:
        # No change needed
        output_defs.append(line)

# Now add any new colors that aren't in definition.csv at all
max_num = max([province_num(line) for line in output_defs])
for color in bmp_colors.keys():
    if color not in def_colors:
        max_num += 1
        line = "{};{};{};{};;x".format(
            max_num, color[0], color[1], color[2])
        print "Adding new province {}".format(line)
        output_defs.append(line)

with open("definition.csv", 'w') as f:
    f.write("province;red;green;blue;x;x\n" + "\n".join(output_defs))

#!/usr/bin/env python

MAX_PROVINCES = 10000

from PIL import Image

def province_color(line):
    spl = line.strip('#').split(';')
    return (spl[1], spl[2], spl[3])

def province_num(line):
    spl = line.strip('#').split(';');
    if not spl[0]:
        return 0
    else:
        return int(spl[0])

# (int, int, int) => true
bmp_colors = {}

# Find all colors in provinces.bmp
image = Image.open("provinces.bmp")
for tpl in image.getcolors(MAX_PROVINCES):
    bmp_colors[tpl[1]] = True

province_defs = file("definition.csv").read().splitlines()[1:-1]
def_colors = {}
new_defs = []

# Toggle existing province defs that have been removed/readded
for line in province_defs:
    if not line:
        continue
    color = province_color(line)
    def_colors[color] = True

    if color in bmp_colors and line.startswith("#"):
        # Commented out but shouldn't be
        print "Activating {}".format(line)
        new_defs.append(line[1:-1])
    elif color not in bmp_colors and not line.startswith("#"):
        # Needs to be commented out
        print "Commenting out {}".format(line)
        new_defs.append("#"+line)
    else:
        # No change needed
        new_defs.append(line)

# Now add any new colors that aren't in definition.csv at all
max_num = max([province_num(line) for line in new_defs])
for color in bmp_colors.keys():
    if color not in def_colors:
        max_num += 1
        line = "{};{};{};{};;x".format(
            max_num, color[0], color[1], color[2])
        print "Adding new province {}".format(line)
        new_defs.append(line)

with open("definition.csv", 'w') as f:
    f.write("\n".join(new_defs))

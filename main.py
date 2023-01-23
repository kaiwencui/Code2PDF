#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import time
import os
import markdown

from fpdf import FPDF, HTMLMixin
from fpdf.enums import XPos, YPos
from pathlib import Path

# prefix components:
space = '    '
branch = '│   '
tee = '├── '
last = '└── '


def tree(dir_path: Path, prefix: str = ''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


def convertMDtoHTML(line) -> str:
    """
    Convert markdown to HTML
    """
    html = markdown.markdown(line)
    return html



class PDF(FPDF, HTMLMixin):
    pass


pdf = PDF(orientation='P',
          unit='mm',
          format='A4')
pdf.add_page()
pdf.add_font("AdobeGaramondProBold", style="", fname="fonts/Adobe Garamond Pro.ttf")
pdf.set_font('AdobeGaramondProBold', size=12)
pdf.add_font("OCRAEXT", style="", fname="fonts/OCRAEXT.ttf")
# pdf.image("assets/header.png", w=207, x=1.5, y=2)

# small header
pdf.ln(-5)
pdf.cell(-5)
pdf.set_font('OCRAEXT', size=10)
pdf.set_text_color(122, 119, 121)
pdf.cell(new_x=XPos.LMARGIN, new_y=YPos.NEXT, txt="source code")
pdf.set_text_color(0, 0, 0)

# title
project_name = input("Enter project name: ")
pdf.ln(50)
pdf.cell(30)
pdf.set_font('OCRAEXT', size=21)
pdf.cell(txt=project_name)

# author
author = input("Enter author: ")
pdf.ln(20)
pdf.cell(30)
pdf.set_font('OCRAEXT', size=10)
pdf.cell(txt="Author: " + author)

# version
author = input("Enter version: ")
pdf.ln(6)
pdf.cell(30)
pdf.set_font('OCRAEXT', size=10)
pdf.cell(txt="Version: " + author)

# source
# source = "github.com"
source = input("Enter source url: ")
pdf.ln(6)
pdf.cell(30)
pdf.multi_cell(w=130, txt="Source: " + source)

# date
pdf.ln(6)
pdf.cell(30)
pdf.cell(txt="Compiled on: " + time.strftime("%Y-%m-%d %H:%M"))
pdf.ln(30)
pdf.cell(30)

# directory tree
# directory = "/Users/kaiwencui/PycharmProjects/pythonProject1/source_code"
directory = input("Enter directory: ")

line = "." + '\n'
for file in tree(Path(directory)):
    line = line + file + '\n'

pdf.set_font('OCRAEXT', size=12)
pdf.cell(txt="Directory:")
pdf.ln(10)
pdf.cell(30)
pdf.add_font("DejaVuSansMono", style="", fname="fonts/DejaVuSansMono.ttf")
pdf.set_font('DejaVuSansMono', size=12)
pdf.multi_cell(600, txt=line)

# Iterate over each file in the directory
# directory = input("Enter project directory: ")
pdf.add_font("SourceCodePro-Regular", style="", fname="fonts/SourceCodePro-Regular.ttf")

extensions = [".js", ".py", ".txt", ".env"]

for path, subdirs, files in os.walk(directory):
    for name in files:
        absolute_path = os.path.join(path, name)
        filename = os.path.basename(absolute_path)

        if filename.endswith(".md"):
            pdf.add_page()
            pdf.set_draw_color(112, 119, 121)
            pdf.rect(5, 5, 200, 8, round_corners=False, style="D")
            pdf.set_font('OCRAEXT', size=10)
            pdf.ln(-2)
            pdf.set_text_color(0, 0, 0)
            filename = "".join(absolute_path.rsplit(directory))
            pdf.cell(w=120, txt="file name: " + filename[1:], new_x=XPos.LEFT)
            # pdf.cell(90)
            stat_result = Path(absolute_path).stat().st_mtime
            modified = datetime.datetime.fromtimestamp(stat_result).strftime('%Y-%m-%d %H:%M')
            pdf.set_x(130)
            pdf.cell(txt="last modified: " + str(modified), new_x=XPos.RIGHT)
            pdf.set_text_color(0, 0, 0)

            # open file and read it line by line
            with open(absolute_path) as file_in:
                lines = []
                for line in file_in:
                    # line = line.replace("\n", "")
                    if '![' in line:
                        line = line.replace(line, '')
                    print(line)
                    lines.append(line)

            pdf.set_x(0)
            pdf.set_y(20)
            pdf.set_font('SourceCodePro-Regular', size=9)

            s = ''.join(lines)

            # print(s)

            line = convertMDtoHTML(s)
            pdf.write_html(line)

            # for line in lines:
            #     pdf.set_text_color(0, 0, 0)
            #     line = convertMDtoHTML(line)
            #     try:
            #         pdf.write_html(line)
            #     except:
            #         continue
            #     pdf.ln(3)

        if filename.endswith(tuple(extensions)):
            pdf.add_page()
            pdf.set_draw_color(112, 119, 121)
            pdf.rect(5, 5, 200, 8, round_corners=False, style="D")
            pdf.set_font('OCRAEXT', size=10)
            pdf.ln(-2)
            pdf.set_text_color(0, 0, 0)
            filename = "".join(absolute_path.rsplit(directory))
            pdf.cell(w=120, txt="file name: " + filename[1:], new_x=XPos.LEFT)
            # pdf.cell(90)
            stat_result = Path(absolute_path).stat().st_mtime
            modified = datetime.datetime.fromtimestamp(stat_result).strftime('%Y-%m-%d %H:%M')
            pdf.set_x(130)
            pdf.cell(txt="last modified: " + str(modified), new_x=XPos.RIGHT)
            pdf.set_text_color(0, 0, 0)

            with open(absolute_path) as file_in:
                lines = []
                for line in file_in:
                    line = line.replace("\n", "")
                    lines.append(line)

            code_lines = "1"
            count = 0
            pdf.set_x(0)
            pdf.set_y(20)
            pdf.set_font('SourceCodePro-Regular', size=9)

            for line in lines:
                count = count + 1
                pdf.set_text_color(172, 173, 172)
                pdf.cell(w=7, txt=str(count))
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(w=180, txt=line, new_x=XPos.LEFT, align="L")
                pdf.ln(1)

            continue
        else:
            continue

pdf.output('test.pdf', 'F')

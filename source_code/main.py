#!/usr/bin/env python
# -*- coding: utf8 -*-

from fpdf import FPDF, HTMLMixin
from fpdf.enums import XPos, YPos

import time
import os
from pathlib import Path


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
project_name = "Source code"
# project_name = input("Enter project name: ")
pdf.ln(60)
pdf.cell(30)
pdf.set_font('OCRAEXT', size=21)
pdf.cell(txt=project_name)

# author
author = "Kai Wen Cui"
# author = input("Enter author: ")
pdf.ln(20)
pdf.cell(30)
pdf.set_font('OCRAEXT', size=12)
pdf.cell(txt="Author: " + author)

# source
source = "github.com"
# source = input("Enter source url: ")
pdf.ln(6)
pdf.cell(30)
pdf.cell(txt="Source: " + source)

# date
pdf.ln(13)
pdf.cell(30)
pdf.cell(txt="Compiled on: " + time.strftime("%Y-%m-%d %H:%M"))
pdf.ln(30)
pdf.cell(30)

# directory tree
directory = "/Users/kaiwencui/PycharmProjects/pythonProject1/source_code"
line = "root"
for line in tree(Path(directory)):
    line = line + line
print("line: " + line)

pdf.cell(txt="Directory:")
pdf.ln(10)
pdf.cell(30)
pdf.add_font("DejaVuSansMono", style="", fname="fonts/DejaVuSansMono.ttf")
pdf.set_font('DejaVuSansMono', size=12)
pdf.cell(txt=line)

# Iterate over each file in the directory
# directory = input("Enter project directory: ")
pdf.add_font("SourceCodePro-Regular", style="", fname="fonts/SourceCodePro-Regular.ttf")
pdf.set_font('SourceCodePro-Regular', size=10)
for file in os.listdir(directory):
    pdf.add_page()
    filename = os.fsdecode(file)
    if filename.endswith(".js") or filename.endswith(".py"):
        path = os.path.join(directory, filename)
        f = open(path, "r").read()

        pdf.multi_cell(600, txt=f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        continue
    else:
        continue

pdf.output('test.pdf', 'F')
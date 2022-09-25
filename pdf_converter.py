#!/usr/bin/env python
# coding: utf-8

# import libraries
from docx2pdf import convert
from pdf2docx import Converter
import pathlib

# Convert pdf to docx
def convert_docx(pdf_file, dest):
    output_file = pathlib.Path(pdf_file).stem
    docx_file = pathlib.Path(dest, output_file + '.docx')
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()
    return output_file + '.docx'


# Convert docx to pdf
def convert_pdf(docx_file, dest):
    output_file = pathlib.Path(docx_file).stem
    pdf_file = pathlib.Path(dest, output_file + '.pdf')
    convert(docx_file)
    return output_file + '.pdf'






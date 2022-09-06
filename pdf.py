from email.mime import image
from fpdf import FPDF
import plotly.express as px
import plotly
import os
import app


class PDF(FPDF):
     pass # nothing happens when it is executed.

pdf = PDF()#pdf object
pdf=PDF(orientation='P') # landscape
pdf=PDF(unit='mm') #unit of measurement

pdf=PDF(format='A4') #page format. A4 is the default value of the format, you don't have to specify it.
# full syntax

pdf = PDF(orientation='P', unit='mm', format='A4')

pdf_w=210
pdf_h=297



class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(0,pdf_h/2,210,pdf_h/2)

def imagex(self):
        self.set_xy(6.0,6.0)
        self.image(app.img,  link='', type='', w=1586/80, h=1920/80)
        self.set_xy(183.0,6.0)
        self.image(app.img,  link='', type='', w=1586/80, h=1920/80)

class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0) # top one
        self.line(5.0,292.0,205.0,292.0) # bottom one
        self.line(5.0,5.0,5.0,292.0) # left one
        self.line(205.0,5.0,205.0,292.0) # right one


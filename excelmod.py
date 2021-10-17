from settings import Config
from pathlib import path
from s2c_class import driver, Speech2Command
import openpyxl
import json

class ModExcel:
    def __init__(self, path="sample.xlsx", config={}):
        self.loc = loc
        self.workbook = openpyxl.load_workbook(path)
        self.row = 0
        self.col = 0
        self.config = config
        self.sheet = self.workbook.active

    def getSheet(self):
        return self.sheet

    def navigate(self, *args):
        try:
            for i in args:
                if i.lower() == "right":
                    self.col += 1
                if i.lower() == "left":
                    self.col -= 1
                if i.lower() == "up":
                    self.row -= 1
                if i.lower() == "down":
                    self.row += 1

            return self.sheet.cell(row=self.row, column=self.col)
        except:
            return None

    def getCell(self):
        try:
            return self.sheet.cell(row=self.row, column=self.col)
        except:
            return None

    def setValue(self, cell, val):
        try:
            cell.value = val
            return True
        except:
            return False
    


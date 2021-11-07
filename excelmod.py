from settings import Config
# from pathlib import path
from s2t_class import Speech2Text
import openpyxl
import json
import os

class ModExcel:
    def __init__(self, path="samples/samples.xlsx", config=Config().get_config()):
        # self.loc = loc
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

    def setValue(self, cmd):
        val = cmd
        cell = self.getCell()
        try:
            cell.value = val
            return True
        except:
            return False

def parsecmd(cmd):
    a = cmd.split(" ")
    return {a[0]: cmd[cmd.index(a[1])-1:].strip()}

def driver_excelmod():
    # print(driver.__code__())
    # print(str(os.path))

    s2t = Speech2Text(mode="mic", src="vosk", output="a.txt")
    cfg = Config().get_config()
    xl = ModExcel(config=cfg)
    cmd = None

    while True:
        try:
            if s2t.src == "vosk":
                text = json.loads(s2t.listen())["text"]
            elif s2t.src == "google":
                text = s2t.listen()
            print(f"\n\n{text}\n\n")
        
            parsed_tree = parsecmd(text)
            commands = list(parsed_tree.keys())


            # Execution block
            if commands[0] in cfg.keys():
                if commands[0] not in ["get"]:
                    cmd = f"xl.{cfg[commands[0]]}({[parsed_tree[commands[0]]]})"
                else:
                    cmd = f"xl.{cfg[commands[0]]}()"
                exec(cmd)
            else:
                print("\n\nSorry, but your command doesn't match the known ones... \n\n")
        except Exception as e:
            print("\n\nAn error occured. Error details: \t", e)

if __name__ == '__main__':
    driver_excelmod()


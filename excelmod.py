from settings import Config
from s2t_class import Speech2Text
import openpyxl
import json
import os

class ModExcel:
    def __init__(self, path="samples/samples.xlsx", config=Config().get_config()):
        self.path = path
        self.workbook = openpyxl.load_workbook(path)
        self.row = 1
        self.col = 1
        self.config = config
        self.sheet = self.workbook.active

    def getSheet(self):
        return self.sheet
    
    def getCell(self):
        try:
            return self.sheet.cell(row=self.row, column=self.col)
        except:
            return None

    def navigate(self, args):
        # try:
        for i in args:
            if i.lower() == "right":
                print("\n\nMoving one column right\n\n")
                self.col += 1
            if i.lower() == "left":
                print("\n\nMoving one column left\n\n")
                self.col -= 1
            if i.lower() == "up":
                print("\n\nMoving one row up\n\n")
                self.row -= 1
            if i.lower() == "down":
                print("\n\nMoving one row down\n\n")
                self.row += 1

        self.getCell()
        # except:
        #     return None

    def setValue(self, cmd):
        val = cmd[0]
        cell = self.getCell()
        try:
            cell.value = val
            print("\n\nModified the concerned excel file.\n\n")
            self.workbook.save(self.path)
            return True
        except:
            print("\n\nCouldn't modify the concerned excel file.\n\n")
            return False

def parsecmd(cmd):
    a = cmd.split(" ")
    return {a[0]: cmd[cmd.index(a[1])-1:].strip()}

def driver_excelmod():
    # print(driver.__code__())
    # print(str(os.path))

    s2t = Speech2Text(mode="mic", src="vosk", output="a_test.txt")
    cfg = Config().get_config()
    xl = ModExcel(config=cfg)
    cmd = None

    while True:
        try:
            if s2t.src == "vosk":
                text = json.loads(s2t.listen())["text"]
            elif s2t.src == "google":
                text = s2t.listen()
            print(f"\n\nCommand given: {text}\n\n")
        
            parsed_tree = parsecmd(text)
            commands = list(parsed_tree.keys())

            print(f"\n\nParsed syntax: {parsed_tree}\n\n")
            print(f"\n\nParsed commands: {commands}\n\n")

            print(f"\n\nConfiguration available:\n\n")
            for i in cfg.keys():
                print(f"{i}\t{cfg[i]}")

            # Execution block
            if commands[0] in cfg.keys():
                print(f"\n\nCommand recognized: {commands[0]}. Parameters: {parsed_tree[commands[0]]}\n\n")
                if commands[0] not in ["get"]:
                    cmd = f"xl.{cfg[commands[0]]}(['{parsed_tree[commands[0]]}'])"
                    
                else:
                    cmd = f"xl.{cfg[commands[0]]}()"
                
                print(f"\n\nBuilt command: {cmd}\n\n")
                exec(cmd)
            else:
                print("\n\nSorry, but your command doesn't match the known ones... \n\n")
        except Exception as e:
            print("\n\nAn error occured. Error details: \t", e)

if __name__ == '__main__':
    driver_excelmod()


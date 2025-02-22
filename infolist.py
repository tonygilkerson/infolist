import cmd
import yaml
import os
import sys
import tty
import termios
from tabulate import tabulate


# read a single character on a unix system
# https://exceptionshub.com/python-read-a-single-character-from-the-user.html
def read_unix(count: int):
    fd = sys.stdin.fileno()

    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(count)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

class MyCLI(cmd.Cmd):
    prompt = '>> '
    infoDataPath = ""
    infoDataList = []
    intro = ""

    def preloop(self):
        """Run this method before the command loop starts."""
        #
        # Where is the infolist data?
        #
        infolistDataPath = os.getenv("INFOLIST_DATA")
        if len(infolistDataPath) == 0:
            # Use default
            infolistDataPath = "~/infolist-data.yaml"

        self.infoDataPath = infolistDataPath
        self.intro = f'\nInfo List, type "help" for available commands. Using ({infolistDataPath})'

        #
        # Load infolist data
        #
        if os.path.exists(infolistDataPath):
            with open(infolistDataPath, "r") as file:
                # self.infoDataList = dict( yaml.safe_load(file).items())
                self.infoDataList = list(yaml.safe_load(file))
        else:
            print(f"Infolist data file not found: {infolistDataPath}")    
            sys.exit(1)
        #
        # do this by default
        #
        self.do_t(self)

    # def __init__(self):
    #     # Call the constructor of the superclass
    #     super().__init__()

    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World! ")

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def do_q(self, line):
        """Exit the CLI."""
        return True

    def default(self, line):
        print(f"you typed: {line}")
        return super().default(line)
    
    
    def do_tt(self, line):
        print("\nPress any key: ")
        char = read_unix(1)
        print(f"you typed: {char}\n")

    def do_t(self, line):
      """Test it."""
      char = ""
      selectIndex = 0
     
      while char != "q":
          table = list()
          for i, item in enumerate(self.infoDataList):
              item["Name"] = item["Name"].replace("[x] ", "")
              item["Name"] = item["Name"].replace("[ ] ", "")
              if i == selectIndex:
                  item["Name"] =  "[x] " + item["Name"]
              else:
                  item["Name"] =  "[ ] " + item["Name"]
              table.append( list(item.values()) )

          # Print table
          os.system('clear')
          print('\nType "Enter" to select, "q" to quit, "," and "." up and down\n')
          outTable = tabulate(
              table, 
              headers=self.infoDataList[0].keys(), 
              tablefmt="simple", 
              stralign="left", 
              maxcolwidths=[None, 30]
          )
          print(outTable)
          
          # 
          # User input
          #
          char = read_unix(1)
          asciiChar = ord(char)
          if asciiChar == 13: # Enter
              print(f"\n\nyou selected: {self.infoDataList[selectIndex]}\n")
              return True
          elif asciiChar == 44: # , aka <
              selectIndex -= 1
          elif asciiChar == 46: # . aka >
              selectIndex += 1
          elif asciiChar == 113: # q
              break
          
          # bounds check
          if selectIndex < 0:
              selectIndex = 0
          elif selectIndex >= len(self.infoDataList):
              selectIndex = len(self.infoDataList) - 1


if __name__ == '__main__':
    MyCLI().cmdloop()
import cmd
import yaml
import os
import sys

from tabulate import tabulate
from internal.utils.io import read_unix

class InfolistCLI(cmd.Cmd):
    prompt = ': '
    infoDataPath = ""
    infoDataList = []
    intro = ""

    def preloop(self):
        """Run this method before the command loop starts."""
        #
        # Where is the infolist data?
        #
        infolistDataPath = os.getenv("INFOLIST_DATA","~/infolist-data.yaml")

        self.infoDataPath = infolistDataPath
        self.intro = f'\nType "help" or "q" to quit. Using ({infolistDataPath})'

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
        self.do_list(self)

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def do_q(self, line):
        """Exit the CLI."""
        return True

    def default(self, line):
        print(f"you typed: {line}")
        return super().default(line)
    
    def do_key(self, line):
        """Read a single keypress."""
        print("\nPress any key: ")
        char = read_unix(1)
        print(f"you typed: {char}\n")

    def do_list(self, line):
      """A list is displayed for you to select an item from."""
      char = ""
      selectIndex = 0
      table = list()

      while char != "q":
          # Create a table for display from the infoDataList
          table = []
          selectField = ""
          for item in self.infoDataList:
              row = [selectField, item["Name"], item["Type"], item["Description"]]
              table.append(row)

          # Sort the display table by Name
          outTable = self.sortTable(table, selectIndex)

          # Display the table
          os.system('clear')
          print(outTable)
          
          # 
          # User input
          #
          char = read_unix()

          # ENTER
          if char == '\r': 
              selectedItemName = table[selectIndex][1]
              self.runItem(selectedItemName)
              break
          
          # UP
          elif char == "UP": 
              selectIndex -= 1

          # DOWN
          elif char == "DOWN": 
              selectIndex += 1
          
          # QUIT
          elif char == 'q':
              break
          else:
              print(f"{char}")
          
          # bounds check
          if selectIndex < 0:
              selectIndex = len(self.infoDataList) - 1 # just wrap around to the bottom
          elif selectIndex >= len(self.infoDataList):
              selectIndex = 0 # just rapp around to the top

    def findItem(self, name):
        """Find an item by name."""
        for item in self.infoDataList:
            if item["Name"] == name:
                return item
        return None
    
    def sortTable(self, table, selectIndex):
        """Sort the table by Name."""
        # Sort input table by Name before display
        table.sort(key=lambda x: x[1])
        table[selectIndex][0] = "=>"
        print('\nType "Enter" to select, "q" to quit, "<" and ">" up and down\n')
        outTable = tabulate(
            table, 
            ["", "Name", "Type", "Description"], 
            tablefmt="simple", 
            stralign="left", 
            maxcolwidths=[None, None, None,45]
        )
        return outTable

    def runItem(self, name):
        """Run an item by name."""
        item = self.findItem(name)

        if item["Type"] == "Command":
            # Command to execute
            command = item["cmd"]["command"]
            args = item["cmd"]["args"]

            # Check to see if we should  show the command
            if item["cmd"]["showCommand"]:
                print(f'\n{" ".join(args)}\n')
            else:
                print("\n")

            # Run the command
            os.execvp(command, args)

        elif item["Type"] == "Link":
            print(f'\nURL:\n{item["URL"]}\n')
        elif item["Type"] == "Note":
            print(f'\nNote:\n\n{item["Note"]}\n')
        else:
            print(f'Unknown type: {item["Type"]}')





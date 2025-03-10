import cmd
import yaml
import os
import sys
from pathlib import Path
from typing import Any

from tabulate import tabulate
from .util import read_unix
from .infolisttypes import Command, Item

class InfolistCLI(cmd.Cmd):
    prompt: str = "\ninfolist: "
    infoDataPath: str = ""
    #infoDataList: list[dict[str, Any]] = [] # DEVTODO del me soon
    infoDataList: list[Item] = []
    intro: str = ""
    
    # sort by Name by default
    sortIndex: int = 1 
    
    # Filter row by items in this list, if empty then no filter
    filters: list[str] = list( )
    
    # Types to display, if empty then all types 
    types: list[str] = list()
    

    def preloop(self):
        """Run this method before the command loop starts."""
        #
        # Where is the infolist data?
        #
        infolistDataPath = os.getenv("INFOLIST_DATA", str(Path.home()) + "/infolist-data.yaml")

        self.infoDataPath = infolistDataPath
        self.intro = f'\nEnter a command, type "help" or "q" to quit. Using ({infolistDataPath})'

        #
        # Load infolist data
        #
        if os.path.exists(infolistDataPath):
            with open(infolistDataPath, "r") as file:
                data: list[dict[str, Any]] = []
                data = list(yaml.safe_load(file))

                
                for row in data:
                    item: Item = Item()
                    item.name = row["Name"]
                    item.description = row["Description"]

                    if "Note" in row:
                        item.note = row["Note"]
                        item.type = "Note"

                    if "URL" in row:
                        item.url = row["URL"]
                        item.type = "Link"

                    if "Command" in row:
                        item.command = Command()
                        item.command.cmd = row["Command"]["cmd"]
                        item.command.args = row["Command"]["args"]
                        item.command.showCommand = row["Command"]["showCommand"]
                        item.type = "Command"
                    self.infoDataList.append(item) 

        else:
            print(f"Infolist data file not found: {infolistDataPath}")    
            sys.exit(1)
        #
        # do this by default
        #
        # self.do_list("")

    def default(self, line: str) -> None:
        print(f"Oops!, unknown command: {line}")
        # return super().default(line)

    def printTypes(self) -> None:
        if len(self.types) > 0:
            for i, t in enumerate(self.types):
                i: int; t: str

                if i == 0:
                    if len(self.types) == 1:
                        print(f"Types: {t}")
                    else:
                        print(f"Types: {t}", end="")
                elif i == len(self.types) - 1:
                    print(f", {t}\n")
                else:
                    print(f", {t}", end="")
    
    def printFilters(self) -> None:
        if len(self.filters) > 0:
            for i, f in enumerate(self.filters):
                i: int; f: str

                if i == 0:
                    if len(self.filters) == 1:
                        print(f"Filters: {f}")
                    else:
                        print(f"Filters: {f}", end="")
                elif i == len(self.filters) - 1:
                    print(f", {f}\n")
                else:
                    print(f", {f}", end="")

    def findItemByName(self, name: str) -> Item:
        """Find an item by name."""
        for item in self.infoDataList:
            item: Item
            if item.name == name:
                return item
        # empty return
        return Item()
    
    def sortTable(self, table: list[list[str]], selectIndex: int) -> str:
        """Sort the table by Name."""
        # Sort input table by Name before display
        table.sort(key=lambda x: x[self.sortIndex])
        table[selectIndex][0] = "=>"
        

        userFriendlyOutput = tabulate(
            table, 
            ["", "Name", "Type", "Description"], 
            tablefmt="simple", 
            stralign="left", 
            maxcolwidths=[None, None, None,45]
        )
        return userFriendlyOutput

    def runItem(self, name: str):
        """Run an item by name."""
        item: Item = self.findItemByName(name)

        if item.type == "Command":
            # Command to execute
            command: str = item.command.cmd
            args: list[str] = item.command.args

            # Check to see if we should  show the command
            if item.command.showCommand:
                print(f'\n{" ".join(args)}\n')
            else:
                print("\n")

            # Run the command
            os.execvp(command, args)

        elif item.type == "Link":
            print(f'\nURL:\n{item.url}\n')
        elif item.type == "Note":
            print(f'\nNote:\n\n{item.note}\n')
        else:
            print(f'Nothing to do, bad type: {item.type}')

    def isFilter(self,content: str):
        """Check if the content is included when filter is applied"""
        # The content is expected to be things like Name or Description
       
        # Assume the content is included when the filter is applied
        isIncluded = True

        # If filters exist then at least one of the filters must be contained in the content
        if len(self.filters) > 0:
            isIncluded = False
            for f in self.filters:
                # a -filter means if content does NOT contain it
                if f.startswith("-"):                  
                  if f[1:].lower() not in content.lower(): 
                      isIncluded = True
                else:
                  if f.lower() in content.lower(): 
                      isIncluded = True
        # Return
        return isIncluded
    
    def isType(self, itemType: str):
        """Check if the row is included when type filter is applied"""
        # Assume the row is included when the type filter is applied
        isIncluded = True

        # If type filter exist then filter rows based on its type
        if len(self.types) > 0:
            isIncluded = False
            for t in self.types:
                if t.lower() in itemType.lower(): 
                    isIncluded = True
        # Return
        return isIncluded
    
    def do_q(self, line: str):
        """Quit and exit the CLI"""
        return True
    def do_cc(self, line: str):
        """Clear the screen"""
        os.system('clear')

    def do_type(self,line: str):
        """Select types. Usage: type <type1> <type2> ..."""
        if line:
            for t in line.split():
                self.types.append(t)
        self.printTypes()

    def do_filter(self,line: str):
        """Add filters. Usage: filter <filter1> <filter2> ... Or will display current filters if no args"""
        if line:
            for s in line.split():
                self.filters.append(s)
        self.printFilters()

    def do_clearfilters(self,line: str):
        """Clear filters, aka no filter, show all"""
        self.filters = list()

    def do_cleartypes(self,line: str):
        """Clear types, aka show all types"""
        self.types = list()

    def do_sort(self, line: str):
        """Sort list by Name. Usage: sort [name|type|description]"""
        if line.lower() == "name":
            self.sortIndex = 1
            self.do_list(line)
        elif line.lower() == "type":
            self.sortIndex = 2
            self.do_list(line)
        elif line.lower() == "description":
            self.sortIndex = 3
            self.do_list(line)
        else:
            print(f"Unknown sort option: '{line}'")
   
    def do_key(self, line: str):
        """Read a single keypress"""
        print("\nPress any key: ")
        char = read_unix()
        print(f"you typed: {char}\n")

    def do_list(self, line: str):
      """Display info list for selection"""
      char = ""
      selectIndex: int = 0
      table:list[list[str]] = list()

      while char != "q":
          # Create a table for display from the infoDataList
          table = []
          selectField = ""

          for item in self.infoDataList:
              
              # Check to see if Name or Description passes the filter
              # Also check if it is the correct type
              nameDesc: str = item.name + " " + item.description
              if self.isFilter(nameDesc) and self.isType(item.type):  
                  row: list[str] = [selectField, item.name, item.type, item.description]
                  table.append(row)

          # Sort the display table by Name
          outTable = self.sortTable(table, selectIndex)

          # Display the table
          os.system('clear')
          print('\nType "Enter" to select, "q" to quit, UP and DOWN keys to change selection\n')
          self.printFilters()
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

          
          # bounds check
          if selectIndex < 0:
              selectIndex = len(self.infoDataList) - 1 # just wrap around to the bottom
          elif selectIndex >= len(self.infoDataList):
              selectIndex = 0 # just rap around to the top





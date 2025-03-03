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
    
    # sort by Name by default
    sortIndex = 1 
    
    # Filter row by items in this list, if empty then no filter
    filters = list()
    
    # Types to display, if empty then all types 
    types = list()

    def preloop(self):
        """Run this method before the command loop starts."""
        #
        # Where is the infolist data?
        #
        infolistDataPath = os.getenv("INFOLIST_DATA","~/infolist-data.yaml")

        self.infoDataPath = infolistDataPath
        self.intro = f'\nEnter a command, type "help" or "q" to quit. Using ({infolistDataPath})'

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
        # self.do_list("")

    def default(self, line):
        print(f"you typed: {line}")
        return super().default(line)

    def printTypes(self):
        if len(self.types) > 0:
            for i, t in enumerate(self.types):
                if i == 0:
                    if len(self.types) == 1:
                        print(f"Types: {t}")
                    else:
                        print(f"Types: {t}", end="")
                elif i == len(self.types) - 1:
                    print(f", {t}\n")
                else:
                    print(f", {t}", end="")
    
    def printFilters(self):
        if len(self.filters) > 0:
            for i, f in enumerate(self.filters):
                if i == 0:
                    if len(self.filters) == 1:
                        print(f"Filters: {f}")
                    else:
                        print(f"Filters: {f}", end="")
                elif i == len(self.filters) - 1:
                    print(f", {f}\n")
                else:
                    print(f", {f}", end="")

    def findItem(self, name):
        """Find an item by name."""
        for item in self.infoDataList:
            if item["Name"] == name:
                return item
        return None
    
    def sortTable(self, table, selectIndex):
        """Sort the table by Name."""
        # Sort input table by Name before display
        table.sort(key=lambda x: x[self.sortIndex])
        table[selectIndex][0] = "=>"
        
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

    def isFilter(self, content):
        """Check if the content is included when filter is applied"""
        # The content is expected to be things like Name or Description
       
        # Assume the content is included when the filter is applied
        included = True

        # If filters exist then at least one of the filters must be contained in the content
        if len(self.filters) > 0:
            included = False
            for f in self.filters:
                if f.lower() in content.lower(): 
                    included = True
        # Return
        return included
    
    def do_q(self, line):
        """Quit and exit the CLI"""
        return True
    def do_cc(self, line):
        """Clear the screen"""
        os.system('clear')

    def do_type(self,line):
        """Select types. Usage: type <type1> <type2> ..."""
        if line:
            for t in line.split():
                self.types.append(t)
        self.printTypes()

    def do_filter(self,line):
        """Add filters. Usage: filter <filter1> <filter2> ... Or will display current filters if no args"""
        if line:
            for s in line.split():
                self.filters.append(s)
        self.printFilters()

    def do_clsfilters(self,line):
        """Clear filter, aka show all"""
        self.filters = list()

    def do_sort(self, line):
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
   
    def do_key(self, line):
        """Read a single keypress"""
        print("\nPress any key: ")
        char = read_unix()
        print(f"you typed: {char}\n")

    def do_list(self, line):
      """Display info list for selection"""
      char = ""
      selectIndex = 0
      table = list()

      while char != "q":
          # Create a table for display from the infoDataList
          table = []
          selectField = ""

          for item in self.infoDataList:
              
              # Check to see if Name passes the filter
              if self.isFilter(item["Name"]):  
                  row = [selectField, item["Name"], item["Type"], item["Description"]]
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





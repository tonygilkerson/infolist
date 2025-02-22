import cmd
import yaml
import os
import sys

class MyCLI(cmd.Cmd):
    prompt = '>> '
    infoDataPath = ""
    infoDataDict = {}
    intro = ""

    def __init__(self):
        # Call the constructor of the superclass
        super().__init__()

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
                self.infoDataDict = dict( yaml.safe_load(file).items())
        else:
            print(f"Infolist data file not found: {infolistDataPath}")    
            sys.exit(1)

    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World! ")

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def do_x(self, line):
        """Exit the CLI."""
        return True

    def do_test(self, line):
        """Test it."""
        # print(infoSorted["dddaaa xxx"])
        print("test")
            
if __name__ == '__main__':
    MyCLI().cmdloop()
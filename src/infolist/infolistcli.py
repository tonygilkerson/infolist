"""My Infolist"""
from typing import Any
import os
import sys
import cmd
import argparse
from pathlib import Path
from importlib.metadata import version
import yaml

from tabulate import tabulate
from .util import read_unix
from .infolisttypes import Item

class InfolistCLI(cmd.Cmd):
    prompt: str = "\ninfolist: "
    infoDataPath: str = ""
    infoDataList: list[Item] = []
    intro: str = ""

    # sort by Name by default
    sortIndex: int = 1

    # Filter row by items in this list, if empty then no filter
    filters: list[str] = list()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Infolist CLI")
        parser.add_argument(
            "--version", "-v", action="store_true", help="Display infolist version"
        )
        parser.add_argument(
            "--filter", "-f", type=str, nargs="*", help="Initial filters"
        )
        args = parser.parse_args()

        if args.version:
            print(f"infolist version: {self.get_version()}")
            sys.exit(0)

        if args.filter:
            self.filters = args.filter


    def preloop(self):
        """Run this method before the command loop starts."""
        #
        # Process command line arguments
        #
        self.parse_args()

        #
        # Where is the infolist data?
        #
        infolistDataPath = os.getenv(
            "INFOLIST_DATA", str(Path.home()) + "/infolist-data.yaml"
        )

        self.infoDataPath = infolistDataPath
        self.intro = (
            f'\nEnter a command, type "help" or "q" to quit. Using ({infolistDataPath})'
        )

        #
        # Load infolist data
        #
        if os.path.exists(infolistDataPath):
            with open(infolistDataPath, "r", encoding="utf-8") as file:
                data: list[dict[str, Any]] = []
                data = list(yaml.safe_load(file))

                for row in data:
                    item: Item = Item()
                    item.name = row["Name"]
                    item.description = row["Description"]
                    item.tags = row["Tags"]
                    item.note = row["Note"]
                    self.infoDataList.append(item)
        else:
            print(f"Infolist data file not found: {infolistDataPath}")
            sys.exit(1)

        # Call do_ll() to display the list when the program is first invoked
        self.do_ll("list")

    def default(self, line: str) -> None:
        print(f"Oops!, unknown command: {line}")
        # return super().default(line)

    def get_version(self) -> str:
        """Retrieve the version of the infolist package."""
        return version("infolist")

    def printFilters(self) -> None:
        if len(self.filters) > 0:
            for i, f in enumerate(self.filters):
                i: int
                f: str

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

    def sortTable(self, table: list[list[str]], select_index: int) -> str:
        """Sort the table by Name."""
        # Sort input table by Name before display
        if len(table) == 0:
            return f"\n\nNo items to display\n\n"
        table.sort(key=lambda x: x[self.sortIndex])
        table[select_index][0] = "=>"

        userFriendlyOutput = tabulate(
            table,
            ["", "Name", "Tags", "Description"],
            tablefmt="simple",
            stralign="left",
            maxcolwidths=[None, None, None, 60],
        )
        return userFriendlyOutput

    def show_item(self, name: str):
        """Run an item by name."""
        item: Item = self.findItemByName(name)
        print(f"\nNote:\n\n{item.note}\n")

    def isFilter(self, content: str):
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

    def do_q(self, line: str):
        """Quit and exit the CLI"""
        return True
    def do_version(self, line: str):
        """Print the version of InfoList"""
        print(f"infolist version: {self.get_version()}")

    def do_cc(self, line: str):
        """Clear the screen"""
        os.system("clear")

    def do_f(self, line: str):
        """Add filters. Usage: filter <filter1> <filter2> ... Or will display current filters if no args"""
        if line:
            for s in line.split():
                self.filters.append(s)
        self.printFilters()

    def do_cf(self, line: str):
        """Clear filters, aka no filter, show all"""
        self.filters = list()

    def do_key(self, line: str):
        """Read a single keypress"""
        print("\nPress any key: ")
        char = read_unix()
        print(f"you typed: {char}\n")

    def do_ll(self, line: str):
        """Display info list for selection"""
        char = ""
        select_index: int = 0
        table: list[list[str]] = list()

        while char != "q":
            # Create a table for display from the infoDataList
            table = []
            selectField = ""

            for item in self.infoDataList:

                # Filter content is name, description and tags
                tags = ", ".join(item.tags)
                content: str = item.name + " " + item.description + " " + tags

                # Check to see if content passes the filter
                if self.isFilter(content):
                    row: list[str] = [
                        selectField,
                        item.name,
                        tags,
                        item.description,
                    ]
                    table.append(row)

            # Sort the display table by Name
            outTable = self.sortTable(table, select_index)

            # Display the table
            os.system("clear")
            print(
                '\nPress "return" to display item, "q" to quit, UP and DOWN keys to change selection\n'
            )
            self.printFilters()
            print(outTable)

            #
            # User input
            #
            char = read_unix()

            # ENTER
            if char == "\r":
                selectedItemName = table[select_index][1]
                self.show_item(selectedItemName)
                break

            # UP
            elif char == "UP":
                select_index -= 1

            # DOWN
            elif char == "DOWN":
                select_index += 1

            # QUIT
            elif char == "q":
                break

            # bounds check
            if select_index < 0:
                select_index = (
                    len(self.infoDataList) - 1
                )  # just wrap around to the bottom
            elif select_index >= len(self.infoDataList):
                select_index = 0  # just rap around to the top

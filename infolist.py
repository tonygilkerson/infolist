#!/usr/bin/python3.9
import cmd
import yaml

class MyCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to MyCLI. Type "help" for available commands.'

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
        with open("/home/tgilkerson/infolsit-config.yaml", "r") as file:
            conf = yaml.safe_load(file)
            for item in conf['infolist']:
                print(item['name'])
                print(item['desc'])
                print()
            
if __name__ == '__main__':
    MyCLI().cmdloop()
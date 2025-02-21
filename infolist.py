import cmd
import yaml

class MyCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'InfoCLI, Type "help" for available commands.'

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
            infoData = yaml.safe_load(file)
            infoSorted = dict(sorted(infoData.items()))
            print(infoSorted["dddaaa xxx"])
            
if __name__ == '__main__':
    MyCLI().cmdloop()
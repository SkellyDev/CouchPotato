'''
This is a script for parsing command 
and pass it as input for action script
to call correct method
'''


class CommandParse:
    def __init__(self, RowCommand):
        self.row_command = RowCommand
        self.parse = ""

    def parse(self):
        # Attenion!!!
        # return row command first before we finishing command parsing part
        return self.row_command

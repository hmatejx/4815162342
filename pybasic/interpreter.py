
"""Class representing a BASIC interpreter.
This is a list of statements, ordered by
line number.

Needs a Computer simulator such as TerminalComputer for interaction.

"""

from .basictoken import BASICToken as Token
from .lexer import Lexer
from .basicparser import BASICParser
from .program import Program
from .terminalcomputer import TerminalComputer
from sys import maxsize


class Interpreter():

    def __init__(self, computer = None):
        self.__lexer = Lexer()
        self.__computer = TerminalComputer() if computer == None else computer
        self.__parser = BASICParser(self.__computer)
        self.__program = Program(self.__parser)


    def interactive(self):
        """Run an interactive session with the interpreter
        """
        self.__computer.clrscr()
        self.__computer.htab(1)
        self.__computer.vtab(24)

        # Continuously accept user input and act on it until
        # the user enters 'EXIT'
        while True:
            self.__computer.print(']', end='')
            stmt = self.__computer.input().strip()

            try:
                tokenlist = self.__lexer.tokenize(stmt)

                # Execute commands directly, otherwise
                # add program statements to the stored
                # BASIC program

                if len(tokenlist) > 0:

                    # Exit the interpreter
                    if tokenlist[0].category == Token.EXIT:
                        break

                    # Add a new program statement, beginning
                    # a line number
                    elif tokenlist[0].category == Token.UNSIGNEDINT\
                        and len(tokenlist) > 1:
                        self.__program.add_stmt(tokenlist)

                    # Delete a statement from the program
                    elif tokenlist[0].category == Token.UNSIGNEDINT \
                            and len(tokenlist) == 1:
                        self.__program.delete_statement(int(tokenlist[0].lexeme))

                    # Execute the program
                    elif tokenlist[0].category == Token.RUN:
                        try:
                            self.__program.execute()

                        except KeyboardInterrupt:
                            self.__computer.print("PROGRAM TERMINATED")

                    # List the program
                    elif tokenlist[0].category == Token.LIST:
                        if len(tokenlist) != 1 and len(tokenlist) != 4:
                            raise RuntimeError('?SYNTAX ERROR')
                        start = 0
                        stop = maxsize
                        if len(tokenlist) == 4:
                            if tokenlist[1].category == Token.UNSIGNEDINT and \
                            tokenlist[2].category == Token.MINUS and \
                            tokenlist[3].category == Token.UNSIGNEDINT:
                                start = int(tokenlist[1].lexeme)
                                stop = int(tokenlist[3].lexeme)
                            else:
                                raise RuntimeError('?SYNTAX ERROR')
                        line_numbers = self.__program.line_numbers()
                        for line_number in [l for l in line_numbers if l >= start and l <= stop]:
                            self.__computer.print(str(line_number) + ' ', end='', flush=False)
                            statement = self.__program.get_line(line_number)
                            for token in statement:
                                if token.category == Token.STRING:
                                    self.__computer.print('"' + token.lexeme + '" ', end='', flush=False)
                                else:
                                    self.__computer.print(token.lexeme + ' ', end='', flush=False)
                            self.__computer.print(end='\n', flush=True)

                    # Save the program to disk
                    elif tokenlist[0].category == Token.SAVE:
                        lines = []
                        line_numbers = self.__program.line_numbers()
                        for line_number in line_numbers:
                            line = str(line_number) + ' '
                            statement = self.__program.get_line(line_number)
                            for token in statement:
                                if token.category == Token.STRING:
                                    line += '"' + token.lexeme + '" '
                                else:
                                    line += token.lexeme + ' '
                            line = line.rstrip()
                            lines.append(line + '\n')
                        try:
                            with open(tokenlist[1].lexeme.upper(), "w") as outfile:
                                outfile.writelines(lines)
                        except OSError:
                            raise OSError("Could not save file")
                        self.__computer.print("Program saved to file")

                    # Load the program from disk
                    elif tokenlist[0].category == Token.LOAD:
                        try:
                            with open(tokenlist[1].lexeme.upper(), 'r') as infile:
                                self.__program.delete()
                                lines = infile.readlines()
                                for line in lines:
                                    tokenlist = self.__lexer.tokenize(line.strip())
                                    self.__program.add_stmt(tokenlist)
                                infile.close()
                        except OSError:
                            raise OSError("Could not read file")
                        self.__computer.print("Program read from file")

                    # Delete the program from memory
                    elif tokenlist[0].category == Token.NEW:
                        self.__program.delete()

                    # Clear all variables
                    elif tokenlist[0].category == Token.CLEAR:
                        self.__parser.clear()

                    # otherwise, interpret as BASIC statement
                    else:
                        self.__parser.parse(tokenlist, 1)

            # Trap all exceptions so that interpreter
            # keeps running
            except Exception as e:
                self.__computer.print(str(e), end='\n')


    def load(self, filename):
        """Loads the program from the
        file identified by filename

        :param filename: Name of the .BAS file
        """
        self.__program.load(filename)


    def execute(self):
        """Executes the current program

        :return: Returns the 'exit status' held in variable RET
        """
        if self.__program is not None:
            self.__program.execute()


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.interactive()

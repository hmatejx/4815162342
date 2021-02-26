#! /usr/bin/python

from pybasic.basictoken import BASICToken as Token
from pybasic.basicparser import BASICParser
from pybasic.lexer import Lexer
from pybasic.program import Program
from apple2.computer import Computer
from sys import maxsize


lexer = None
computer = None
parser = None


def Interpreter():
    global lexer, computer, parser
    if lexer == None: lexer = Lexer()
    if computer == None: computer = Computer()
    if parser == None: parser = BASICParser(computer)
    program = Program(parser)

    computer.clrscr()
    computer.htab(1)
    computer.vtab(24)

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:
        computer.print(']', end='')
        stmt = computer.input().strip()

        try:
            tokenlist = lexer.tokenize(stmt)

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
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        computer.print("PROGRAM TERMINATED")

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
                    line_numbers = program.line_numbers()
                    for line_number in [l for l in line_numbers if l >= start and l <= stop]:
                        computer.print(str(line_number) + ' ', end=False, flush=False)
                        statement = program.get_line(line_number)
                        for token in statement:
                            if token.category == Token.STRING:
                                computer.print('"' + token.lexeme + '" ', end=False, flush=False)
                            else:
                                computer.print(token.lexeme + ' ', end=False, flush=False)
                        computer.print(end=True, flush=True)

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    lines = []
                    line_numbers = program.line_numbers()
                    for line_number in line_numbers:
                        line = str(line_number) + ' '
                        statement = program.get_line(line_number)
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
                    computer.print("Program saved to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    try:
                        with open(tokenlist[1].lexeme.upper(), 'r') as infile:
                            program.delete()
                            lines = infile.readlines()
                            for line in lines:
                                tokenlist = lexer.tokenize(line.strip())
                                program.add_stmt(tokenlist)
                            infile.close()
                    except OSError:
                        raise OSError("Could not read file")
                    computer.print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Clear all variables
                elif tokenlist[0].category == Token.CLEAR:
                    parser.clear()

                # otherwise, interpret as BASIC statement
                else:
                    parser.parse(tokenlist, 1)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            computer.print(str(e), end=True)


if __name__ == "__main__":
    Interpreter()

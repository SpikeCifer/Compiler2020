# ---------------------------------------------------------------------------------------------
#                                         Miminal++_Compiler.py
#
# A complete compiler for the Minimal ++ language developed as a college project
# More info on the report as well as the given pdf files
#
# Teacher: Dr G.Manis
#
# Students
# Names: Stylianos Zappids, Zisimos Parasxis
# Usernames: cse52971 cse53059
# AMs: 2971, 3059
#
# Python Edition 3.7
# Developed in PyCharm
# ---------------------------------------------------------------------------------------------
import _io
import string
import sys
from collections import deque


class Error:
    def __init__(self, error_type, error_cause, error_suggestion='No suggestion'):
        error_id = error_type + ": " + error_cause
        error_location = "\nIn Line: " + str(minimal.line_index) + ", Character: " + str(minimal.char_index)
        error_solution = "\nSuggestion: " + error_suggestion
        exit(error_id + error_location + error_solution)


class Compiler:
    @staticmethod
    def load_source():
        file = filename.split(".")
        if file[1] != "min":
            exit("SYSTEM ERROR: This compiler only works for .min files")
        try:
            return open(filename, 'r')
        except FileNotFoundError:
            exit("SYSTEM ERROR: File not found!")

    def __init__(self):
        """ Compiler: The main class of the program.
            It contains all the tools required for the compiler to work properly as attributes

            LP: The Lexical Analyzer
            SP: The Syntax Parser
            IC: The Intermediate code generator
            ST: The Symbol Table
            FC: The Final Code creator

            Also it has two addional attributes for handling errors
            line_index: Points at the line where the error appears
            char_index: Points at the character after which the error appears (Not accurate)
        """
        self.LP = Lexer()
        self.SP = Parser()
        self.IC = ICGenerator()
        self.ST = SymbolTable()
        self.FC = Finalizer()

        self.line_index = 0
        self.char_index = 0

        self.main_framelength = 0
        self.program_name = ''


# Lectical Analysis
class Lexical(Error):
    Error1 = 13
    Error2 = Error1 + 1
    Error3 = Error1 + 2
    Error4 = Error1 + 3
    Error5 = Error1 + 4

    errors = {
        Error1: "1: Digits can not be followed by characters",
        Error2: "2: Closed long comment without opening one",
        Error3: "3: Opened second comment inside another one",
        Error4: "4: EOF while in long comment",
        Error5: "5: Invalid symbol"
    }

    def __init__(self, cause, char):
        msg = self.errors.get(cause)
        if cause == self.Error5:
            msg += " '" + char + "'"
        super().__init__('LexicalError', msg)


class Lexeme:
    IDTK = 1
    CONSTANTTK = 2

    # Operators
    ADDTK = 3
    MULTIPLYTK = 4
    BRACKETTK = 5
    SEPARATORTK = 6
    COMPARATORTK = 7
    DECLARATORTK = 8

    # Key words
    PROGRAMTK = 9
    DECLARETK = 10
    IFTK = 11
    THENTK = 12
    ELSETK = 13
    WHILETK = 14
    DOUBLEWHILETK = 15
    LOOPTK = 16
    EXITTK = 17
    FORCASETK = 18
    INCASETK = 19
    WHENTK = 20
    DEFAULTTK = 21
    NOTTK = 22
    ANDTK = 23
    ORTK = 24
    FUNCTIONTK = 25
    PROCEDURETK = 26
    CALLTK = 27
    RETURNTK = 28
    INTK = 29
    INOUTTK = 30
    INPUTTK = 31
    PRINTTK = 32

    # EOF
    EOFTK = 33

    dictionary = {
        # Add ops
        '+': ADDTK,
        '-': ADDTK,
        # Multiply ops
        '*': MULTIPLYTK,
        '/': MULTIPLYTK,
        # Brackets
        '(': BRACKETTK,
        ')': BRACKETTK,
        '[': BRACKETTK,
        ']': BRACKETTK,
        '{': BRACKETTK,
        '}': BRACKETTK,
        # Separators
        ':': SEPARATORTK,
        ';': SEPARATORTK,
        ',': SEPARATORTK,
        # relops
        '<': COMPARATORTK,
        '>': COMPARATORTK,
        '=': COMPARATORTK,
        '<=': COMPARATORTK,
        '>=': COMPARATORTK,
        '<>': COMPARATORTK,
        # declator
        ':=': DECLARATORTK,
        # Key words
        'program': PROGRAMTK,
        'declare': DECLARETK,
        'if': IFTK,
        'then': THENTK,
        'else': ELSETK,
        'while': WHILETK,
        'doublewhile': DOUBLEWHILETK,
        'loop': LOOPTK,
        'exit': EXITTK,
        'forcase': FORCASETK,
        'incase': INCASETK,
        'when': WHENTK,
        'default': DEFAULTTK,
        'not': NOTTK,
        'and': ANDTK,
        'or': ORTK,
        'function': FUNCTIONTK,
        'procedure': PROCEDURETK,
        'call': CALLTK,
        'return': RETURNTK,
        'in': INTK,
        'inout': INOUTTK,
        'input': INPUTTK,
        'print': PRINTTK,
        '': EOFTK,
    }
    key_words = ["program", "declare", "if", "else", "while", "doublewhile", "loop", "exit", "forcase", "incase",
                 "when", "default", "not", "and", "or", "function", "procedure", "call", "return", "in",
                 "inout", "input", "print", "then"]
    relops = ['<', '>', '=', '<=', '>=', '<>']

    def __init__(self, word, char):
        """ Lexeme: An object with 2 attributes
            token:  The token recognized by the Parser
            word:   The actual word

        :param word: The constructed word
        :param char: The last character
        """
        full_word = word + char
        minimal.LP.pos_index -= 1
        if full_word in self.dictionary:
            minimal.LP.pos_index += 1
            self.token = self.dictionary.get(full_word, self.IDTK)
            self.word = full_word
            return

        self.word = word
        if word.isdigit():
            self.token = self.CONSTANTTK
            if int(self.word) > 32767 or int(self.word) < -32767:
                print("Warning! Number " + str(self.word) + " is out of range")
            return
        self.token = self.dictionary.get(word, self.IDTK)
        return

    def __str__(self):
        return "Word: " + self.word + " with Token: " + str(self.token)


class Lexer:
    """ Lexer: The tool that reads from the source code, breaks it into words
        and then returns the tokens to the parser. Lexer has a few states that goes
        through while analyzing the source code.

        alphabet: The symbols that the lexer understands

        DFA: A code implementation of the Finite Automata the Lexer uses
    """
    source: _io.TextIOWrapper
    start_state = 0
    special1 = start_state + 1  # Read * Symbol
    special2 = start_state + 2  # Read / Symbol

    chars_state = 3
    numbs_state = 4

    long_comment = 5
    special3 = long_comment + 1  # Read * inside long comment
    special4 = long_comment + 2  # Read / inside long comment

    short_comment = 8
    special5 = short_comment + 1  # Read * inside short comment
    special6 = short_comment + 2  # Read / inside short comment

    temp = 11  # < > or :
    return_state = 12

    comments = [short_comment, special3, special4, long_comment, special5, special6]
    alphabet = {
        '+': 2,
        '-': 2,
        '*': 3,
        '/': 4,
        '<': 5,
        '>': 6,
        '=': 7,
        ':': 8,
        ';': 9,
        ',': 9,
        '(': 10,
        ')': 10,
        '[': 10,
        ']': 10,
        '{': 10,
        '}': 10,
        '\n': 11,
        ' ': 12,
        '\t': 12,
        '': 13
    }

    DFA = [
        # start_state
        [chars_state, numbs_state, return_state, special1, special2, temp, temp,
         return_state, temp, return_state, return_state, start_state, start_state, return_state,
         Lexical.Error5],

        # Special 1
        [return_state, return_state, return_state, return_state, Lexical.Error2, return_state, return_state,
         return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state],

        # Special 2
        [return_state, return_state, return_state, long_comment, short_comment, return_state, return_state,
         return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state],

        # chars_state
        [chars_state, chars_state, return_state, return_state, return_state, return_state, return_state,
         return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state],

        # numbs_state
        [Lexical.Error1, numbs_state, return_state, return_state, return_state, return_state, return_state,
         return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state],

        # Long_comment
        [long_comment, long_comment, long_comment, special3, special4, long_comment, long_comment,
         long_comment, long_comment, long_comment, long_comment, long_comment, long_comment, Lexical.Error4,
         long_comment],

        # Special 3
        [long_comment, long_comment, long_comment, long_comment, start_state, long_comment, long_comment,
         long_comment, long_comment, long_comment, long_comment, long_comment, long_comment, Lexical.Error4,
         long_comment],

        # Special 4
        [long_comment, long_comment, long_comment, Lexical.Error3, Lexical.Error3, long_comment, long_comment,
         long_comment, long_comment, long_comment, long_comment, long_comment, long_comment, Lexical.Error4,
         long_comment],

        # Short Comment
        [short_comment, short_comment, short_comment, special5, special6, short_comment, short_comment,
         short_comment, short_comment, short_comment, short_comment, start_state, short_comment, return_state,
         short_comment],

        # Special 5
        [short_comment, short_comment, short_comment, short_comment, Lexical.Error2, short_comment, short_comment,
         short_comment, short_comment, short_comment, short_comment, start_state, short_comment, return_state,
         short_comment],

        # Special 6
        [short_comment, short_comment, short_comment, Lexical.Error3, Lexical.Error3, short_comment, short_comment,
         short_comment, short_comment, short_comment, short_comment, start_state, short_comment, return_state,
         short_comment],

        # temp
        [return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state, return_state, return_state, return_state, return_state, return_state, return_state,
         return_state]
    ]

    def __init__(self):
        self.pos_index = 0
        self.source = Compiler.load_source()

    def identify(self, char):
        """ Check if given char is in the compiler's alphabet and returns the assigned column

        :param char: Character given for identification
        :return: The columned assigned for that char (special case 14 for invalid characters)
        """
        if char in string.ascii_letters:  # Only Latin Characters
            return 0
        elif char.isnumeric():
            return 1
        else:
            if char == '\n':
                minimal.line_index += 1
                minimal.char_index = 0
            return self.alphabet.get(char, 14)

    # Create the lexeme and update the starting position
    def handle_return(self, word, char):
        result = Lexeme(word, char)
        self.source.seek(self.pos_index)
        return result

    def lex(self):
        char = word = ''
        state = self.start_state
        line = self.source.readline()
        while line != '':
            for char in line:
                minimal.char_index += 1
                self.pos_index += 1

                state = self.DFA[state][self.identify(char)]
                if state == self.return_state:
                    return self.handle_return(word, char)
                elif state in Lexical.errors:
                    Lexical(state, char)
                elif state in self.comments or state == self.start_state:
                    word = ""
                elif char not in [' ', '\t', '\n'] and len(word) <= 30:
                    word += char

            line = self.source.readline()
            self.pos_index += 1

        state = self.DFA[state][13]
        if state in Lexical.errors:
            Lexical(state, char)
        elif state == self.return_state:
            return self.handle_return(word, char)
        exit("Something went very wrong")


# Syntax Analysis
class Parse(Error):
    def __init__(self, error_cause, suggestion='No Suggestion'):
        super().__init__('SyntaxError', error_cause, error_suggestion=suggestion)


class Parser:
    """ Parser: The syntax analyzing tool, goes through all of the source code checking whether it follows the syntax
        of the language or not.

        This class also contains the syntax of the minimal++ language
    """

    def __init__(self):
        self.lexeme = None

    # --------------------------- Starting ---------------------------
    def program(self):
        self.lexeme = minimal.LP.lex()
        if self.lexeme.token == Lexeme.PROGRAMTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                minimal.program_name = self.lexeme.word
                self.lexeme = minimal.LP.lex()
                minimal.ST.add_scope()
                if self.lexeme.word == '{':
                    self.lexeme = minimal.LP.lex()
                    self.block(minimal.program_name)
                    if self.lexeme.word == '}':
                        minimal.ST.delete_scope()
                        return  # This is the proper end of the compiling process

                    # Possible Errors Part
                    msg = ""
                    final_token = self.lexeme
                    self.lexeme = minimal.LP.lex()

                    if final_token.word == ";" and self.lexeme.word == "}":
                        msg += "The ';' separator is unnecessary after the program's last statement."
                    elif final_token.word in Lexeme.key_words:
                        msg += "Statements not separated by ';' operator"
                    else:
                        msg += "Check if multiple statements are not inside {} blocks"

                    Parse("Expected '}' bracket to end program's block\n", msg)
                Parse("Expected '{' character to start program's block", "Add the appropriate symbol")
            Parse("A program should always have a name ", "Name the program")
        Parse("Keyword 'program' is required to start", "Add the appropriate keyword")

    def block(self, name):
        self.declarations()
        self.subprograms()
        if len(minimal.ST.scopes) > 1:
            minimal.ST.scopes[-2].entities[-1].startQuad = minimal.IC.next_quad()
        minimal.IC.generate_quad("begin_block", name, "_", "_")
        self.statements()
        if name == minimal.program_name:
            minimal.IC.generate_quad("halt", "_", "_", "_")
        minimal.IC.generate_quad("end_block", name, "_", "_")

    # ------------------------- Declarations -------------------------
    def declarations(self):
        while self.lexeme.token == Lexeme.DECLARETK:
            self.lexeme = minimal.LP.lex()
            char = self.varlist()
            if self.lexeme.word == ';':
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Either ',' or ';' separator was expected after variable " + char, "Find what is missing")

    def varlist(self):
        var = ""
        if self.lexeme.token == Lexeme.IDTK:
            var = self.lexeme.word
            minimal.ST.add_entity(Variable(var))
            self.lexeme = minimal.LP.lex()
            while self.lexeme.word == ',':
                self.lexeme = minimal.LP.lex()
                if self.lexeme.token == Lexeme.IDTK:
                    var = self.lexeme.word
                    minimal.ST.add_entity(Variable(var))
                    self.lexeme = minimal.LP.lex()
                else:
                    Parse("Expected variable's name after ',' character",
                          "Either add another variable or remove the last ,")
        elif self.lexeme.word == ',':
            Parse("Expected a variable's name before the first ',' character", "Add the first variable")
        return var  # Return the last character written before the error pops up

    def subprograms(self):
        while self.lexeme.token in [Lexeme.FUNCTIONTK, Lexeme.PROCEDURETK]:
            self.subprogram()

    def subprogram(self):
        if self.lexeme.token == Lexeme.FUNCTIONTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                function_name = self.lexeme.word
                if function_name == minimal.program_name:
                    Semantic(6)
                minimal.ST.add_entity(Subprogram(function_name, 1))
                minimal.ST.add_scope()
                self.lexeme = minimal.LP.lex()
                self.funcbody(function_name)
                minimal.ST.delete_scope()
            elif self.lexeme.word in Lexeme.key_words:
                Parse("A function can't have a key word as a name")
            else:
                Parse("A function should always have a name", )

        elif self.lexeme.token == Lexeme.PROCEDURETK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                procedure_name = self.lexeme.word
                if procedure_name == minimal.program_name:
                    Semantic(6)
                minimal.ST.add_entity(Subprogram(procedure_name, 2))
                minimal.ST.add_scope()
                self.lexeme = minimal.LP.lex()
                self.funcbody(procedure_name)
                minimal.ST.delete_scope()
            elif self.lexeme.word in Lexeme.key_words:
                Parse("A procedure can't have a key word as a name")
            else:
                Parse("A procedure should always have a name")

    def funcbody(self, name):
        self.formalpars()
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "{":
            self.lexeme = minimal.LP.lex()
            self.block(name)
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "}":
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Expected '}' char to end the subprogram's block",
                      "Check if multiple statements are not between { } brackets")
        else:
            Parse("Expected '{' to start the subprogram's block",
                  "Add the approriate symbol")

    def formalpars(self):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            self.formalparlist()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
            else:
                if self.lexeme.token == Lexeme.IDTK:
                    Parse("Parameter " + self.lexeme.word + "'s type has not been declared",
                          "Parameter " + self.lexeme.word + " identify yourself!")
                else:
                    Parse("Expected either another variable name or ')' to stop declaring parameters")
        else:
            Parse("Expected '(' character to start declaring parameters")
        return

    def formalparlist(self):
        if self.lexeme.token == Lexeme.INTK or self.lexeme.token == Lexeme.INOUTTK:
            self.formalparitem()
            while self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ",":
                self.lexeme = minimal.LP.lex()
                if self.lexeme.token not in [Lexeme.INTK, Lexeme.INOUTTK]:
                    Parse("Expected another parameter's type after ','")
                self.formalparitem()

    def formalparitem(self):  # The parameters as shown in function
        if self.lexeme.token == Lexeme.INTK:
            par_type = self.lexeme.word
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                minimal.ST.add_entity(Parameter(self.lexeme.word, 1))
                minimal.ST.add_argument(1)
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Expected parameter's name after type " + par_type)
        elif self.lexeme.token == Lexeme.INOUTTK:
            par_type = self.lexeme.word
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                minimal.ST.add_entity(Parameter(self.lexeme.word, 2))
                minimal.ST.add_argument(2)
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Expected parameter's name after type " + par_type)

    @staticmethod
    def compare_lists(formal_pars, actual_pars):
        if len(formal_pars) != len(actual_pars):
            Semantic(5)
        for i in range(len(formal_pars)):
            if str(formal_pars[i]) != actual_pars[i][0]:
                Semantic(4, actual_pars[i][1])

    def actualpars(self, subprogram):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            parlist = self.actualparlist()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                # When you are done compare the actual parameters with the formal parameters
                self.compare_lists(subprogram.arguments, parlist)
                for par in parlist:
                    minimal.IC.generate_quad("par", par[1], par[0], '_')
                self.lexeme = minimal.LP.lex()
            else:
                msg = "Expected right bracket ) to close call parameters"
                cause = "Add appropriate symbol"
                if self.lexeme.token == Lexeme.IDTK:
                    cause = "\nSuggestion: Parameter " + self.lexeme.word + "identify yourself"
                Parse(msg, cause)
        else:
            Parse("Expected opening bracket ( to open call parameters")

    def actualparlist(self):
        parlist = []
        if self.lexeme.token == Lexeme.INTK or self.lexeme.token == Lexeme.INOUTTK:
            par_item = self.actualparitem()
            parlist.append(par_item)
            while self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ",":
                self.lexeme = minimal.LP.lex()
                parlist.append(self.actualparitem())
        return parlist

    def actualparitem(self):
        par_type = ''
        var = None
        if self.lexeme.token == Lexeme.INTK:
            par_type = 'CV'
            self.lexeme = minimal.LP.lex()
            var = self.expression()
        elif self.lexeme.token == Lexeme.INOUTTK:
            par_type = 'REF'
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                var = self.lexeme.word
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Variable name was expected")
        return par_type, var  # Return parameter type and name

    # ------------------------- Statements -------------------------
    def assignment_stat(self, var):
        if self.lexeme.token == Lexeme.DECLARATORTK:
            self.lexeme = minimal.LP.lex()
            Eplace = self.expression()
            minimal.IC.generate_quad(":=", Eplace, "_", var)
        else:
            Parse("Expected := symbol for assignment", "Add appropriate opperator")
        return

    def if_stat(self):  # S -> if B then {P1} S1 {P2} TAIL{P3}
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            C = self.condition()  # S -> if B
            BTrue = C[0]
            BFalse = C[1]
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
                if self.lexeme.token == Lexeme.THENTK:  # S -> if B then {P1}
                    minimal.IC.backpatch(BTrue, minimal.IC.next_quad())
                    self.lexeme = minimal.LP.lex()
                    self.statements()  # S1
                    ifList = minimal.IC.make_list(minimal.IC.next_quad())
                    minimal.IC.generate_quad("jump", "_", "_", "_")
                    minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
                    self.elsepart()
                    minimal.IC.backpatch(ifList, minimal.IC.next_quad())
                else:
                    Parse("Expected keyword 'then' after if clause's condition")
            else:
                Parse("Expected right bracket ) to close if clause's condition")
        else:
            Parse("Expected left bracket ( to open if clause's condition")

    def elsepart(self):
        if self.lexeme.token == Lexeme.ELSETK:
            self.lexeme = minimal.LP.lex()
            self.statements()

    def while_stat(self):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            Bquad = minimal.IC.next_quad()  # Return to condition check
            self.lexeme = minimal.LP.lex()
            C = self.condition()
            BTrue = C[0]
            BFalse = C[1]
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
                minimal.IC.backpatch(BTrue, minimal.IC.next_quad())
                self.statements()
                minimal.IC.generate_quad("jump", "_", "_", Bquad)
                minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
            else:
                Parse("Expected right bracket ) to close while condition")
        else:
            Parse("Expected left bracket ( to open while condition")

    def doublewhile_stat(self):  # The state/flag was an interesting concept
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            state = minimal.IC.new_temp()
            minimal.ST.add_entity(Constant('0', 0))
            minimal.IC.generate_quad(":=", "0", "_", state)  # Initialize loop state
            condQuad = minimal.IC.next_quad()
            self.lexeme = minimal.LP.lex()
            C = self.condition()
            BTrue = C[0]
            BFalse = C[1]
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
                minimal.IC.backpatch(BTrue, minimal.IC.next_quad())
                state1_list = minimal.IC.make_list(minimal.IC.next_quad())
                minimal.IC.generate_quad("=", "2", state, "_")
                minimal.ST.add_entity(Constant('1', 1))
                minimal.IC.generate_quad(":=", "1", "_", state)
                self.statements()  # True statements
                minimal.IC.generate_quad("jump", "_", "_", condQuad)
                if self.lexeme.token == Lexeme.ELSETK:
                    self.lexeme = minimal.LP.lex()
                    minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
                    state2_list = minimal.IC.make_list(minimal.IC.next_quad())
                    minimal.IC.generate_quad("=", "1", state, "_")
                    minimal.ST.add_entity(Constant('2', 2))
                    minimal.IC.generate_quad(":=", "2", "_", state)
                    self.statements()
                    minimal.IC.generate_quad("jump", "_", "_", condQuad)
                    minimal.IC.backpatch(state1_list, minimal.IC.next_quad())
                    minimal.IC.backpatch(state2_list, minimal.IC.next_quad())
                else:
                    Parse("Expected keyword 'else' for doublewhile to have the proper syntax")
            else:
                Parse("Right bracket expected ) to end doublewhile condition")
        else:
            Parse("Expected left bracket ( to start doublewhile condition")

    def loop_stat(self):  # The program repeats the following statments until
        Bquad = minimal.IC.next_quad()
        self.statements()
        minimal.IC.generate_quad("jump", "_", "_", Bquad)

    def exit_stat(self):
        minimal.IC.generate_quad("halt", "_", "_", "_")

    def forcase_stat(self):
        first_quad = minimal.IC.next_quad()
        while self.lexeme.token == Lexeme.WHENTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
                self.lexeme = minimal.LP.lex()
                C = self.condition()
                BTrue = C[0]
                BFalse = C[1]
                if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                    self.lexeme = minimal.LP.lex()
                    if self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ":":
                        self.lexeme = minimal.LP.lex()

                        minimal.IC.backpatch(BTrue, minimal.IC.next_quad())
                        self.statements()
                        minimal.IC.generate_quad("jump", "_", "_", first_quad)
                        minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
                    else:
                        Parse("Expected ':' after condition symbol")
                else:
                    Parse("Expected closing bracket ) to close when case condition")
            else:
                Parse("Expected opening bracket ( for when case condition")
        if self.lexeme.token == Lexeme.DEFAULTTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ":":
                self.lexeme = minimal.LP.lex()
                self.statements()
            else:
                Parse("Expected : symbol")
        else:
            Parse("Expected keyword 'default' for the default case")

    def incase_stat(self):
        t = minimal.IC.new_temp()
        first_quad = minimal.IC.next_quad()
        minimal.IC.generate_quad(":=", "0", "_", t)

        while self.lexeme.token == Lexeme.WHENTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
                self.lexeme = minimal.LP.lex()
                C = self.condition()
                BTrue = C[0]
                BFalse = C[1]
                if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                    self.lexeme = minimal.LP.lex()
                    if self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ":":
                        self.lexeme = minimal.LP.lex()
                        minimal.IC.backpatch(BTrue, minimal.IC.next_quad())
                        self.statements()
                        minimal.IC.generate_quad(":=", "1", "_", t)
                        minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
                    else:
                        Parse("Expected ':' after condition symbol")
                else:
                    Parse("Expected closing bracket ) to close when case condition")
            else:
                Parse("Expected opening bracket ( for when case condition")
        minimal.IC.generate_quad("=", "1", t, first_quad)
        return

    def return_stat(self):
        if minimal.ST.scopes[-2].entities[-1].program_type == 2:
            print("Warning: Procedures should not have a return statement")
            print("Line " + str(minimal.line_index))
        minimal.IC.generate_quad("retv", "_", "_", self.expression())

    def call_stat(self):
        if self.lexeme.token == Lexeme.IDTK:
            procedure_name = self.lexeme.word
            self.lexeme = minimal.LP.lex()
            procedure = minimal.ST.find_entity(procedure_name)
            if procedure is None:
                Semantic(1, procedure_name)
            self.actualpars(procedure)

            minimal.IC.generate_quad("call", '_', "_", procedure_name)
            return
        if self.lexeme.word in Lexeme.key_words:
            Parse(self.lexeme.word + " is a key word, you can not use it as a function's name", "I lied")
        Parse("Expected name of procedure to call")

    def print_stat(self):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            minimal.IC.generate_quad("out", '_', "_", self.expression())
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Expected right bracket ) to close print statment")
        else:
            Parse("Expected left bracket ( to open print statement")

    def input_stat(self):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.IDTK:
                minimal.IC.generate_quad("in",  "_", "_", self.lexeme.word)
                self.lexeme = minimal.LP.lex()
                if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                    self.lexeme = minimal.LP.lex()
                else:
                    Parse("Expected closing bracket ) for input statement")
            else:
                Parse("Expected name of variable to save input")
        else:
            Parse("Expected opening bracket ( for input statement")

    statements_selector = {
        Lexeme.IDTK: assignment_stat,
        Lexeme.IFTK: if_stat,
        Lexeme.WHILETK: while_stat,
        Lexeme.DOUBLEWHILETK: doublewhile_stat,
        Lexeme.LOOPTK: loop_stat,
        Lexeme.EXITTK: exit_stat,
        Lexeme.FORCASETK: forcase_stat,
        Lexeme.INCASETK: incase_stat,
        Lexeme.RETURNTK: return_stat,
        Lexeme.CALLTK: call_stat,
        Lexeme.PRINTTK: print_stat,
        Lexeme.INPUTTK: input_stat
    }

    def statements(self):
        statements_counter = [0]
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "{":
            self.lexeme = minimal.LP.lex()
            self.statement(statements_counter)
            while self.lexeme.token == Lexeme.SEPARATORTK and self.lexeme.word == ";":
                self.lexeme = minimal.LP.lex()
                self.statement(statements_counter)
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "}":
                self.lexeme = minimal.LP.lex()
                return
            Parse("Right curly bracket } was expected to stop statements block",
                  "Maybe you missed a ';' operator between previous statements")
        self.statement(statements_counter)

    def statement(self, counter):
        if self.lexeme.token in self.statements_selector:
            counter[0] += 1
            statement_id = self.statements_selector.get(self.lexeme.token)
            if self.lexeme.token == Lexeme.IDTK:
                word = self.lexeme.word
                self.lexeme = minimal.LP.lex()
                statement_id(self, word)
            else:
                self.lexeme = minimal.LP.lex()
                statement_id(self)
        else:  # Handle possible Errors
            if counter[0] > 0:
                Parse("Expected a statement", "The block's last statement has no need of ';' separator")
            elif self.lexeme.word == '}':
                Parse("Expected a statement", "I am sorry, our services do not accept empty statement blocks")
            Parse("Expected '}' bracket")

    # ------------------------- Logical -------------------------
    def condition(self):  # B-> Q1{P1}(OR {P2}Q2 {P3})*
        Q1 = self.boolterm()
        BTrue = Q1[0]  # Q1.true
        BFalse = Q1[1]  # Q1.false
        while self.lexeme.token == Lexeme.ORTK:  # (or {P2}Q2 {P3})*
            minimal.IC.backpatch(BFalse, minimal.IC.next_quad())
            self.lexeme = minimal.LP.lex()
            Q2 = self.boolterm()
            BTrue = minimal.IC.merge_lists(BTrue, Q2[0])
            BFalse = Q2[1]
        return BTrue, BFalse

    def boolterm(self):  # Q->R1{P1}( AND {P2}R2 {P3})*
        R1 = self.boolfactor()
        QTrue = R1[0]  # R1.true
        QFalse = R1[1]  # R1.false
        while self.lexeme.token == Lexeme.ANDTK:  # (and {P2} R2{P3})*
            minimal.IC.backpatch(QTrue, minimal.IC.next_quad())  # If condition is true, go to the immediate next quad
            self.lexeme = minimal.LP.lex()
            R2 = self.boolfactor()
            QFalse = minimal.IC.merge_lists(QFalse, R2[1])
            QTrue = R2[0]
        return QTrue, QFalse

    def boolfactor(self):
        RTrue = minimal.IC.empty_list()
        RFalse = minimal.IC.empty_list()
        if self.lexeme.token == Lexeme.NOTTK:
            self.lexeme = minimal.LP.lex()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.token == "[":
                self.lexeme = minimal.LP.lex()
                B = self.condition()  # R ->( B )
                # {P1}:
                RTrue = B[1]
                RFalse = B[0]
                if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "]":
                    self.lexeme = minimal.LP.lex()
                else:
                    Parse("Expected ]")
            else:
                Parse("Expected [")
        elif self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "[":
            self.lexeme = minimal.LP.lex()
            B = self.condition()  # R ->( B )
            # {P1}:
            RTrue = B[0]
            RFalse = B[1]
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "]":
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Expected ]")
        else:  # R ->E1 relop E2{P1}
            E1 = self.expression()  # x
            relop = self.relational_oper()  # <>=
            E2 = self.expression()  # y

            RTrue = minimal.IC.make_list(minimal.IC.next_quad())
            minimal.IC.generate_quad(relop, E1, E2, "_")

            RFalse = minimal.IC.make_list(minimal.IC.next_quad())
            minimal.IC.generate_quad("jump", "_", "_", "_")
        return RTrue, RFalse

    def expression(self):
        sign = self.optional_sign()
        T1place = sign + self.term()
        while self.lexeme.token == Lexeme.ADDTK:  # (+T2{P1})*
            oper = self.add_oper()
            T2place = self.term()
            # {P1}
            w = minimal.IC.new_temp()
            minimal.IC.generate_quad(oper, T1place, T2place, w)
            T1place = w
        return T1place

    def term(self):
        F1place = self.factor()  # F1
        while self.lexeme.token == Lexeme.MULTIPLYTK:
            oper = self.mul_oper()
            F2place = self.factor()  # F2
            w = minimal.IC.new_temp()
            minimal.IC.generate_quad(oper, F1place, F2place, w)
            F1place = w
        return F1place

    def factor(self):
        Fplace = ""
        if self.lexeme.token == Lexeme.CONSTANTTK:
            constant = Constant(self.lexeme.word, int(self.lexeme.word))
            minimal.ST.add_entity(constant)
            Fplace = self.lexeme.word
            self.lexeme = minimal.LP.lex()

        elif self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            self.lexeme = minimal.LP.lex()
            Fplace = self.expression()
            if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == ")":
                self.lexeme = minimal.LP.lex()
            else:
                Parse("Right bracket ')' expected")

        elif self.lexeme.token == Lexeme.IDTK:
            idt = self.lexeme.word
            self.lexeme = minimal.LP.lex()
            Fplace = self.idtail(idt)
        else:
            Parse("This factor's syntax is not supported")

        return Fplace

    def idtail(self, id_name):
        if self.lexeme.token == Lexeme.BRACKETTK and self.lexeme.word == "(":
            function = minimal.ST.find_entity(id_name)
            if function is None:
                Semantic(1, id_name)
            self.actualpars(function)
            w = minimal.IC.new_temp()
            minimal.IC.generate_quad("par", w, "RET", "_")
            minimal.IC.generate_quad("call", '_', '_', function.name)
            return w
        minimal.ST.find_entity(id_name)
        return id_name

    def relational_oper(self):
        relop = ""
        if self.lexeme.token == Lexeme.COMPARATORTK:
            relop = self.lexeme.word
            self.lexeme = minimal.LP.lex()
        else:
            Parse("Expected Relational Operator")
        return relop

    def add_oper(self):
        oper = ""
        if self.lexeme.token == Lexeme.ADDTK:
            oper = self.lexeme.word
            self.lexeme = minimal.LP.lex()
        return oper

    def mul_oper(self):
        oper = ""
        if self.lexeme.token == Lexeme.MULTIPLYTK:
            oper = self.lexeme.word
            self.lexeme = minimal.LP.lex()
        return oper

    def optional_sign(self):
        sign = ""
        if self.lexeme.token == Lexeme.ADDTK:
            sign = self.add_oper()
        return sign


class ICGenerator:
    def __init__(self):
        self.temp_index = 1
        self.quad_index = 1
        self.quadsList = []

    def __str__(self):
        quads = ''
        for quad in self.quadsList:
            quads += str(quad) + '\n'
        return quads

    def next_quad(self):
        return self.quad_index

    def generate_quad(self, op, x, y, z):
        tag = str(self.quad_index) + ':'
        self.quad_index += 1
        quad = [tag, op, x, y, z]
        self.quadsList.append(quad)

    def new_temp(self):
        temp = self.temp_index
        self.temp_index += 1
        temp = "T_" + str(temp)
        minimal.ST.add_entity(Temp(temp))
        return temp

    @staticmethod
    def empty_list():
        return ['']

    @staticmethod
    def make_list(x):
        return [x]

    @staticmethod
    def merge_lists(l1, l2):
        return l1 + l2

    def backpatch(self, patchlist, label):
        for tag in patchlist:
            for quad in self.quadsList:
                if quad[0].split(":")[0] == str(tag):
                    quad[4] = label


class Semantic(Error):
    errors = {
        1: "entity not found",
        2: "Passing wrong argument type",
        3: "entity already exists in the same scope",
        4: "'s type does not match function's parameter type",
        5: "Number of passed parameters is not the same as the declared parameters",
        6: "A subprogram can not have the same name as the main program"
    }

    def __init__(self, error_cause, requested_entity=''):
        super().__init__('SemanticError', requested_entity + " " + self.errors.get(error_cause))


class SymbolTable:
    def __init__(self):
        self.scopes = deque()

    def __str__(self):
        table = ''
        for scope in self.scopes:
            table += str(scope)
        return table

    def add_scope(self):
        new_scope = Scope(len(self.scopes))
        self.scopes.append(new_scope)

    def delete_scope(self):
        if self.scopes[-1].nesting_level == 0:
            minimal.main_framelength = self.scopes[-1].offset
        else:
            framelength = self.scopes[-1].offset
            self.scopes[-2].entities[-1].framelength = framelength
        scope = self.scopes[-1]
        minimal.FC.write_block(scope)
        self.scopes.pop()

    def add_entity(self, new_entity):
        scope = self.scopes[-1]
        if new_entity.entity_type != 'Constant' and scope.islocal(new_entity.name):
            Semantic(3, new_entity.name)
        elif new_entity.entity_type in ['Variable', 'Parameter', 'Temp']:
            new_entity.offset = scope.offset
            scope.offset += 4
        scope.entities.append(new_entity)

    def add_argument(self, parmode):
        subprogram = self.scopes[-2].entities[-1]
        subprogram.arguments.append(Argument(parmode))

    def find_entity(self, name):
        for scope in reversed(self.scopes):
            for entity in scope.entities:
                if entity.name == name:
                    return entity
        return None

    def get_level(self, entity):
        for scope in reversed(self.scopes):
            if entity in scope.entities:
                return scope.nesting_level


class Entity:
    name = ''
    entity_type = ''

    def __init__(self, name, entity_type):
        self.name = name
        self.entity_type = entity_type

    def __str__(self):
        return self.name


class Variable(Entity):
    offset = 12

    def __init__(self, name):
        Entity.__init__(self, name, 'Variable')

    def __str__(self):
        return "- Variable: name = " + self.name + ", offset = " + str(self.offset)


class Subprogram(Entity):
    def __init__(self, name, program_type):
        Entity.__init__(self, name, 'Subprogram')
        self.startQuad = 0
        self.arguments = []
        self.framelength = 12
        self.program_type = program_type

    def __str__(self):
        msg = "- Subprogram: name = " + self.name + ", type = " + str(self.program_type)
        msg += ", startQuad = " + str(self.startQuad)
        msg += ", number of arguments = " + str(len(self.arguments))
        msg += ", List of arguments: ["
        for arg in self.arguments:
            msg += str(arg) + ', '
        msg = msg[:-2]
        msg += "]"
        msg += ", framelength = " + str(self.framelength)
        return msg


class Constant(Entity):
    value = -1

    def __init__(self, name, value):
        Entity.__init__(self, name, 'Constant')
        self.value = value

    def __str__(self):
        return "- Constant = " + str(self.value)


class Parameter(Entity):
    parMode = 0
    offset = 12

    def __init__(self, name, parMode):
        Entity.__init__(self, name, 'Parameter')
        self.parMode = parMode

    def __str__(self):
        if self.parMode == 1:
            par_type = 'CV'
        else:
            par_type = 'REF'
        return "- Parameter: name = " + self.name + ", type = " + str(par_type) + ", offset = " + str(self.offset)


class Temp(Entity):
    offset = 0

    def __init__(self, name):
        Entity.__init__(self, name, 'Temp')

    def __str__(self):
        return "- Temp: name = " + self.name + ", offset = " + str(self.offset)


class Scope:
    entities = []
    nesting_level = 0
    offset = 12

    def __init__(self, nesting_level):
        self.entities = []
        self.nesting_level = nesting_level

    def __str__(self):
        scope = '\nLevel ' + str(self.nesting_level) + ':\n'
        for entity in self.entities:
            scope += 'Entity' + str(entity) + '\n'
        return scope

    def islocal(self, name):
        for entity in self.entities:
            if entity.name == name:
                return True
        return False


class Argument:
    parMode = 0

    def __init__(self, par_mode):
        self.parMode = par_mode

    def __str__(self):
        if self.parMode == 1:
            return 'CV'
        elif self.parMode == 2:
            return 'REF'
        return "Unknown"


class Finalizer:
    pari = 0

    def __init__(self):
        self.file = open("MIPS" + ".asm", "w")
        self.file.write(".text\n.globl Lmain")
        self.file.write("\nL0: j Lmain")

        self.label = 1
        self.start_quad = 0
        self.scope = None

    #   -------- Helpful Functions --------
    def gnlvcode(self, entity):
        level = minimal.ST.get_level(entity)
        dist = self.scope.nesting_level - level
        line = 'lw $t0,-4($sp)\n'
        for i in range(dist - 1):
            line += 'lw $t0,-4($t0)\n'
        line += 'addi $t0,$t0,-' + str(entity.offset)
        return line

    def loadvr(self, v, r):
        entity = minimal.ST.find_entity(v)
        level = minimal.ST.get_level(entity)
        if entity is None:
            Semantic(1, v)
        elif entity.entity_type == 'Constant':
            return 'li ' + r + ',' + str(entity.value)
        elif level == 0:
            return 'lw ' + r + ',-' + str(entity.offset) + '($s0)'
        elif entity in self.scope.entities:
            if entity.entity_type == 'Parameter' and entity.parMode == 2:  # Passed by reference
                line = 'lw $t0,-' + str(entity.offset) + '($sp)' + '\n'
                line += 'lw ' + r + ',($t0)'
                return line
            return 'lw ' + r + ',-' + str(entity.offset) + '($sp)'
        line = self.gnlvcode(entity) + '\n'
        if entity.entity_type == 'Parameter' and entity.parMode == 2:
            line += 'lw $t0,($t0)' + '\n'
        line += 'lw ' + r + ',($t0)'
        return line

    def storerv(self, r, v):
        entity = minimal.ST.find_entity(v)
        level = minimal.ST.get_level(entity)
        if entity is None:
            Semantic(1, v)
        elif level == 0:
            return 'sw '+r+',-'+str(entity.offset)+'($s0)'
        elif entity in self.scope.entities:
            if entity.entity_type == 'Parameter' and entity.parMode == 2:
                line = 'lw $t0,-' + str(entity.offset) + '($sp)\n'
                line += 'sw '+r+',($t0)'
                return line
            return 'sw '+r+',-'+str(entity.offset)+'($sp)'
        line = self.gnlvcode(entity)+'\n'
        if entity.entity_type == 'Parameter' and entity.parMode == 2:
            line += 'lw $t0,($t0)'+'\n'
        line += 'sw '+r+',($t0)'
        return line

    def getfunc(self):
        # Return first call quad after the current parameter
        for quad in minimal.IC.quadsList[self.label:]:
            if quad[1] == 'call':
                return minimal.ST.find_entity(quad[4])

    #   ------------ Commands ------------
    relops = {
        '=': 'beq',
        '<': 'blt',
        '>': 'bgt',
        '<=': 'ble',
        '>=': 'bge',
        '<>': 'bne',
    }

    math = {
        '+': 'add',
        '-': 'sub',
        '*': 'mul',
        '/': 'div',
    }

    def par(self, quad, line):
        function = self.getfunc()  # Get the function to be called next
        param = minimal.ST.find_entity(quad[2])
        if self.pari == 0:
            line += 'addi $fp,$sp,'+str(function.framelength)+'\n'

        if quad[3] == 'CV':
            line += self.loadvr(quad[2], '$t0') + '\n'
            line += 'sw $t0,-' + str(12 + 4 * self.pari) + '($fp)'
        elif quad[3] == 'REF':
            if param in self.scope.entities:
                if param.entity_type == 'Parameter' and param.parMode == 2:
                    line += 'lw $t0,-' + str(param.offset) + '($sp)\n'
                    line += 'sw $t0,-' + str(12 + 4 * self.pari) + '($fp)'
                else:
                    line += 'addi $t0,$sp,-' + str(param.offset) + '\n'
                    line += 'sw $t0,-' + str(12 + 4 * self.pari) + '($fp)'
            elif param.entity_type == 'Parameter' and param.parMode == 2:
                line += self.gnlvcode(param) + '\n'
                line += 'lw $t0,($t0)' + '\n'
                line += 'sw $t0, -' + str(12 + 4 * self.pari) + '($fp)'
            else:
                line += self.gnlvcode(param)+'\n'
                line += 'sw $t0,-' + str(12 + 4 * self.pari) + '($fp)'
        elif quad[3] == 'RET':
            line += 'addi $t0,$sp,-' + str(param.offset) + '\n'
            line += 'sw $t0,-8($fp)'
        self.pari += 1
        return line

    def begin_block(self, quad, line):
        if quad[2] == minimal.program_name:
            main = '\nLmain:'
            line = main + line
            line += 'addi $sp,$sp,' + str(minimal.main_framelength)
            line += '\nmove $s0,$sp'
            return line
        line += 'sw $ra,-0($sp)'
        return line

    def jump(self, quad, line):
        line += 'b L' + str(quad[4])
        return line

    def relop(self, quad, line):
        line += self.loadvr(quad[2], '$t1') + '\n'
        line += self.loadvr(quad[3], '$t2') + '\n'
        line += self.relops.get(quad[1]) + ' $t1,' + '$t2,' + 'L' + str(quad[4])
        return line

    def assign(self, quad, line):
        line += self.loadvr(quad[2], '$t1') + '\n'
        line += self.storerv('$t1', quad[4])
        return line

    def mathop(self, quad, line):
        line += self.loadvr(quad[2], '$t1') + '\n'
        line += self.loadvr(quad[3], '$t2') + '\n'
        line += self.math.get(quad[1]) + " $t1,$t1,$t2" + '\n'
        line += self.storerv('$t1', quad[4])
        return line

    def sysout(self, quad, line):
        line += self.loadvr(quad[4], '$t1') + '\n'
        line += 'li $v0,1\n'
        line += 'move $a0, $t1\n'
        line += 'syscall'
        return line

    def sysin(self, quad, line):
        line += 'li $v0,5\n'
        line += 'syscall\n'
        line += self.storerv('$v0', quad[4])
        return line

    def retv(self, quad, line):
        line += self.loadvr(quad[4], '$t1') + '\n'
        line += 'lw $t0,-8($sp)\n'
        line += 'sw $t1,($t0)'
        return line

    def call(self, quad, line):
        function = minimal.ST.find_entity(quad[4])
        func_scope = minimal.ST.get_level(function)
        if self.pari == 0:
            line += 'addi $fp,$sp,' + str(function.framelength) + '\n'
        if function in self.scope.entities:
            line += 'sw $sp,-4($fp)\n'
        else:
            line += 'lw $t0,-4($sp)\n'
            line += 'sw $t0,-4($fp)\n'
        line += 'addi $sp,$sp,' + str(function.framelength) + '\n'
        line += 'jal L' + str(function.startQuad) + '\n'
        line += 'addi $sp,$sp,-' + str(function.framelength)
        self.pari = 0
        return line

    def halt(self, quad, line):
        line += 'li $v0,10\n'
        line += 'syscall'
        return line

    def end_block(self, quad, line):
        if self.scope.nesting_level != 0:
            line += 'lw $ra,-0($sp)\n'
            line += 'jr $ra'
        return line

    commands = {
        'begin_block': begin_block,
        'halt': halt,
        'end_block': end_block,
        'jump': jump,
        'call': call,
        'par': par,
        '=': relop,
        '<': relop,
        '>': relop,
        '<=': relop,
        '>=': relop,
        '<>': relop,
        ':=': assign,
        '+': mathop,
        '-': mathop,
        '*': mathop,
        '/': mathop,
        'out': sysout,
        'in': sysin,
        'retv': retv
    }

    #   ---------- Write Functins ----------
    def write_quad(self, quad):
        print(quad)
        command = self.commands.get(quad[1])
        line = '\nL' + str(quad[0]) + " "
        line = command(self, quad, line)
        self.file.write(line)
        self.label += 1

    def write_block(self, scope):
        self.scope = scope
        for quad in minimal.IC.quadsList[self.start_quad:]:
            self.write_quad(quad)
        self.start_quad = self.label - 1


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'Script.min'
    minimal = Compiler()
    minimal.SP.program()

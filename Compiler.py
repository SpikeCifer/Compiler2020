# ---------------------------------------------------|CONTRIBUTERS|-----------------------------------------------------
# 2971: ΣΤΥΛΙΑΝΟΣ ΖΑΠΠΙΔΗΣ
# 3059: ΖΗΣΙΜΟΣ ΠΑΡΑΣΧΗΣ
# ----------------------------------------------------|TODO_Notes|------------------------------------------------------
#
#
# -------------------------------------------------|Other Libraries|----------------------------------------------------
from termcolor import colored
# -----------------------------------------------------|GLOBALS|--------------------------------------------------------
source = ""
start_index = 0
lexeme = [-1, ""]  # The lexeme that gets returned from lexer

line_index = 1              # Will be used for errors
char_index_of_line = 0      # Will be used for errors
# ------------------------ DEFINE STATES PART ------------------------
state0 = 0    # This is the starting state
state1 = 1    # Lex is reading IDs
state2 = 2    # Lex is reading constants
state3 = 3    # Lex read * symbol
state4 = 4    # Lex read / symbol

# These states have to do with comments
state5 = 5    # Long Comment state
state6 = 6    # Lex read * while in long comment state
state7 = 7    # Lex read / while in long comment state
state8 = 8    # Short Comment State
state9 = 9    # Lex read / while in short comment state
state10 = 10  # Lex has read * symbol while in short comment

# These states have to do with double char ops
state11 = 11  # Lex has read < symbol
state12 = 12  # Lex has read > symbol
state13 = 13  # Lex has read : symbol

specials1 = {state3, state4}       # The states where depending on the next char return or not
specials2 = {state10, state11}     # The states where depending on the next char they add it to the word
comments = {state5, state6, state7, state8, state9, state10}
# ---------------------------- DEFINE GENERAL TOKENS PART ----------------------------
EOFTK = 14
IDTK = 15
CONSTANTTK = 16
ADDTK = 17
MULTIPLYTK = 18
BRACKETTK = 19
SEPARATORTK = 20
COMPARATORTK = 21
DECLARATORTK = 22

stateR = {EOFTK, IDTK, CONSTANTTK, ADDTK,
          MULTIPLYTK, BRACKETTK, SEPARATORTK, COMPARATORTK, DECLARATORTK}

singles = {ADDTK, BRACKETTK, SEPARATORTK}
longs = {state1, state2}

# ---------------------------------|DEFINE KEYWORDS PART|---------------------------------
# All of them were originally IDTKs, we now come to specify them
PROGRAMTK = 23
DECLARETK = 24
IFTK = 25
ELSETK = 26
WHILETK = 27
DOUBLEWHILETK = 28
LOOPTK = 29
EXITTK = 30
FORCASETK = 31
INCASETK = 32
WHENTK = 33
DEFAULTTK = 34
NOTTK = 35
ANDTK = 36
ORTK = 37
FUNCTIONTK = 38
PROCEDURETK = 39
CALLTK = 40
RETURNTK = 41
INTK = 42
INOUTTK = 43
INPUTTK = 44
PRINTTK = 45
THENTK = 46

taken_words = ["program", "declare", "if", "else", "while", "doublewhile", "loop", "exit", "forcase", "incase",
               "when", "default", "not", "and", "or", "function", "procedure", "call", "return", "in",
               "inout", "input", "print","then"]
double_ops = ["<>", ">=", "<=", ":="]
# ----------------------- LEX ERRORS -----------------------
Error1 = 47  # Char after Digit
Error2 = 48  # Closed long comment without opening one
Error3 = 49  # Opened second comment inside another one
Error4 = 50  # EOF while in long comment
Error5 = 51  # Invalid symbol
stateE = {Error1, Error2, Error3, Error4, Error5}
# ----------------------- LEX PART -----------------------

states = [
    # state0
    [state1, state2, ADDTK, state3, state4, state11, state12,
     COMPARATORTK, state13, SEPARATORTK, SEPARATORTK, BRACKETTK, BRACKETTK, BRACKETTK,
     BRACKETTK, BRACKETTK, BRACKETTK, state0, state0, EOFTK, Error5],
    # state1
    [state1, state1, IDTK, IDTK, IDTK, IDTK, IDTK,
     IDTK, IDTK, IDTK, IDTK, IDTK, IDTK, IDTK,
     IDTK, IDTK, IDTK, IDTK, IDTK, IDTK, IDTK],
    # state2
    [Error1, state2, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK,
     CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK,
     CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK, CONSTANTTK],
    # state3
    [MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, Error2, MULTIPLYTK, MULTIPLYTK,
     MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,  MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,
     MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,  MULTIPLYTK, MULTIPLYTK, MULTIPLYTK],
    # state4
    [MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, state5, state8, MULTIPLYTK, MULTIPLYTK,
     MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,  MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,
     MULTIPLYTK, MULTIPLYTK, MULTIPLYTK, MULTIPLYTK,  MULTIPLYTK, MULTIPLYTK, MULTIPLYTK],
    # state5
    [state5, state5, state5, state6, state7, state5, state5,
     state5, state5, state5, state5, state5, state5, state5,
     state5, state5, state5, state5, state5, Error4, state5],
    # state6
    [state5, state5, state5, state5, state0, state5, state5,
     state5, state5, state5, state5, state5, state5, state5,
     state5, state5, state5, state5, state5, Error4, state5],
    # state7
    [state5, state5, state5, Error3, Error3, state5, state5,
     state5, state5, state5, state5, state5, state5, state5,
     state5, state5, state5, state5, state5, Error4, state5],
    # state8
    [state8, state8, state8, state10, state9, state8, state8,
     state8, state8, state8, state8, state8, state8, state8,
     state8, state8, state8, state0, state8, EOFTK, state8],
    # state9
    [state8, state8, state8, Error3, Error3, state8, state8,
     state8, state8, state8, state8, state8, state8, state8,
     state8, state8, state8, state0, state8, EOFTK, state8],
    # state10
    [state8, state8, state8, state8, Error2, state8, state8,
     state8, state8, state8, state8, state8, state8, state8,
     state8, state8, state8, state0, state8, EOFTK, state8],
    # state11
    [COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK,
     COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK,
     COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK],
    # state12
    [COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK,
     COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK,
     COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK, COMPARATORTK],
    # state13
    [SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK,
     DECLARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK,
     SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK, SEPARATORTK],
]


def lex_error(error_type, c):
    print(colored("Warning!", "red"))
    print(colored("Lex Error", "blue"),
          colored("\nLine:", "yellow"), line_index,
          colored("Character:", "green"), char_index_of_line)
    error_message = "Error_Type " + str(error_type)
    if error_type == Error1:
        error_message += ": Digits can not be followed by characters"
    elif error_type == Error2:
        error_message += ": Closed long comment without opening one"
    elif error_type == Error3:
        error_message += ": Opened second comment inside another one"
    elif error_type == Error4:
        error_message += ": EOF while in long comment"
    elif error_type == Error5:
        error_message += ": Invalid symbol " + "'"+c+"'"
    else:
        error_message += "404: Undefined Error"
    print(colored(error_message, "grey"))
    exit()


def syntax_error(s):
    print(colored("Warning!", "red"))
    print(colored("Syntax Error","blue"))
    print(colored("In line", "yellow"), str(line_index))
    print(colored(s, "grey", "on_red"))
    exit()


def eof(current_char):
    total = start_index + current_char
    if total > len(source)-1:
        return True
    return False


def find_symbol(symbol):
    if symbol in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return 0

    elif symbol in "0123456789":
        return 1

    elif symbol in "+-*/":
        if symbol in "+-":
            return 2
        elif symbol == "*":
            return 3
        else:
            return 4

    elif symbol in "<>=":
        if symbol == "<":
            return 5
        elif symbol == ">":
            return 6
        else:
            return 7

    elif symbol in ":;,":
        if symbol == ":":
            return 8
        elif symbol == ";":
            return 9
        else:
            return 10

    elif symbol in "()[]{}":
        if symbol == "(":
            return 11
        elif symbol == ")":
            return 12
        elif symbol == "[":
            return 13
        elif symbol == "]":
            return 14
        elif symbol == "{":
            return 15
        else:
            return 16

    elif symbol in "\n \t":
        if symbol == "\n":
            return 17
        else:
            return 18

    else:
        return 20


def update_state(state, char):
    column = find_symbol(char)
    state = states[state][column]
    return state


def identify(tk, word):
    for i in range(0, len(taken_words)):
        if word == taken_words[i]:
            tk = i + 23
    return tk


def handle_return(tk, word, temp, symbol, index):
    global start_index
    if tk == IDTK:
        tk = identify(tk, word)
        start_index += index - 1
        return tk, word

    elif tk == CONSTANTTK:
        number = int(word)
        if number > 32767 or number < -32767:
            print("Warning number " + word + " is out of bounds")
        start_index += index - 1
        return tk, word

    elif tk in singles:
        if temp == ":":
            start_index += index - 1
            return tk, temp
        else:
            start_index += index
        return tk, symbol

    elif tk == MULTIPLYTK:
        start_index += index - 1
        return tk, temp

    elif tk == COMPARATORTK:
        opp = temp + symbol
        if opp in double_ops:
            start_index += index
            return tk, opp
        elif symbol == "=":
            start_index += index
            return tk, symbol
        else:
            start_index += index - 1
            return tk, temp

    elif tk == DECLARATORTK:
        start_index += index
        return tk, ":="

    elif tk == EOFTK:
        start_index += index
        return tk, ""


def lex():
    global char_index_of_line, line_index
    current_char = 0
    state = state0
    word = ""  # Word must be a buffer[30]
    temp = ""
    symbol = ""
    while state not in stateR and state not in stateE:
        if eof(current_char):
            state = states[state][19]  # All of them are in stateR so it exits immediately
            current_char += 1
        else:
            symbol = source[start_index + current_char]
            if (state == state0 or state in comments) and symbol == "\n":
                line_index += 1
                char_index_of_line = 0
            state = update_state(state, symbol)
            if state in longs:  # State1 or State2 create IDs or Constants
                if len(word) <= 30:
                    word += symbol
            elif state == state3 or state == state4:
                temp = symbol
            elif state == state5 or state == state8:
                temp = ""
            elif state == state11 or state == state12 or state == state13:
                temp = symbol
            # Any other state does not affect the word
            char_index_of_line += 1
            current_char += 1

    # start_index += current_char
    if state in stateE:
        lex_error(state, symbol)
    else:
        tk = state
        return handle_return(tk, word, temp, symbol, current_char)

# ----------------------------------------------------|SYNTAX PART|-----------------------------------------------------


def program():  # The starting grammar rule
    global lexeme
    lexeme = lex()
    if lexeme[0] == PROGRAMTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
            if lexeme[0] == BRACKETTK and lexeme[1] == "{":
                lexeme = lex()
                block()
                if lexeme[0] == BRACKETTK and lexeme[1] == "}":
                    print(colored("Syntax Check completed successfully!","green"))
                else:
                    syntax_error("Expected right curly bracket }")
            else:
                syntax_error("Expected left curly bracket {")
        else:
            syntax_error("The name of the program was expected")
    else:
        syntax_error("To start a program the keyword 'program' is expected")


def block():
    declarations()
    subprograms()
    statements()
    return


def declarations():
    global lexeme
    while lexeme[0] == DECLARETK:
        lexeme = lex()
        varlist()
        if lexeme[0] == SEPARATORTK and lexeme[1] == ";":
            lexeme = lex()
        else:
            syntax_error("Expected separator ;")
    return


def varlist():
    global lexeme
    if lexeme[0] == IDTK:
        lexeme = lex()
        while lexeme[0] == SEPARATORTK and lexeme[1] == ",":
            lexeme = lex()
            if lexeme[0] == IDTK:
                lexeme = lex()
            else:
                syntax_error("Expected variable name")


def subprograms():
    global lexeme
    while lexeme[0] == FUNCTIONTK or lexeme[0] == PROCEDURETK:
        subprogram()


def subprogram():
    global lexeme
    if lexeme[0] == FUNCTIONTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
            funcbody()
        else:
            syntax_error("The name of the function was expected")

    elif lexeme[0] == PROCEDURETK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
            funcbody()
        else:
            syntax_error("The name of the procedure was expected")


def funcbody():
    global lexeme
    formalpars()
    if lexeme[0] == BRACKETTK and lexeme[1] == "{":
        lexeme = lex()
        block()
        if lexeme[0] == BRACKETTK and lexeme[1] == "}":
            lexeme = lex()
        else:
            syntax_error("Expected } bracket")
    else:
        syntax_error("Expected { bracket")


def formalpars():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        formalparlist()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error("Right bracket expected")
    else:
        syntax_error("Expected left bracket")


def formalparlist():
    global lexeme
    if lexeme[0] == INTK or lexeme[0] == INOUTTK:
        formalparitem()
    while lexeme[0] == SEPARATORTK and lexeme[1] == ",":
        lexeme = lex()
        formalparitem()


def formalparitem():
    global lexeme
    if lexeme[0] == INTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
        else:
            syntax_error("Expected parameter name after in keyword")

    elif lexeme[0] == INOUTTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
        else:
            syntax_error("Expected parameter name after inout keyword")


def statements():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "{":
        lexeme = lex()
        statement()
        while lexeme[0] == SEPARATORTK and lexeme[1] == ";":
            lexeme = lex()
            statement()
        if lexeme[0] == BRACKETTK and lexeme[1] == "}":
            lexeme = lex()
        else:
            syntax_error("Right } bracket expected")
    else:
        statement()


def statement():
    assignment_stat()
    if_stat()
    while_stat()
    doublewhile_stat()
    loop_stat()
    exit_stat()
    forcase_stat()
    call_stat()
    return_stat()
    input_stat()
    print_stat()


def assignment_stat():
    global lexeme
    if lexeme[0] == IDTK:
        lexeme = lex()
        if lexeme[0] == DECLARATORTK:
            lexeme = lex()
            expression()
        else:
            syntax_error("Expected := symbol for assignment")


def if_stat():
    global lexeme
    if lexeme[0] == IFTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            condition()
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
                if lexeme[0] == THENTK:
                    lexeme = lex()
                    statements()
                    elsepart()
                else:
                    syntax_error("Expected keyword then")
            else:
                syntax_error("Expected closing bracket )")
        else:
            syntax_error("Expected opening bracket (")


def elsepart():
    global lexeme
    if lexeme[0] == ELSETK:
        lexeme = lex()
        statements()


def while_stat():
    global lexeme
    if lexeme[0] == WHILETK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            condition()
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
                statements()
            else:
                syntax_error("Right bracket expected")
        else:
            syntax_error("Expected left bracket")


def doublewhile_stat():
    global lexeme
    if lexeme[0] == DOUBLEWHILETK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            condition()
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
                statements()
                if lexeme[0] == ELSETK:
                    lexeme = lex()
                    statements()
                else:
                    syntax_error("Expected keyword else")
            else:
                syntax_error("Right bracket expected")
        else:
            syntax_error("Expected left bracket")


def loop_stat():
    global lexeme
    if lexeme[0] == LOOPTK:
        lexeme = lex()
        statements()


def exit_stat():
    global lexeme
    if lexeme[0] == EXITTK:
        lexeme = lex()


def forcase_stat():
    global lexeme
    if lexeme[0] == FORCASETK:
        lexeme = lex()
        while lexeme[0] == WHENTK:
            lexeme = lex()
            if lexeme[0] == BRACKETTK and lexeme[1] == "(":
                lexeme = lex()
                condition()
                if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                    lexeme = lex()
                    if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
                        lexeme = lex()
                        statements()
                    else:
                        syntax_error("Expected : separator")
                else:
                    syntax_error("Expected closing bracket )")
            else:
                syntax_error("Expected opening bracket (")

        if lexeme[0] == DEFAULTTK:
            lexeme = lex()
            if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
                lexeme = lex()
                statements()
            else:
                syntax_error("Expected : symbol")
        else:
            syntax_error("Expected keyword default")


def incase_stat():
    global lexeme
    if lexeme[0] == INCASETK:
        lexeme = lex()
        while lexeme[0] == WHENTK:
            lexeme = lex()
            if lexeme[0] == BRACKETTK and lexeme[1] == "(":
                lexeme = lex()
                condition()
                if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                    lexeme = lex()
                    if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
                        lexeme = lex()
                        statements()
                    else:
                        syntax_error("Expected : separator")
                else:
                    syntax_error("Expected closing bracket )")
            else:
                syntax_error("Expected opening bracket (")


def return_stat():
    global lexeme
    if lexeme[0] == RETURNTK:
        lexeme = lex()
        expression()


def call_stat():
    global lexeme
    if lexeme[0] == CALLTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
            actualpars()
        else:
            syntax_error("Expected variable name")


def print_stat():
    global lexeme
    if lexeme[0] == PRINTTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            expression()
            if lexeme == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
            else:
                syntax_error("Expected closing bracket )")
        else:
            syntax_error("Expected opening bracket (")


def input_stat():
    global lexeme
    if lexeme[0] == INPUTTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            if lexeme[0] == IDTK:
                lexeme = lex()
                if lexeme == BRACKETTK and lexeme[1] == ")":
                    lexeme = lex()
                else:
                    syntax_error("Expected closing bracket )")
            else:
                syntax_error("Expected variable name")
        else:
            syntax_error("Expected opening bracket (")


def actualpars():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        actualparlist()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error ("Right bracket expected")
    else:
        syntax_error("Expected opening bracket (")


def actualparlist():
    global lexeme
    while lexeme[0] == INTK or lexeme[0] == INOUTTK:
        lexeme = lex()
        actualparitem()
        if lexeme[0] == SEPARATORTK and lexeme[1] == ",":
            lexeme = lex()
        else:
            syntax_error("Expected ,")


def actualparitem():
    global lexeme
    if lexeme[0] == INTK:
        lexeme = lex()
        expression()
    elif lexeme[0] == INOUTTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
        else:
            syntax_error("Variable name was expected")


def condition():
    global lexeme
    boolterm()
    while lexeme[0] == ORTK:
        lexeme = lex()
        boolterm()


def boolterm():
    global lexeme
    boolfactor()
    while lexeme[0] == ANDTK:
        lexeme = lex()
        boolfactor()


def boolfactor():
    global lexeme

    if lexeme[0] == NOTTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "[":
            lexeme = lex()
            condition()
            if lexeme[0] == BRACKETTK and lexeme[1] == "]":
                lexeme = lex()
            else:
                syntax_error("Expected ]")
        else:
            syntax_error("Expected [")

    elif lexeme[0] == BRACKETTK and lexeme[1] == "[":
        lexeme = lex()
        condition()
        if lexeme[0] == BRACKETTK and lexeme[1] == "]":
            lexeme = lex()
        else:
            syntax_error("Expected ]")
    else:
        expression()
        relational_oper()
        expression()


def expression():
    global lexeme
    optionalsign()
    term()
    while lexeme[0] == ADDTK:
        add_oper()
        term()


def term():
    global lexeme
    factor()
    while lexeme[0] == MULTIPLYTK:
        mul_oper()
        factor()


def factor():
    global lexeme
    if lexeme[0] == CONSTANTTK:
        lexeme = lex()
    elif lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        condition()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error("Right bracket expected")
    else:
        if lexeme[0] == IDTK:
            lexeme = lex()
            idtail()


def idtail():
    actualpars()


def relational_oper():
    global lexeme
    if lexeme[0] == COMPARATORTK:
        lexeme = lex()
    else:
        syntax_error("Expected Relational Operator")


def add_oper():
    global lexeme
    if lexeme[0] == ADDTK:
        lexeme = lex()


def mul_oper():
    global lexeme
    if lexeme[0] == MULTIPLYTK:
        lexeme = lex()


def optionalsign():
    add_oper()

# -----------------------------------------------------|MAIN PART|------------------------------------------------------


def load_source(filename):
    global source
    file = filename.split(".")
    if file[1] != "min":
        print("This compiler only works for .min files")
        exit()
    source = open(filename).read()
    return


def main():
    load_source("source.min")
    program()

main()
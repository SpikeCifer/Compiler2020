# ---------------------------------------------------|CONTRIBUTERS|-----------------------------------------------------
# 2971: ΣΤΥΛΙΑΝΟΣ ΖΑΠΠΙΔΗΣ  cse52971
# 3059: ΖΗΣΙΜΟΣ ΠΑΡΑΣΧΗΣ    cse53059
# -----------------------------------------------------|TODO_NOTES|-----------------------------------------------------
# TODO: After each tag add : (This creates a problem in backpatch)
# -------------------------------------------------|Other Libraries|----------------------------------------------------
# from termcolor import colored
# -----------------------------------------------------|GLOBALS|--------------------------------------------------------
source = ""
start_index = 0
lexeme = [-1, ""]  # The lexeme that gets returned from lexer

line_index = 1              # Will be used for errors
char_index_of_line = 0      # Will be used for errors

# Intermediate code globals
tag_index = 1
quadsList = []  # It's a list of lists
temp_index = 1
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
               "inout", "input", "print", "then"]
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


def lex_error(error_type, c):  # Prints an appropriate lex error message
    print("Warning! Lex Error \nLine:", line_index, "Character:", char_index_of_line)
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
    print(error_message)
    exit()


def syntax_error(s):
    print("Warning! Syntax Error")
    print("In line", line_index)
    print(s)
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
            print("Lex Warning!\nNumber "+ word + " is out of bounds")
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


# --------------------------------------------|INTERMEDIATE CODE FUNCTIONS|---------------------------------------------
def nextQuad():
    return tag_index


def genQuad(op, x, y, z):  # They are all strings
    global tag_index, quadList
    tag = str(tag_index)+":"
    tag_index += 1
    quad = [tag, op, x, y, z]
    quadsList.append(quad)
    return


def printQuads():
    for quad in quadsList:
        print(quad)


def newTemp():
    global temp_index
    temp = temp_index
    temp_index += 1
    return "T_" + str(temp)


def emptyList():
    taglist = [""]
    return taglist


def makeList(x):
    taglist = [x]
    return taglist


def mergeLists(l1, l2):
    return l1 + l2


def backpatch(list, label):
    global quadsList
    for tag in list:
        for quad in quadsList:
            if quad[0].split(":")[0] == str(tag):  # When this gets over 9 it reads just 1
                quad[4] = label
    return
# ----------------------------------------------------|SYNTAX PART|-----------------------------------------------------


def program():  # The starting grammar rule
    global lexeme
    lexeme = lex()
    if lexeme[0] == PROGRAMTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            name = lexeme[1]  # store program's name
            lexeme = lex()
            if lexeme[0] == BRACKETTK and lexeme[1] == "{":
                lexeme = lex()
                block(name)
                if lexeme[0] == BRACKETTK and lexeme[1] == "}":
                    print("Syntax Check completed successfully!!")
                    printQuads()
                else:
                    msg = ""
                    finalT = lexeme
                    lexeme = lex()
                    if finalT[1] == ";" and lexeme[1] == "}":
                        msg += "';' character is not required at the end of last line"
                    elif finalT[1] in taken_words:
                        msg += "Statements not separated by ';' oper"
                    else:
                        msg += "Check if multiple statements are used not in {} block"
                    syntax_error("Expected '}' character to end program's block\nSuggestion: "+msg)

            else:
                syntax_error("Expected '{' character to start program's block")
        else:
            syntax_error("A program should always have a name")
    else:
        syntax_error("To start a program the keyword 'program' is expected")
    return


def block(name):
    declarations()
    subprograms()

    genQuad("begin_block", name, "_", "_")
    statements()
    # if (this is the main program block)
    # genquad("halt", "_", "_", "_")
    genQuad("end_block", name, "_", "_")
    return


def declarations():
    global lexeme
    while lexeme[0] == DECLARETK:
        lexeme = lex()
        varlist()
        if lexeme[0] == SEPARATORTK and lexeme[1] == ";":
            lexeme = lex()
        else:
            syntax_error("';' oper not found at the end of declare line")
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
                syntax_error("Expected variable after ',' character")
    return


def subprograms():
    while lexeme[0] == FUNCTIONTK or lexeme[0] == PROCEDURETK:
        subprogram()
    return


def subprogram():
    global lexeme
    if lexeme[0] == FUNCTIONTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            name = lexeme[1]
            lexeme = lex()
            funcbody(name)
        else:
            syntax_error("A function should always have a name")

    elif lexeme[0] == PROCEDURETK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            name = lexeme[1]
            lexeme = lex()
            funcbody(name)
        else:
            syntax_error("A procedure should always have a name")
    return


def funcbody(name):
    global lexeme
    formalpars()
    if lexeme[0] == BRACKETTK and lexeme[1] == "{":
        lexeme = lex()
        block(name)
        if lexeme[0] == BRACKETTK and lexeme[1] == "}":
            lexeme = lex()
        else:
            syntax_error("Expected '}' char to end the subprogram's block"
                         "\nCheck if multiple statements not in {}")
    else:
        syntax_error("Expected '{' to start the subprogram's block")
    return


def formalpars():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        formalparlist()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            msg = "Expected ')' character to stop declaring parameters"
            if lexeme[0] == IDTK:
                msg += "\nCheck if you have missed a parameter's type"
            syntax_error(msg)
    else:
        syntax_error("Expected '(' character to start declaring parameters")
    return


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
    else:
        syntax_error("Expected parameter type")


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
            syntax_error("Right curly bracket } was expected to stop statements block"
                         "\nCheck if you have missed a ; operator between statements")
    else:
        statement()


def statement():
    global lexeme
    if lexeme[0] == IDTK:
        id = lexeme[1]
        lexeme = lex()
        assignment_stat(id)
    elif lexeme[0] == IFTK:
        lexeme = lex()
        if_stat()
    elif lexeme[0] == WHILETK:
        lexeme = lex()
        while_stat()
    elif lexeme[0] == DOUBLEWHILETK:
        lexeme = lex()
        doublewhile_stat()
    elif lexeme[0] == LOOPTK:
        lexeme = lex()
        loop_stat()
    elif lexeme[0] == EXITTK:
        lexeme = lex()
        exit_stat()
    elif lexeme[0] == FORCASETK:
        lexeme = lex()
        forcase_stat()
    elif lexeme[0] == INCASETK:
        lexeme = lex()
        incase_stat()
    elif lexeme[0] == RETURNTK:
        lexeme = lex()
        return_stat()
    elif lexeme[0] == CALLTK:
        lexeme = lex()
        call_stat()
    elif lexeme[0] == INPUTTK:
        lexeme = lex()
        input_stat()
    elif lexeme[0] == PRINTTK:
        lexeme = lex()
        print_stat()
    else:
        if lexeme[1] == "}":
            syntax_error("Expected a statement")
        elif lexeme[1] == ";":
            syntax_error("Unnecessary ; at last statement")
        else:
            syntax_error("Invalid statement")


def assignment_stat(var):
    global lexeme
    if lexeme[0] == DECLARATORTK:
        lexeme = lex()
        Eplace = expression()
        genQuad(":=", Eplace, "_", var)
    else:
        syntax_error("Expected := symbol for assignment")
    return


def if_stat():  # S -> if B then {P1} S1{P2}TAIL {P3}
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        C = condition()  # S -> if B
        BTrue = C[0]
        BFalse = C[1]
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
            if lexeme[0] == THENTK:  # S -> if B then {P1}
                backpatch(BTrue, nextQuad())
                lexeme = lex()
                statements()  # S1

                ifList = makeList(nextQuad())
                genQuad("jump", "_", "_", "_")
                backpatch(BFalse, nextQuad())
                elsepart(C)

                backpatch(ifList, nextQuad())
            else:
                syntax_error("Expected keyword 'then'")
        else:
            syntax_error("Expected right bracket ) to close if condition")
    else:
        syntax_error("Expected left bracket ( to open if condition")


def elsepart(C):
    global lexeme
    if lexeme[0] == ELSETK:
        lexeme = lex()
        statements()
    return


def while_stat():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        condition()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
            statements()
        else:
            syntax_error("Expected right bracket ) to close while condition")
    else:
        syntax_error("Expected left bracket ( to open while condition")


def doublewhile_stat():
    global lexeme
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
                syntax_error("Expected keyword 'else' for doublewhile to have the proper syntax")
        else:
            syntax_error("Right bracket expected ) to end doublewhile condition")
    else:
        syntax_error("Expected left bracket ( to start doublewhile condition")


def loop_stat():
    statements()


def exit_stat():
    return


def forcase_stat():
    global lexeme
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
                    syntax_error("Expected ':' after condition symbol")
            else:
                syntax_error("Expected closing bracket ) to close when case condition")
        else:
            syntax_error("Expected opening bracket ( for when case condition")

    if lexeme[0] == DEFAULTTK:
        lexeme = lex()
        if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
            lexeme = lex()
            statements()
        else:
            syntax_error("Expected : symbol")
    else:
        syntax_error("Expected keyword 'default' for the default case")


def incase_stat():
    global lexeme
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
                    syntax_error("Expected ':' after condition symbol")
            else:
                syntax_error("Expected closing bracket ) to close when case condition")
        else:
            syntax_error("Expected opening bracket ( for when case condition")


def return_stat():
    expression()

# This is not necessary
def call_stat():
    global lexeme
    if lexeme[0] == IDTK:
        lexeme = lex()
        actualpars()
    else:
        syntax_error("Expected name of function to call")


def print_stat():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        genQuad("out", expression(), "_", "_")
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error("Expected right bracket ) to close print statment")
    else:
        syntax_error("Expected left bracket ( to open print statement")


def input_stat():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        if lexeme[0] == IDTK:
            genQuad("inp", lexeme[1], "_", "_")
            lexeme = lex()
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
            else:
                syntax_error("Expected closing bracket ) for input statement")
        else:
            syntax_error("Expected name of variable to save input")
    else:
        syntax_error("Expected opening bracket ( for input statement")


def actualpars():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        actualparlist()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error("Expected right bracket ) to close call parameters")
    else:
        syntax_error("Expected opening bracket ( to open call parameters")


def actualparlist():
    global lexeme
    if lexeme[0] == INTK or lexeme[0] == INOUTTK:
        actualparitem()
        while lexeme[0] == SEPARATORTK and lexeme[1] == ",":
            lexeme = lex()
            actualparitem()


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
    else:
        syntax_error("Expected type of parameter")


def condition():  # B-> Q1{P1}(or {P2}Q2 {P3})*
    global lexeme
    BTrue = emptyList()
    BFalse = emptyList()

    Q1 = boolterm()
    BTrue = Q1[0]   # Q1.true
    BFalse = Q1[1]  # Q1.false
    while lexeme[0] == ORTK:  # (or {P2}Q2 {P3})*
        backpatch(BFalse, nextQuad())

        lexeme = lex()
        Q2 = boolterm()

        BTrue = mergeLists(BTrue, Q2[0])
        BFalse = Q2[1]
    return BTrue, BFalse


def boolterm():  # Q->R1{P1}( and {P2}R2 {P3})*
    global lexeme
    QTrue = emptyList()
    QFalse = emptyList()

    R1 = boolfactor()

    QTrue = R1[0]   # R1.true
    QFalse = R1[1]  # R1.false
    while lexeme[0] == ANDTK:  # (and {P2} R2{P3})*

        backpatch(QTrue, nextQuad())

        lexeme = lex()
        R2 = boolfactor()

        QFalse = mergeLists(QFalse, R2[1])
        QTrue = R2[0]
    return QTrue, QFalse


def boolfactor():
    global lexeme
    RTrue = emptyList()
    RFalse = emptyList()

    if lexeme[0] == NOTTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "[":
            lexeme = lex()
            B = condition()  # R ->( B )

            # {P1}:
            RTrue = B[0]
            RFalse = B[1]
            if lexeme[0] == BRACKETTK and lexeme[1] == "]":
                lexeme = lex()
            else:
                syntax_error("Expected ]")
        else:
            syntax_error("Expected [")

    elif lexeme[0] == BRACKETTK and lexeme[1] == "[":
        lexeme = lex()
        B = condition()  # R ->( B )

        # {P1}:
        RTrue = B[0]
        RFalse = B[1]
        if lexeme[0] == BRACKETTK and lexeme[1] == "]":
            lexeme = lex()
        else:
            syntax_error("Expected ]")

    else:  # R ->E1 relop E2{P1}
        E1 = expression()          # x
        relop = relational_oper()  # <>=
        E2 = expression()          # y

        RTrue = makeList(nextQuad())
        genQuad(relop, E1, E2, "_")

        RFalse = makeList(nextQuad())
        genQuad("jump", "_", "_", "_")
    return RTrue, RFalse


def expression():
    global lexeme
    sign = optional_sign()  # Where should this be saved?
    T1place = sign + term()
    while lexeme[0] == ADDTK:  # (+T2{P1})*
        oper = add_oper()
        T2place = term()
        # {P1}
        w = newTemp()
        genQuad(oper, T1place, T2place, w)
        T1place = w
    return T1place


def term():
    global lexeme
    F1place = factor()       # F1
    while lexeme[0] == MULTIPLYTK:
        oper = mul_oper()
        F2place = factor()   # F2
        w = newTemp()
        genQuad(oper, F1place, F2place, w)
        F1place = w
    return F1place


def factor():
    global lexeme
    Fplace = ""
    if lexeme[0] == CONSTANTTK:
        Fplace = lexeme[1]
        lexeme = lex()

    elif lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        Fplace = expression()
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
        else:
            syntax_error("Right bracket ')' expected")

    elif lexeme[0] == IDTK:
        Fplace = lexeme[1]
        lexeme = lex()
        idtail()
    else:
        syntax_error("This factor's syntax is not supported")

    return Fplace


def idtail():
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        actualpars()


def relational_oper():
    global lexeme
    relop = ""
    if lexeme[0] == COMPARATORTK:
        relop = lexeme[1]
        lexeme = lex()
    else:
        syntax_error("Expected Relational Operator")
    return relop


def add_oper():
    global lexeme
    oper = ""
    if lexeme[0] == ADDTK:
        oper = lexeme[1]
        lexeme = lex()
    return oper


def mul_oper():
    global lexeme
    oper = ""
    if lexeme[0] == MULTIPLYTK:
        oper = lexeme[1]
        lexeme = lex()
    return oper


def optional_sign():
    sign = ""
    if lexeme[0] == ADDTK:
         sign = add_oper()
    return sign

# Function Load Source opens the source code file and saves the code in global variable source
def load_source(filename):
    global source
    file = filename.split(".")
    if file[1] != "min":
        print("This compiler only works for .min files", "red")
        exit()
    try:
        source = open(filename).read()
    except:
        print("I was incapable of finding the file you requested,\n"
              "please make sure it's in the same folder as the compiler!")
        exit()
    return


def main():
    load_source("source.min")
    program()
main()
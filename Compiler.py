import sys
# ---------------------------------------------------|CONTRIBUTERS|-----------------------------------------------------
# 2971: ΣΤΥΛΙΑΝΟΣ ΖΑΠΠΙΔΗΣ  cse52971
# 3059: ΖΗΣΙΜΟΣ ΠΑΡΑΣΧΗΣ    cse53059
# -----------------------------------------------------|TODO_NOTES|-----------------------------------------------------
# TODO: Test with big programs
# TODO: Fix char_index_of_line
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
program_name = ""
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

# ---------------------------------|DEFINE KEYWORDS PART|---------------------------------
# All of them were originally IDTKs, we now have to specify them
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

# ---------------------------------- USEFULL LISTS ---------------------------
taken_words = ["program", "declare", "if", "else", "while", "doublewhile", "loop", "exit", "forcase", "incase",
               "when", "default", "not", "and", "or", "function", "procedure", "call", "return", "in",
               "inout", "input", "print", "then"]                    # This list keeps the key words
double_ops = ["<>", ">=", "<=", ":="]  # This list keeps the double operator symbols
statement_tokens = [IDTK, IFTK, WHILETK, DOUBLEWHILETK, LOOPTK, EXITTK, FORCASETK, INCASETK, RETURNTK,
                    CALLTK, INPUTTK, PRINTTK]               # This list keeps all available statement tokens

# ----------------------- LEX ERRORS -----------------------
Error1 = 47  # Char after Digit
Error2 = 48  # Closed long comment without opening one
Error3 = 49  # Opened second comment inside another one
Error4 = 50  # EOF while in long comment
Error5 = 51  # Invalid symbol
stateE = {Error1, Error2, Error3, Error4, Error5}
# ----------------------- LEX PART -----------------------
# All of Lexer's states
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


# Function Load Source opens the source code file and saves the code in global variable source
def main():
    load_source("source.min")
    program()
    return


def load_source(filename):
    global source
    file = filename.split(".")
    if file[1] != "min":
        print("This compiler only works for .min files", "red")
        exit()
    try:
        source = open(filename).read()
    except FileNotFoundError:
        print("I was incapable of finding the file you requested,\n"
              "please make sure it's in the same folder as the compiler!")
        exit()
    return
# ----------------------------------------------------|LEXER PART|-----------------------------------------------------


def lex_error(error_type, c):  # Prints an appropriate lex error message
    print("Lex Error! \nLine:", line_index, "Character:", char_index_of_line)
    error_message = "Error Type "
    if error_type == Error1:
        error_message += "1: Digits can not be followed by characters"
    elif error_type == Error2:
        error_message += "2: Closed long comment without opening one"
    elif error_type == Error3:
        error_message += "3: Opened second comment inside another one"
    elif error_type == Error4:
        error_message += "4: EOF while in long comment"
    elif error_type == Error5:
        error_message += "5: Invalid symbol " + "'"+c+"'"
    else:
        error_message += "404: Undefined Error"
    print(error_message)
    exit()
    return


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
        if int(word) < -32767 or int(word) > 32767:
            print("Lex Warning!\nAt line "+str(line_index)+", number "+word+" is out of bounds")
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
            # if current state is a comment or starting state and lex read new line, update error pointers
            if (state == state0 or state in comments) and symbol == '\n':
                line_index += 1
                char_index_of_line = 0

            state = update_state(state, symbol)
            if state in [state1, state2]:  # State1 creates ids, State2 creates Constants
                if len(word) <= 30:        # If max buffer size has been reached don't add to word
                    word += symbol
            elif state in [state3, state4]:
                temp = symbol
            elif state in [state5, state8]:
                temp = ""
            elif state in [state11, state12, state13]:
                temp = symbol
            # Any other state does not affect the word
            current_char += 1

    char_index_of_line += current_char - 1
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
    global tag_index
    tag = str(tag_index)+":"
    tag_index += 1
    quad = [tag, op, x, y, z]
    quadsList.append(quad)
    return


def printQuads():
    for quad in quadsList:
        print(quad)
    return


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


def backpatch(patchlist, label):
    global quadsList
    for tag in patchlist:
        for quad in quadsList:
            if quad[0].split(":")[0] == str(tag):
                quad[4] = label
    return


def createC():  # This function creates an equal C program
    printQuads()
    file = open(program_name+".c", "w")
    file.write("#include <stdio.h>\n")
    file.write("int main(){\n")

    for quad in quadsList:
        line_result = "\tL_" + quad[0] + " "  # Create Label
        if quad[1] not in ['begin_block', 'end_block']:
            # Special Jump Command
            if quad[1] == "jump":
                line_result += "goto L_" + str(quad[4])

            # User communication commands
            elif quad[1] == "out":
                line_result += 'printf("'+'%d",'+quad[2]+')'
            elif quad[1] == "inp":
                line_result += 'scanf("'+'%d",&'+quad[2]+')'

            # Assignment command
            elif quad[1] == ":=":
                line_result += str(quad[4]) + "=" + str(quad[2])

            # Logic operators
            elif quad[1] in "<>=":
                if quad[1] == "=":
                    line_result += "if (" + str(quad[2]) + "==" + str(quad[3]) + ") goto L_" + str(quad[4])
                else:
                    line_result += "if (" + str(quad[2]) + str(quad[1]) + str(quad[3]) + ") goto L_" + str(quad[4])

            # Math functions
            elif quad[1] in '+-*/':
                line_result += str(quad[4]) + "=" + str(quad[2]) + str(quad[1]) + str(quad[3])

            # Exit of block and exit command (Should not be the same)
            elif quad[1] == "halt":
                line_result += "exit(0)"

            # In case I forgot something
            else:
                print("You forgot command(s)", quad[1])

            # End line and print the quad in short comment
            line_result += "; //" + str(quad[1:]) + "\n"
        else:
            line_result += " //" + str(quad[1:]) + "\n"  # Not a command line
        file.write(line_result)
    file.write("}")     # Close main block
    file.close()
    return
# ----------------------------------------------------|SYNTAX PART|-----------------------------------------------------


def syntax_error(error):
    print("Warning! Syntax Error")
    print("In line", line_index, "Character", char_index_of_line)
    print(error)
    exit()
    return


def program():  # The starting grammar rule
    global lexeme, program_name
    lexeme = lex()
    if lexeme[0] == PROGRAMTK:
        lexeme = lex()
        if lexeme[0] == IDTK:
            program_name = lexeme[1]
            lexeme = lex()
            if lexeme[1] == '{':
                lexeme = lex()
                block(program_name)
                if lexeme[1] == '}':
                    print("Syntax Check completed successfully!!")
                    createC()
                else:
                    msg = ""
                    finalT = lexeme
                    lexeme = lex()

                    if finalT[1] == ";" and lexeme[1] == "}":
                        msg += "The ';' separator is unnecessary after the program's last statement."
                    elif finalT[1] in taken_words:
                        msg += "Statements not separated by ';' operator"
                    else:
                        msg += "Check if multiple statements are not inside {} blocks"

                    syntax_error("Expected '}' bracket to end program's block\n"+msg)
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
    if name == program_name:
        genQuad("halt", "_", "_", "_")
    genQuad("end_block", name, "_", "_")
    return


def declarations():
    global lexeme
    while lexeme[0] == DECLARETK:
        lexeme = lex()
        char = varlist()
        if lexeme[1] == ';':
            lexeme = lex()
        else:
            syntax_error("Either ',' or ';' separator was expected after variable "+char)
    return


def varlist():
    global lexeme
    last_char = ""
    if lexeme[0] == IDTK:
        last_char = lexeme[1]
        lexeme = lex()
        while lexeme[1] == ',':
            lexeme = lex()
            if lexeme[0] == IDTK:
                last_char = lexeme[1]
                lexeme = lex()
            else:
                syntax_error("Expected variable's name after ',' character")
    elif lexeme[1] == ',':
        syntax_error("Expected a variable's name before the first ',' character")
    return last_char  # Return the last character written before the error pops up

# _________________________________________________ SUBPROGRAMS __________________________________________________


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
            if lexeme[0] == IDTK:
                syntax_error("Parameter "+lexeme[1]+"'s type has not been declared")
            else:
                syntax_error("Expected either another variable name or ')' to stop declaring parameters")
    else:
        syntax_error("Expected '(' character to start declaring parameters")
    return


def formalparlist():
    global lexeme
    if lexeme[0] == INTK or lexeme[0] == INOUTTK:
        formalparitem()
        while lexeme[0] == SEPARATORTK and lexeme[1] == ",":
            lexeme = lex()
            if lexeme[0] not in [INTK, INOUTTK]:
                syntax_error("Expected another parameter's type after ','")
            formalparitem()
    return


def formalparitem():
    global lexeme
    if lexeme[0] in [INTK, INOUTTK]:
        par_type = lexeme[1]
        lexeme = lex()
        if lexeme[0] == IDTK:
            lexeme = lex()
        else:
            syntax_error("Expected parameter's name after type "+par_type)
    return
# ______________________________________________ STATEMENTS _____________________________________


def assignment_stat(var):
    global lexeme
    if lexeme[0] == DECLARATORTK:
        lexeme = lex()
        Eplace = expression()
        genQuad(":=", Eplace, "_", var)
    else:
        syntax_error("Expected := symbol for assignment")
    return


def if_stat():  # S -> if B then {P1} S1 {P2} TAIL{P3}
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

                ifList = makeList(nextQuad())  # Create a jump, and fill it after the else part is done
                genQuad("jump", "_", "_", "_")
                backpatch(BFalse, nextQuad())
                elsepart(C)

                backpatch(ifList, nextQuad())  # Else part is done, if True jump to the next quad
            else:
                syntax_error("Expected keyword 'then' after if clause's condition")
        else:
            syntax_error("Expected right bracket ) to close if clause's condition")
    else:
        syntax_error("Expected left bracket ( to open if clause's condition")


def elsepart(C):
    global lexeme
    if lexeme[0] == ELSETK:
        lexeme = lex()
        statements()
    return


def while_stat():
    global lexeme
    '''
    BTrue = emptyList()
    BFalse = emptyList()
    '''
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        Bquad = nextQuad()  # Return to condition check
        lexeme = lex()
        C = condition()

        BTrue = C[0]
        BFalse = C[1]
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()
            backpatch(BTrue, nextQuad())
            statements()
            genQuad("jump", "_", "_", Bquad)
            backpatch(BFalse, nextQuad())
        else:
            syntax_error("Expected right bracket ) to close while condition")
    else:
        syntax_error("Expected left bracket ( to open while condition")


# optional
def doublewhile_stat():  # The state/flag was an interesting concept
    global lexeme
    '''
    BTrue = emptyList()
    BFalse = emptyList()
    '''
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        state = newTemp()
        genQuad(":=", "0", "_", state)  # Initialize loop state
        condQuad = nextQuad()
        lexeme = lex()
        C = condition()

        BTrue = C[0]
        BFalse = C[1]
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            lexeme = lex()

            backpatch(BTrue, nextQuad())
            state1_list = makeList(nextQuad())
            genQuad("=", "2", state, "_")
            genQuad(":=", "1", "_", state)

            statements()  # True statements
            genQuad("jump", "_", "_", condQuad)
            if lexeme[0] == ELSETK:
                lexeme = lex()

                backpatch(BFalse, nextQuad())
                state2_list = makeList(nextQuad())
                genQuad("=", "1", state, "_")
                genQuad(":=", "2", "_", state)

                statements()

                genQuad("jump", "_", "_", condQuad)

                backpatch(state1_list, nextQuad())
                backpatch(state2_list, nextQuad())

            else:
                syntax_error("Expected keyword 'else' for doublewhile to have the proper syntax")
        else:
            syntax_error("Right bracket expected ) to end doublewhile condition")
    else:
        syntax_error("Expected left bracket ( to start doublewhile condition")


# optional
def loop_stat():  # The program repeats the following statments until
    Bquad = nextQuad()
    statements()
    genQuad("jump", "_", "_", Bquad)


# optional
def exit_stat():
    genQuad("halt", "_", "_", "_")
    return


def forcase_stat():
    global lexeme
    BTrue = emptyList()
    BFalse = emptyList()

    case = newTemp()
    first_quad = nextQuad()  # Keep the first quad, we will return to it
    while lexeme[0] == WHENTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            C = condition()
            BTrue = C[0]
            BFalse = C[1]
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
                if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
                    lexeme = lex()

                    backpatch(BTrue, nextQuad())
                    statements()
                    genQuad("jump", "_", "_", first_quad)
                    backpatch(BFalse, nextQuad())

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


# optional
def incase_stat():
    global lexeme
    BTrue = emptyList()
    BFalse = emptyList()

    t = newTemp()
    first_quad = nextQuad()
    genQuad(":=", "0", "_", t)

    while lexeme[0] == WHENTK:
        lexeme = lex()
        if lexeme[0] == BRACKETTK and lexeme[1] == "(":
            lexeme = lex()
            C = condition()
            BTrue = C[0]
            BFalse = C[1]
            if lexeme[0] == BRACKETTK and lexeme[1] == ")":
                lexeme = lex()
                if lexeme[0] == SEPARATORTK and lexeme[1] == ":":
                    lexeme = lex()
                    backpatch(BTrue, nextQuad())
                    statements()
                    genQuad(":=", "1", "_", t)
                    backpatch(BFalse, nextQuad())
                else:
                    syntax_error("Expected ':' after condition symbol")
            else:
                syntax_error("Expected closing bracket ) to close when case condition")
        else:
            syntax_error("Expected opening bracket ( for when case condition")
    genQuad("=", "1", t, first_quad)
    return


def return_stat():
    genQuad("retv", expression(), "_","_")
    return


def call_stat():
    global lexeme
    if lexeme[0] == IDTK:
        function = lexeme[1]
        lexeme = lex()
        actualpars()
        genQuad("call", '_', "_", function)
    else:
        if lexeme[1] in taken_words:
            syntax_error(lexeme[1]+" is a key word, you can not use it as a function's name")
        else:
            syntax_error("Expected name of procedure to call")


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


statements_selector = {
    IDTK: assignment_stat,
    IFTK: if_stat,
    WHILETK: while_stat,
    DOUBLEWHILETK: doublewhile_stat,
    LOOPTK: loop_stat,
    EXITTK: exit_stat,
    FORCASETK: forcase_stat,
    INCASETK: incase_stat,
    RETURNTK: return_stat,
    CALLTK: call_stat,
    PRINTTK: print_stat,
    INPUTTK: input_stat
}


def statements():
    global lexeme
    statements_counter = [0]
    if lexeme[0] == BRACKETTK and lexeme[1] == "{":
        lexeme = lex()
        statement(statements_counter)
        while lexeme[0] == SEPARATORTK and lexeme[1] == ";":
            lexeme = lex()
            statement(statements_counter)

        if lexeme[0] == BRACKETTK and lexeme[1] == "}":
            lexeme = lex()
        else:
            syntax_error("Right curly bracket } was expected to stop statements block"
                         "\nMaybe you missed a ';' operator between previous statements")
    else:
        statement(statements_counter)
    return


def statement(counter):
    global lexeme
    if lexeme[0] in statement_tokens:
        counter[0] += 1
        statement_id = statements_selector.get(lexeme[0])
        if lexeme[0] == IDTK:  # Special case where a parameter has to be passed to the method
            word = lexeme[1]
            lexeme = lex()
            statement_id(word)
        else:
            lexeme = lex()
            statement_id()
    else:
        expected = "Error 1. Expected a statement!"
        if counter[0] > 0:
            syntax_error(expected+"\nProblem: The block's last statement has no need of ';' separator")
        elif lexeme[1] == '}':
            syntax_error(expected+"\nProblem: I am sorry, our services do not accept empty statement blocks")
        else:
            syntax_error("Expected '}' bracket")
    return


def actualpars():
    global lexeme
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        lexeme = lex()
        parlist = actualparlist() # Get the parameters' list
        if lexeme[0] == BRACKETTK and lexeme[1] == ")":
            for par in parlist:
                genQuad("par", par[1], par[0], '_') # Create the parameter quads after you have collected all parameters
            lexeme = lex()
        else:
            msg = "Expected right bracket ) to close call parameters"
            if lexeme[0] == IDTK:
                msg += "\n Suggestion: Parameter "+lexeme[1]+"'s type has not been declared"
            syntax_error(msg)
    else:
        syntax_error("Expected opening bracket ( to open call parameters")


def actualparlist():
    global lexeme
    parlist = []
    if lexeme[0] == INTK or lexeme[0] == INOUTTK:
        parlist.append(actualparitem())
        while lexeme[0] == SEPARATORTK and lexeme[1] == ",":
            lexeme = lex()
            parlist.append(actualparitem())
    return parlist


def actualparitem():
    global lexeme
    par_type = ''
    if lexeme[0] == INTK:  # CV par
        par_type = 'CV'
        lexeme = lex()
        var = expression()
    elif lexeme[0] == INOUTTK:  # REF par
        par_type = 'REF'
        lexeme = lex()
        if lexeme[0] == IDTK:
            var = lexeme[1]
            lexeme = lex()
        else:
            syntax_error("Variable name was expected")
    return par_type, var # Return parameter type and name


def condition():  # B-> Q1{P1}(OR {P2}Q2 {P3})*
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


def boolterm():  # Q->R1{P1}( AND {P2}R2 {P3})*
    global lexeme
    QTrue = emptyList()
    QFalse = emptyList()

    R1 = boolfactor()

    QTrue = R1[0]   # R1.true
    QFalse = R1[1]  # R1.false
    while lexeme[0] == ANDTK:  # (and {P2} R2{P3})*

        backpatch(QTrue, nextQuad())  # If condition is true, go to the immediate next quad

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
            RTrue = B[1]
            RFalse = B[0]
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
    sign = optional_sign()
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
        id = lexeme[1]
        lexeme = lex()
        Fplace = idtail(id)
    else:
        syntax_error("This factor's syntax is not supported")

    return Fplace


def idtail(id):
    if lexeme[0] == BRACKETTK and lexeme[1] == "(":
        actualpars()
        w = newTemp()
        genQuad("par", w, "RET", "_")
        genQuad("call", '_', '_', id)
        return w
    else:
        return id


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


if __name__ == "__main__":
    main()

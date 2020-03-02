# -----------------------------------------------------|GLOBALS|--------------------------------------------------------
source = ""
start_index = 0

line_index = 1              # Will be used for errors
char_index_of_line = 1      # Will be used for errors
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
# ------------------------ DEFINE GENERAL TOKENS PART ------------------------
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

# ------------------------ DEFINE SPECIAL TOKENS PART ------------------------
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
INCASETK  = 32
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

taken_words = ["program", "declare", "if", "else", "while", "doublewhile", "loop", "exit", "forcase", "incase",
               "when", "default", "not", "and", "or", "function", "procedure", "call", "return", "in",
               "inout", "input", "print"]
double_ops = ["<>", ">=", "<=", ":="]
# ----------------------- LEX ERRORS -----------------------
Error1 = 46  # Char after Digit
Error2 = 47  # Closed long comment without opening one
Error3 = 48  # Opened second comment inside another one
Error4 = 49  # EOF while in long comment
Error5 = 50  # Invalid symbol
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


def error(error_type):
    print("There was a Lex Error in Line:", line_index, "Character:", char_index_of_line)
    print("More specifically:")
    if error_type == Error1:
        print("\tError", error_type, ": Digits can not be followed by characters")
    elif error_type == Error2:
        print("\tError", error_type, ": Closed long comment without opening one")
    elif error_type == Error3:
        print("\tError", error_type, ": Opened second comment inside another one")
    elif error_type == Error4:
        print("\tError", error_type, ": EOF while in long comment")
    elif error_type == Error5:
        print("\tError", error_type, ": Invalid symbol")
    else:
        print("\tUndefined error")
    exit()


def eof(current_char):
    total = start_index + current_char
    if total > len(source)-1:
        return True
    return False


def find_symbol(symbol):
    global line_index, char_index_of_line
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
            line_index += 1
            char_index_of_line = 0
            return 17
        else:
            return 18

    else:
        return 20


def update_state(state, char):
    column = find_symbol(char)
    state = states[state][column]
    return state


def identify(token, word):
    for i in range(0, len(taken_words)):
        if word == taken_words[i]:
            token = i + 23
    return token


def handle_return(token, word, temp, symbol, index):
    global start_index
    if token == IDTK:
        token = identify(token, word)
        start_index += index - 1
        return token, word

    elif token == CONSTANTTK:
        start_index += index - 1
        return token, word

    elif token in singles:
        if temp == ":":
            start_index += index - 1
            return token, temp
        else:
            start_index += index
        return token, symbol

    elif token == MULTIPLYTK:
        start_index += index - 1
        return token, temp

    elif token == COMPARATORTK:
        opp = temp + symbol
        if opp in double_ops:
            start_index += index
            return token, opp
        elif symbol == "=":
            start_index += index
            return token, symbol
        else:
            start_index += index - 1
            return token, temp

    elif token == DECLARATORTK:
        start_index += index
        return token, ":="

    elif token == EOFTK:
        start_index += index
        return token, ""


def lex():
    current_char = 0
    state = state0
    word = ""  # Word must be a buffer[30]
    temp = ""
    symbol = ""
    while state not in stateR and state not in stateE:
        if eof(current_char):
            state = states[state][19]  # All of them are in stateR so it exits immediately
            current_char +=1
        else:
            symbol = source[start_index + current_char]
            state = update_state(state, symbol)
            if state in longs:  # State1 or State2 create IDs or Constants
                word += symbol
            elif state == state3 or state == state4:
                temp = symbol
            elif state == state5 or state == state8:
                temp = ""
            elif state == state11 or state == state12 or state == state13:
                temp = symbol
            # Any other state does not affect the word
            current_char += 1

    # start_index += current_char
    if state in stateE:
        error(state)
    else:
        token = state
        return handle_return(token, word, temp, symbol, current_char)


def load_source(filename):
    global source
    source = open(filename).read()
    return


def main():
    load_source("source.min")
    for i in range(0, 4):
        print(lex())
main()


def error(s):
    print(s);


def program():
	if (token == PROGRAMTK):
		token = lex();
		if (token == IDTK):
			token = lex()[0];
			block();
                else error("program name expected");
	else error("the keyword 'program' was expected");		



def block():

	declarations();
	subprograms();
	statements();


def declarations():
	while (token == DECLARETK):
			token = lex()[0];
			varlist();
			if (token == semicoltk):
				token = lex()[0];
			
	


def varlist():

	if (token == IDTK):
		token = lex()[0];
		while (token == comtk):
			token = lex()[0];

def subprograms():

	while (token == FUNCTIONTK || token == PROCEDURETK):
		subprograms();
    

def subprogram():

	if (token == FUNCTIONTK):
		token = lex()[0];
		if (token == IDTK):
			token = lex()[0];
			funcbody();
		else error ("The keyword 'id' was expected");
		
	else if (token == PROCEDURETK):
		token = lex()[0];
		if (token == IDTK):
			token = lex()[0];
			funcbody();
		else error ("The keyword 'id' was expected");
	


def funcbody():
	formalpars();
	if (token == BRACKETTK):
		token = lex()[0];
		block();
		if (token == BRACKETTK):
			token = lex()[0];
		else error ("Right curly brackett expected");

def formalpars():

	if (token == BRACKETTK):
		token = lex()[0];
		formalparlist();
		if (token == BRACKETTK):
			token = lex()[0];
		else error ("right bracket expected");


def formalparitem():
	if (token == INTTK):
		token = lex()[0];
		if (token == IDTK):
			token = lex()[0];
		else error ("The keyword 'id' expected");
	
	else if (token == INOUTTK):
		token = lex()[0];
		if (token == idtk):
			token = lex()[0];
		else error ("The keyword 'id' expected");
		
	


def statements():
	statement();
	if (token == BRACKETTK):
		token = lex()[0];
		statement();
		while (token == semicoltk):
			statement();
		if (token == BRACKETTK):
			token = lex()[0];
		else error ("Right curly bracket expected");


def ifstat():

	if (token == BRACKETTK):
		token = lex()[0];
		condition();
		if(token == BRACKETTK):
			token = lex()[0];
		else error ("Right brackett expected");
	  
	if (token == THENTK):
		token = lex()[0];
		statements();
		elsepart();
	else error ("the keyword ‘then’ was expected"); 



def elsepart():
    
	if (token == THENTK):
		token = lex()[0];
		statements();


def whilestat():
    
	if (token == WHILETK):
		token = lex()[0];
		if (token == BRACKETTK):
			token = lex()[0];
			condition();
			if(token == BRACKETTK):
				token = lex()[0];
			else error ("Right brackett expected");
		statements();
	else error ("the keyword 'while' was expected");	


void doublewhilestat()
{
	if (token == DOUBLEWHILETK){
		token = lex()[0];
		if (token == BRACKETTK){
			token = lex()[0];
			condition();
			if(token == BRACKETTK){
				token = lex()[0];
			else error ("Right brackett expected");
			}	
		}
		statements();
		if (token == ELSETK){
			token = lex()[0];
			statements();
		}
	else error ("The keyword 'doublewhile' was expected");
	}
}		
		
	
void loopstat()
{
	if (token == LOOPTK){
		token = lex()[0];
		statements();
	else error ("The keyword 'loop' was expected");
	}
}


void exitstat()
{
	if (token == EXITTK){
		token = lex()[0];
	else error("The keyword 'exit' was expected")	
	}
}
	
	
void forcasestat()
{
		if (token == FORCASETK){
			while (token == WHENTK){
				condition();
				if (token == coltk){
					statements();
				}
			}
		else error ("The keyword 'forcase' was expected");
		}
}

	
void incasestat()
{
	if (token == INCASETK){
			while (token == WHENTK){
				condition();
				if (token == coltk){
					statements();
				}
			}
	else error ("The keyword 'incase' was expected");
	}	
}	
		
		
void returnstat()
{
	if (token == RETURNTK){
		token = lex()[0];
		expression();
	else error ("The keyword 'return' was expected");
	}
}



void callstat()
{
	if (token == CALLTK){
		token = lex()[0];
		if (token == IDTK){
			token = lex()[0];
			if (token == BRACKETTK){
				token = lex()[0];
				actualparlists();
				if (token == BRACKETTK){
					token = lex()[0];
					else error ("right bracket expected");
				}	
			}
		else error ("The keyword 'id' was expected");
		}
	else error ("The keyword 'call' was expected");
	}
}


void printstat()
{
	if (token == PRINTTK){
		token = lex()[0];
		if (token == BRACKETTK){
			token = lex()[0];
			expression();
			if (token == BRACKETTK){
				token = lex()[0];
				else error ("right bracket expected");
			}
		}
	else error ("The keyword 'print' was expected");
	}
}


void inputstat()
{
	if (token == INPUTTK){
		token = lex()[0];
		if (token == BRACKETTK){
			token == lex();
			if (token == IDTK){
				token = lex()[0];
			else error ("The keyword 'id' was expected");
			}
			if (token == BRACKETTK){
				token = lex()[0];
			else error ("Right bracket expected");
			}
		}
	else error ("The keyword 'input' was expected");
    }
}


void actualpars()
{
	if (token == BRACKETTK){
			token = lex()[0];
			actualparlist();
			if (token == BRACKETTK){
				token = lex()[0];
			else error ("Right bracket expected");
			}	
	}
}


void actualparitem ()
{
	if (token == INTTK){
		token = lex()[0];
		expression();
	}
	else if (token == INOUTTK){
		token = lex()[0];
		if (token == IDTK){
			token = lex()[0];
		else error ("The keyword 'id' was expected");
		}
	}
}


void condition()
{
	boolterm();
	while (token == ORTK ){
		boolterm();
	}
}	


void boolterm()
{
	boolfactor();
	while (token == ANDTK ){
		boolfactor();
	}
}


void boolfactor()
{
	if (token == NOTTK){
			token = lex();
			if (token == BRACKETTK){
				token = lex()[0];
				condition ();
			}
			if (token == BRACKETTK){
				token = lex()[0];
			else error(“right bracket expected”); 
			}
	else if (token == BRACKETTK){
				token = lex()[0];
				condition ();
			}
			if (token == BRACKETTK){
				token = lex()[0];
			else error(“right bracket expected”); 
			}		
	else{
			expression();
			relOper();
			expression();
	}
  }
}

void expression()
{
	optionalsign();
	term();
	while (token == plustk || token == minustk){
		addoper();
		term();
	}
}

void term()
{
	factor();
	while (token == asterisktk || token == forwardslashtk){
		mulOper();
		factor();
	}
}







void addoper()
{
	if (token == ADDTK){
		token = lex();
	}
	else if (token == minustk){
		token = lex();
	}
}

void mulOper()
{
	if (token == asterisktk){
		token = lex();
	}
	else if (token == forwardslashtktk){
		token = lex();
	}
}

void optionalsign()
{
	addoper();
}
	
				


	
			




	
	
	

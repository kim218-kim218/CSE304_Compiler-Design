# Name: Nahyun Kim
# nahyun.kim.4@stonybrook.edu

from lexer import initLexer, getNextToken
import sys
import os

current_token = None

def match(expected_type):
    global current_token
    if current_token.type == expected_type:
        current_token = getNextToken()
    else:
        print(f" ** Error: Expected {expected_type} but got {current_token.type}")
        sys.exit(1)

def lookahead():
    return current_token.type

def program():
    production("Program => decllist funcdecls T_EOF")
    decllist()
    funcdecls()
    if lookahead() != "T_EOF":
        print(f" ** Error in program: Expected T_EOF but got {lookahead()}")
        sys.exit(1)

def funcdecls():
    if lookahead() == "T_FUNCTION":
        production("funcdecls => funcdecl funcdecls")
        funcdecl()
        funcdecls()
    elif lookahead() == "T_Ident" and current_token.value == "main":
        production("funcdecls => maindecl")
        maindecl()
    else:
        print(f" ** Error in funcdecls: got {lookahead()}")
        sys.exit(1)

def funcdecl():
    production("funcdecl => FUNCTION ftypespec simplevar fdeclparms LBRACE decllist statementlist RBRACE")
    match("T_FUNCTION")
    ftypespec()
    simplevar()
    fdeclparms()
    match("T_LBRACE")
    decllist()
    statementlist()
    match("T_RBRACE")

def maindecl():
    production("maindecl => MAIN LPAREN RPAREN LBRACE decllist statementlist RBRACE")
    match("T_Ident")  # "main"
    match("T_LPAREN")
    match("T_RPAREN")
    match("T_LBRACE")
    decllist()
    statementlist()
    match("T_RBRACE")

def ftypespec():
    if lookahead() in ["T_VOID", "T_INT", "T_FLOAT"]:
        production(f"ftypespec => {lookahead()}")
        match(lookahead())
    else:
        print(f" ** Error in ftypespec: got {lookahead()}")
        sys.exit(1)

def simplevar():
    production("simplevar => ID")
    match("T_Ident")

def fdeclparms():
    production("fdeclparms => LPAREN fparmlist RPAREN")
    match("T_LPAREN")
    fparmlist()
    match("T_RPAREN")

def fparmlist():
    if lookahead() in ["T_INT", "T_FLOAT"]:
        production("fparmlist => fparm fparmlistrem")
        fparm()
        fparmlistrem()
    else:
        production("fparmlist => e")

def fparm():
    production("fparm => typespec parmVar")
    typespec()
    parmVar()

def parmVar():
    production("parmVar => ID parmVarTail")
    match("T_Ident")
    parmVarTail()

def parmVarTail():
    if lookahead() == "T_LBRACKET":
        production("parmVarTail => LBRACKET RBRACKET parmVarTail")
        match("T_LBRACKET")
        match("T_RBRACKET")
        parmVarTail()
    else:
        production("parmVarTail => e")

def fparmlistrem():
    if lookahead() == "T_COMMA":
        print("fparmlistrem => COMMA fparm fparmlistrem")
        match("T_COMMA")
        fparm()
        fparmlistrem()
    else:
        print("fparmlistrem => e")

def decllist():
    if lookahead() in ["T_INT", "T_FLOAT"]:
        production("decllist => decl decllist")
        decl()
        decllist()
    else:
        production("decllist => e")

def bstatementlist():
    production("bstatementlist => LBRACE statementlist RBRACE")
    match("T_LBRACE")
    statementlist()
    match("T_RBRACE")

def statementlist():
    if lookahead() in ["T_IF", "T_WHILE", "T_Ident", "T_PRINT", "T_READ", "T_RETURN", "T_CALL"]:
        production("statementlist => statement statementlisttail")
        statement()
        statementlisttail()
    else:
        production("statementlist => e")

def statementlisttail():
    if lookahead() == "T_SEMICOLON":
        production("statementlisttail => SEMICOLON statementlist")
        match("T_SEMICOLON")
        statementlist()
    else:
        production("statementlisttail => e")

def decl():
    production("decl => typespec variablelist")
    typespec()
    variablelist()

def variablelist():
    production("variablelist => variable variablelisttail")
    variable()
    variablelisttail()

def variablelisttail():
    if lookahead() == "T_COMMA":
        production("variablelisttail => COMMA variable variablelisttail")
        match("T_COMMA")
        variable()
        variablelisttail()
    elif lookahead() == "T_SEMICOLON":
        production("variablelisttail => SEMICOLON")
        match("T_SEMICOLON")
    else:
        print(f"** Error in variablelisttail: got {lookahead()}")
        sys.exit(1)

def variable():
    production("variable => ID variabletail")
    match("T_Ident")
    variabletail()

def variabletail():
    if lookahead() == "T_LBRACKET":
        production("variabletail => LBRACKET ICONST RBRACKET variabletail")
        match("T_LBRACKET")
        match("T_ICONST")
        match("T_RBRACKET")
        variabletail()
    else:
        production("variabletail => e")

def typespec():
    if lookahead() == "T_INT":
        production("typespec => INT")
        match("T_INT")
    elif lookahead() == "T_FLOAT":
        production("typespec => FLOAT")
        match("T_FLOAT")
    else:
        print(f"** Error in typespec: got {lookahead()}")
        sys.exit(1)

def usevariable():
    production("usevariable => ID usevariabletail")
    match("T_Ident")
    usevariabletail()

def usevariabletail():
    if lookahead() == "T_LBRACKET":
        production("usevariabletail => arraydim")
        arraydim()
    else:
        production("usevariabletail => e")

def arraydim():
    if lookahead() == "T_LBRACKET":
        production("arraydim => LBRACKET arraydimtail")
        match("T_LBRACKET")
        arraydimtail()
    else:
        production("arraydim => e")


def arraydimtail():
    if lookahead() == "T_ICONST":
        production("arraydimtail => ICONST RBRACKET arraydim")
        match("T_ICONST")
        match("T_RBRACKET")
        arraydim()
    elif lookahead() == "T_Ident":
        production("arraydimtail => ID RBRACKET arraydim")
        match("T_Ident")
        match("T_RBRACKET")
        arraydim()
    else:
        print(f"** Error in arraydimtail: got {lookahead()}")
        sys.exit(1)

def statement():
    token = lookahead()
    if token == "T_WHILE":
        production("statement => whilestatement")
        whilestatement()
    elif token == "T_IF":
        production("statement => ifstatement")
        ifstatement()
    elif token == "T_Ident":
        production("statement => assignmentstatement")
        assignmentstatement()
    elif token == "T_PRINT":
        production("statement => printstatement")
        printstatement()
    elif token == "T_READ":
        production("statement => readstatement")
        readstatement()
    elif token == "T_RETURN":
        production("statement => returnstatement")
        returnstatement()
    elif token == "T_CALL":
        production("statement => callstatement")
        callstatement()
    else:
        print(f"** Error in statement: got {lookahead()}")
        sys.exit(1)

def basicexpr():
    production("basicexpr => basicterm basicexprtail")

def basicexprtail():
    if lookahead() == "T_PLUS":
        production("basicexprtail => PLUS basicterm basicexprtail")
        match("T_PLUS")
        basicterm()
        basicexprtail()
    elif lookahead() == "T_MINUS":
        production("basicexprtail => MINUS basicterm basicexprtail")
        match("T_MINUS")
        basicterm()
        basicexprtail()
    else:
        production("basicexprtail => e")

def basicterm():
    production("basicterm => basicfactor basictermtail")
    basicfactor()
    basictermtail()

def basictermtail():
    if lookahead() == "T_MULT":
        production("basictermtail => MULT basicfactor basictermtail")
        match("T_MULT")
        basicfactor()
        basictermtail()
    elif lookahead() == "T_DIV":
        production("basictermtail => DIV basicfactor basictermtail")
        match("T_DIV")
        basicfactor()
        basictermtail()
    else:
        production("basictermtail => e")

def basicfactor():
    if lookahead() == "T_Ident":
        production("basicfactor => ID")
        match("T_Ident")
    elif lookahead() == "T_ICONST":
        production("basicfactor => ICONST")
        match("T_ICONST")
    else:
        print(f"** Error in basicfactor: got {lookahead()}")
        sys.exit(1)

def assignmentstatement():
    production("assignmentstatement => usevariable ASSIGN otherexpression")
    usevariable()
    match("T_ASSIGN")
    otherexpression()

def otherexpression():
    production("otherexpression => term otherexpressiontail")
    term()
    otherexpressiontail()

def otherexpressiontail():
    if lookahead() == "T_PLUS":
        production("otherexpressiontail => PLUS term otherexpressiontail")
        match("T_PLUS")
        term()
        otherexpressiontail()
    elif lookahead() == "T_MINUS":
        production("otherexpressiontail => MINUS term otherexpressiontail")
        match("T_MINUS")
        term()
        otherexpressiontail()
    else:
        production("otherexpressiontail => e")

def term():
    production("term => factor termtail")
    factor()
    termtail()

def termtail():
    if lookahead() == "T_MULT":
        production("termtail => MULT factor termtail")
        match("T_MULT")
        factor()
        termtail()
    elif lookahead() == "T_DIV":
        production("termtail => DIV factor termtail")
        match("T_DIV")
        factor()
        termtail()
    else:
        production("termtail => e")

def factortail():
    if lookahead() == "T_LBRACKET":
        production("factortail => usevariabletail")
        usevariabletail()
    elif lookahead() == "T_LPAREN":
        production("factortail => funccalltail")
        funccalltail()
    else:
        production("factortail => e")

def funccalltail():
    production("funccalltail => LPAREN arglist RPAREN")
    match("T_LPAREN")
    arglist()
    match("T_RPAREN")

def arglist():
    if lookahead() in ["T_Ident", "T_ICONST", "T_FCONST", "T_LPAREN", "T_MINUS"]:
        production("arglist => otherexpression arglistrem")
        otherexpression()
        arglistrem()
    else:
        production("arglist => e")

def arglistrem():
    if lookahead() == "T_COMMA":
        production("arglistrem => COMMA otherexpression arglistrem")
        match("T_COMMA")
        otherexpression()
        arglistrem()
    else:
        production("arglistrem => e")

def factor():
    if lookahead() == "T_Ident":
        production("factor => ID factortail")
        match("T_Ident")
        factortail()
    elif lookahead() == "T_ICONST":
        production("factor => ICONST")
        match("T_ICONST")
    elif lookahead() == "T_FCONST":
        production("factor => FCONST")
        match("T_FCONST")
    elif lookahead() == "T_LPAREN":
        production("factor => LPAREN otherexpression RPAREN")
        match("T_LPAREN")
        otherexpression()
        match("T_RPAREN")
    elif lookahead() == "T_MINUS":
        production("factor => MINUS factor")
        match("T_MINUS")
        factor()
    else:
        print(f"** Error in factor: got {lookahead()}")
        sys.exit(1)

def whilestatement():
    production("whilestatement => WHILE relationalexpr bstatementlist")
    match("T_WHILE")
    relationalexpr()
    bstatementlist()

def ifstatement():
    production("ifstatement => IF relationalexpr bstatementlist istail")
    match("T_IF")
    relationalexpr()
    bstatementlist()
    istail()

def istail():
    if lookahead() == "T_ELSE":
        production("istail => ELSE bstatementlist")
        match("T_ELSE")
        bstatementlist()
    else:
        production("istail => e")

def relationalexpr():
    production("relationalexpr => condexpr relationalexprtail")
    condexpr()
    relationalexprtail()

def relationalexprtail():
    if lookahead() == "T_AND":
        production("relationalexprtail => AND condexpr")
        match("T_AND")
        condexpr()
    elif lookahead() == "T_OR":
        production("relationalexprtail => OR condexpr")
        match("T_OR")
        condexpr()
    else:
        production("relationalexprtail => e")

def condexpr():
    if lookahead() == "T_LPAREN":
        production("condexpr => LPAREN otherexpression condexprtail RPAREN")
        match("T_LPAREN")
        otherexpression()
        condexprtail()
        match("T_RPAREN")
    elif lookahead() == "T_NOT":
        production("condexpr => NOT condexpr")
        match("T_NOT")
        condexpr()
    elif lookahead() in ["T_Ident", "T_ICONST", "T_FCONST", "T_LPAREN", "T_MINUS"]:
        production("condexpr => otherexpression condexprtail")
        otherexpression()
        condexprtail()
    else:
        print(f"** Error in condexpr: got {lookahead()}")
        sys.exit(1)

def condexprtail():
    if lookahead() == "T_LT":
        production("condexprtail => LT otherexpression")
        match("T_LT")
        otherexpression()
    elif lookahead() == "T_LE":
        production("condexprtail => LE otherexpression")
        match("T_LE")
        otherexpression()
    elif lookahead() == "T_GT":
        production("condexprtail => GT otherexpression")
        match("T_GT")
        otherexpression()
    elif lookahead() == "T_GE":
        production("condexprtail => GE otherexpression")
        match("T_GE")
        otherexpression()
    elif lookahead() == "T_EQ":
        production("condexprtail => EQUAL otherexpression")
        match("T_EQ")
        otherexpression()
    else:
        print(f"** Error in condexprtail: got {lookahead()}")
        sys.exit(1)

def printstatement():
    production("printstatement => PRINT otherexpression")
    match("T_PRINT")
    otherexpression()

def readstatement():
    production("readstatement => READ usevariable")
    match("T_READ")
    usevariable()

def returnstatement():
    match("T_RETURN")
    if lookahead() in ["T_Ident", "T_ICONST", "T_FCONST", "T_LPAREN", "T_MINUS"]:
        production("returnstatement => RETURN otherexpression")
        otherexpression()
    else:
        production("returnstatement => RETURN")

def callstatement():
    production("callstatement => CALL ID funccalltail")
    match("T_CALL")
    match("T_Ident")
    funccalltail()


# --------- Main -------------

current_token = None
logfile = None

def production(rule_str):
    print(rule_str)
    if logfile:
        logfile.write(rule_str + "\n")

if __name__ == "__main__":
    # Docker dir
    test_dir = "/app/tests"
    output_dir = "/app/output"

    fname = input("Enter RASCL source file name : ").strip()

    if not fname.endswith(".rsc"):
        print("Error: Please provide a .rsc file.")
        sys.exit(1)

    filename = os.path.join(test_dir, fname)

    if not os.path.isfile(filename):
        print(f" File '{filename}' not found in /app/tests.")
        sys.exit(1)

    rsp_filename = os.path.join(output_dir, fname.rsplit(".", 1)[0] + ".rsp")

    try:
        logfile = open(rsp_filename, "w")
    except:
        print("Error: could not create output log file.")
        sys.exit(1)

    if not initLexer(filename):
        print(f"Error: Failed to read file '{filename}'")
        sys.exit(1)

    current_token = getNextToken()
    production("Parsing program:")
    program()

    logfile.close()
    print(f"V Parsing completed.")

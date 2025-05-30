# Name: Nahyun Kim
# nahyun.kim.4@stonybrook.edu

from lexer import initLexer, getNextToken
from symbol_table import lookup_symbol_table, insert_symbol
import sys
import os

# ---------------- Helper Function ----------------------------------------
current_token = None

temp_counter = 0
rif_output = []
data_segment = []

def new_temp():
    global temp_counter
    name = f"T{temp_counter}"
    temp_counter += 1
    return name

float_temp_count = 0

def new_float_temp():
    global float_temp_count
    name = f"FT{float_temp_count}"
    float_temp_count += 1
    return name


def emit(op, arg1, arg2, result):
    rif_output.append(f"{op}, {arg1}, {arg2}, {result}")


def emit_data(dtype, count, name):
    data_segment.append(f"{dtype}, 0, {count}, {name}")

def emit_comment(comment):
    rif_output.append(f"# {comment}")

def condexpr_helper(result_temp, true_label, false_label):
    # OR 처리
    if lookahead() == "T_LPAREN":
        match("T_LPAREN")
        left, right, op = condexpr()
        match("T_RPAREN")
    elif lookahead() in ["T_Ident", "T_ICONST", "T_FCONST", "T_LPAREN", "T_MINUS"]:
        left = otherexpression()
        if lookahead() in ["T_LT", "T_LE", "T_GT", "T_GE", "T_EQ"]:
            op = lookahead()
            match(op)
            right = otherexpression()
            rif_op = {
                "T_LT": "blt", "T_LE": "ble", "T_GT": "bgt", "T_GE": "bge", "T_EQ": "beq"
            }[op]
            emit(rif_op, left, right, true_label)
        else:
            emit("bne", left, "0", true_label)

    if lookahead() == "T_OR":
        match("T_OR")
        emit("j", "0", "0", false_label)  # short-circuit 실패 시 false로
        emit(".label", "0", "0", false_label)
        condexpr_helper(result_temp, true_label, false_label)
    elif lookahead() == "T_AND":
        mid_label = new_label()
        emit("j", "0", "0", mid_label)  # if true, continue evaluating
        emit(".label", "0", "0", mid_label)
        match("T_AND")
        condexpr_helper(result_temp, true_label, false_label)
    else:
        emit("j", "0", "0", false_label)

def match(expected_type):
    global current_token
    if current_token.type == expected_type:
        # print("-------------Token :",current_token)
        current_token = getNextToken()
    else:
        print(f" ** Error: Expected {expected_type} but got {current_token.type}")
        sys.exit(1)

def lookahead():
    return current_token.type

# --------------------------------------------------------------------------

def program():
    production("Program => decllist funcdecls T_EOF")
    decllist()
    funcdecls()
    if lookahead() != "T_EOF":
        print(f" ** Error in program: Expected T_EOF but got {lookahead()}")
        sys.exit(1)

    output_path = os.path.join(output_dir, fname.rsplit(".", 1)[0] + ".rso")

    with open(output_path, "w") as f:
        f.write(".segment, 0, 0, .data\n")
        for line in data_segment:
            f.write(line + "\n")

        f.write(".segment, 0, 0, .text\n")
        for line in rif_output:
            f.write(line + "\n")

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

# def parmVar():
#     production("parmVar => ID parmVarTail")
#     match("T_Ident")
#     parmVarTail()
def parmVar():
    production("parmVar => ID parmVarTail")
    name = current_token.value
    match("T_Ident")

    # 🔸 심볼 테이블에 매개변수 추가
    insert_symbol(name, last_declared_type)

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
    
    # 저장할 타입 예: .int, .float
    if lookahead() == "T_INT":
        dtype = ".int"
    elif lookahead() == "T_FLOAT":
        dtype = ".float"
    else:
        print(f"** Error in decl(): unknown type {lookahead()}")
        sys.exit(1)

    typespec()
    variablelist(dtype)


def variablelist(dtype):
    production("variablelist => variable variablelisttail")
    variable(dtype)
    variablelisttail(dtype)


def variablelisttail(dtype):
    if lookahead() == "T_COMMA":
        match("T_COMMA")
        variable(dtype)
        variablelisttail(dtype)
    elif lookahead() == "T_SEMICOLON":
        match("T_SEMICOLON")
    else:
        print(f"** Error in variablelisttail: got {lookahead()}")
        sys.exit(1)

# def variable(dtype):
#     production("variable => ID variabletail")
#     name = current_token.value
#     match("T_Ident")
    
#     # 👇 타입 문자열 구분
#     type_str = "int" if dtype == ".int" else "float"
    
#     # 👇 Symbol Table에 삽입
#     insert_symbol(name, type_str)
    
#     # 👇 데이터 세그먼트로 출력
#     if lookahead() == "T_LBRACKET":
#         match("T_LBRACKET")
#         size = int(current_token.value)
#         match("T_ICONST")
#         match("T_RBRACKET")
#         emit_data(dtype, size, name)
#     else:
#         emit_data(dtype, 1, name)
def variable(dtype):
    production("variable => ID variabletail")
    name = current_token.value
    match("T_Ident")

    # 타입 문자열
    type_str = "int" if dtype == ".int" else "float"
    insert_symbol(name, type_str)

    # 배열 크기 계산
    total_size = variabletail()

    emit_data(dtype, total_size, name)

# def variabletail():
#     if lookahead() == "T_LBRACKET":
#         production("variabletail => LBRACKET ICONST RBRACKET variabletail")
#         match("T_LBRACKET")
#         match("T_ICONST")
#         match("T_RBRACKET")
#         variabletail()
#     else:
#         production("variabletail => e")
def variabletail():
    if lookahead() == "T_LBRACKET":
        production("variabletail => LBRACKET ICONST RBRACKET variabletail")
        match("T_LBRACKET")
        size = int(current_token.value)
        match("T_ICONST")
        match("T_RBRACKET")
        rest_size = variabletail()
        return size * rest_size
    else:
        production("variabletail => e")
        return 1  # 스칼라 변수


# def typespec():
#     if lookahead() == "T_INT":
#         production("typespec => INT")
#         match("T_INT")
#     elif lookahead() == "T_FLOAT":
#         production("typespec => FLOAT")
#         match("T_FLOAT")
#     else:
#         print(f"** Error in typespec: got {lookahead()}")
#         sys.exit(1)

last_declared_type = None  # 🔸 전역 선언 (parser.py 맨 위에서)

def typespec():
    global last_declared_type
    if lookahead() == "T_INT":
        production("typespec => INT")
        last_declared_type = "int"
        match("T_INT")
    elif lookahead() == "T_FLOAT":
        production("typespec => FLOAT")
        last_declared_type = "float"
        match("T_FLOAT")
    else:
        print(f"** Error in typespec: got {lookahead()}")
        sys.exit(1)

def usevariable():
    production("usevariable => ID usevariabletail")
    varname = current_token.value
    match("T_Ident")
    addr_temp = usevariabletail(varname)
    return addr_temp

def usevariabletail(varname):
    if lookahead() == "T_LBRACKET":
        production("usevariabletail => arraydim")
        return arraydim(varname)
    else:
        production("usevariabletail => e")
        addr_temp = new_temp()
        emit("la", addr_temp, 0, varname)
        return addr_temp

def arraydim(varname):
    match("T_LBRACKET")
    index_temp = otherexpression()  # ← 중요: expression으로 바꿔서 인덱스가 식일 수 있도록 함
    match("T_RBRACKET")

    # 주소 계산: base + (index * 4)
    offset_temp = new_temp()
    addr_temp = new_temp()
    base_temp = new_temp()

    emit("li", offset_temp, 0, "4")
    emit("mul", index_temp, offset_temp, offset_temp)
    emit("la", base_temp, 0, varname)
    emit("add", offset_temp, base_temp, addr_temp)

    # 다차원 배열일 경우 재귀 호출
    if lookahead() == "T_LBRACKET":
        return arraydimtail(addr_temp)
    else:
        return addr_temp

def arraydimtail(prev_addr_temp):
    match("T_LBRACKET")
    index_temp = otherexpression()
    match("T_RBRACKET")

    offset_temp = new_temp()
    new_addr_temp = new_temp()

    emit("li", offset_temp, 0, "4")
    emit("mul", index_temp, offset_temp, offset_temp)
    emit("add", prev_addr_temp, offset_temp, new_addr_temp)

    if lookahead() == "T_LBRACKET":
        return arraydimtail(new_addr_temp)
    else:
        return new_addr_temp

def statement():
    token = lookahead()

    if token == "T_WHILE":
        production("statement => whilestatement")
        emit_comment("Start WHILE statement ---")
        whilestatement()

    elif token == "T_IF":
        production("statement => ifstatement")
        emit_comment("Start IF statement ---")
        ifstatement()

    elif token == "T_Ident":
        production("statement => assignmentstatement")
        emit_comment("Start ASSIGN statement ---")
        assignmentstatement()

    elif token == "T_PRINT":
        production("statement => printstatement")
        emit_comment("Start PRINT statement ---")
        printstatement()

    elif token == "T_READ":
        production("statement => readstatement")
        emit_comment("Start READ statement ---")
        readstatement()

    elif token == "T_RETURN":
        production("statement => returnstatement")
        emit_comment("Start RETURN statement ---")
        returnstatement()

    elif token == "T_CALL":
        production("statement => callstatement")
        emit_comment("Start CALL statement ---")
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
   
    # 좌변 주소 계산
    addr_temp = usevariable()  # usevariable()은 이제 주소를 리턴해야 함
    match("T_ASSIGN")

    # 우변 값 계산
    value_temp = otherexpression()  # expression도 값을 계산해서 T# 리턴하게 해야 함

    # RIF 저장 코드 생성
    emit("sw", value_temp, 0, addr_temp)


def otherexpression():
    production("otherexpression => term otherexpressiontail")
    t1 = term()
    return otherexpressiontail(t1)

def otherexpressiontail(inherited_temp):
    if lookahead() == "T_PLUS":
        match("T_PLUS")
        t2 = term()
        result = new_temp()
        emit("add", inherited_temp, t2, result)
        return otherexpressiontail(result)
    elif lookahead() == "T_MINUS":
        match("T_MINUS")
        t2 = term()
        result = new_temp()
        emit("sub", inherited_temp, t2, result)
        return otherexpressiontail(result)
    else:
        production("otherexpressiontail => e")
        return inherited_temp

def term():
    production("term => factor termtail")
    f1 = factor()
    return termtail(f1)

def termtail(inherited_temp):
    if lookahead() == "T_MULT":
        match("T_MULT")
        f2 = factor()
        result = new_temp()
        emit("mul", inherited_temp, f2, result)
        return termtail(result)
    elif lookahead() == "T_DIV":
        match("T_DIV")
        f2 = factor()
        result = new_temp()
        emit("div", inherited_temp, f2, result)
        return termtail(result)
    else:
        return inherited_temp


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
        varname = current_token.value
        match("T_Ident")

        # lookahead()를 통해 factortail을 구분
        if lookahead() == "T_LBRACKET":
            # a[expr]
            match("T_LBRACKET")
            index_temp = otherexpression() 
            match("T_RBRACKET")

            offset_temp = new_temp()
            emit("li", offset_temp, 0, "4")

            offset_bytes = new_temp()
            emit("mul", index_temp, offset_temp, offset_bytes)

            base_temp = new_temp()
            emit("la", base_temp, 0, varname)

            final_addr = new_temp()
            emit("add", offset_bytes, base_temp, final_addr)

            result_temp = new_temp()
            emit("lw", result_temp, 0, final_addr)
            return result_temp

        elif lookahead() == "T_LPAREN":
            # 함수 호출: foo(expr)
            match("T_LPAREN")
            arglist()  # 내부에서 param emit 필요
            match("T_RPAREN")

            ret_temp = new_temp()
            emit("call", 0, ret_temp, varname)
            return ret_temp

        else:
            addr_temp = new_temp()
            emit("la", addr_temp, 0, varname)

            var_type = lookup_symbol_table(varname)

            if var_type == "float":
                val_temp = new_float_temp()
            else:
                val_temp = new_temp()

            emit("lw", val_temp, 0, addr_temp)
            return val_temp

    elif lookahead() == "T_ICONST":
        production("factor => ICONST")
        val = current_token.value
        match("T_ICONST")
        temp = new_temp()
        emit("li", temp, 0, val)
        return temp

    elif lookahead() == "T_FCONST":
        production("factor => FCONST")
        val = current_token.value
        match("T_FCONST")
        temp = new_float_temp()
        emit("li", temp, 0, val)  # FT#
        return temp

    elif lookahead() == "T_LPAREN":
        production("factor => LPAREN otherexpression RPAREN")
        match("T_LPAREN")
        result = otherexpression()
        match("T_RPAREN")
        return result

    elif lookahead() == "T_MINUS":
        production("factor => MINUS factor")
        match("T_MINUS")
        val_temp = factor()  # 재귀 호출
        result_temp = new_temp()
        emit("sub", "0", val_temp, result_temp)  # 0 - val
        return result_temp

    else:
        print(f"** Error in factor: got {lookahead()}")
        sys.exit(1)


# ----------- Helper Func -----------
label_count = 0

def new_label():
    global label_count
    name = f"L{label_count}"
    label_count += 1
    return name
# -----------------------------------


def whilestatement():
    production("whilestatement => WHILE relationalexpr bstatementlist")
    match("T_WHILE")
    label_body = new_label()
    label_cond = new_label()
    label_end = new_label()

    emit(".label", "0", "0", label_cond)

    match("T_LPAREN")
    left, right, op = condexpr()
    match("T_RPAREN")

    if right:  # 비교 연산
        # print("op in while statement ------------>",op)
        rif_op = {
            "T_LT": "blt", "T_LE": "ble",
            "T_GT": "bgt", "T_GE": "bge",
            "T_EQ": "beq"
        }[op]
        emit(rif_op, left, right, label_body)
    else:
        # 단순 조건값이 0이 아닌 경우 (e.g., while(x))
        emit("bne", left, "0", label_body)

    emit("j", "0", "0", label_end)

    emit(".label", "0", "0", label_body)
    match("T_LBRACE")
    statementlist()
    match("T_RBRACE")
    emit("j", "0", "0", label_cond)
    emit(".label", "0", "0", label_end)


def ifstatement():
    production("ifstatement => IF condexpr bstatementlist istail")
    match("T_IF")

    label_then = new_label()
    label_else = new_label()
    label_end = new_label()

    match("T_LPAREN")

    condexpr_helper("dummy", label_then, label_else)

    match("T_RPAREN")

    emit(".label", "0", "0", label_then)
    match("T_LBRACE")
    statementlist()
    match("T_RBRACE")
    emit("j", "0", "0", label_end)

    emit(".label", "0", "0", label_else)
    istail()

    emit(".label", "0", "0", label_end)


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
    left_label = new_label()
    end_label = new_label()
    result_temp = new_temp()

    condexpr_helper(result_temp, left_label, end_label)

    emit(".label", "0", "0", end_label)
    return (result_temp, None, None)


def condexprtail(left):
    if lookahead() in ["T_LT", "T_LE", "T_GT", "T_GE", "T_EQ"]:
        op = lookahead()
        match(op)
        right = otherexpression()

        # 비교 연산은 결과값을 사용하지 않고 직접 분기하기 때문에, left와 right만 리턴
        return (left, right, op)
    else:
        # 그냥 값 자체를 조건으로 쓰는 경우
        return (left, None, None)

def printstatement():
    production("printstatement => PRINT otherexpression")
    match("T_PRINT")
    value_temp = otherexpression()
    emit("syscall", "2", value_temp, "0")


def readstatement():
    production("readstatement => READ usevariable")
    match("T_READ")
    usevariable()

def returnstatement():
    match("T_RETURN")
    if lookahead() in ["T_Ident", "T_ICONST", "T_FCONST", "T_LPAREN", "T_MINUS"]:
        production("returnstatement => RETURN otherexpression")
        temp = otherexpression()
        emit("return", "0", "0", temp)
    else:
        production("returnstatement => RETURN")
        emit("return", "0", "0", "0")

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

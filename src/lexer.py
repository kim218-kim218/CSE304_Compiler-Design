# Name: Nahyun Kim
# nahyun.kim.4@stonybrook.edu


import re

# define TOKENS
TOKENS = {
    'T_SEMICOLON': r';',
    'T_LPAREN': r'\(',
    'T_RPAREN': r'\)',
    'T_COMMA': r',',
    'T_LBRACE': r'\{',
    'T_RBRACE': r'\}',
    'T_LBRACKET': r'\[',
    'T_RBRACKET': r'\]',
    'T_ASSIGN': r'=',
    'T_LT': r'<',
    'T_LE': r'<=',
    'T_GT': r'>',
    'T_GE': r'>=',
    'T_EQ': r'==',
    'T_NE': r'!=',
    'T_PLUS': r'\+',
    'T_MINUS': r'-',
    'T_MULT': r'\*',
    'T_DIV': r'/',
    'T_NOT': r'!',
    'T_AND': r'&&',
    'T_OR': r'\|\|',
    'T_IF': r'\bif\b',
    'T_ELSE': r'\belse\b',
    'T_WHILE': r'\bwhile\b',
    'T_INT': r'\bint\b',
    'T_FLOAT': r'\bfloat\b',
    'T_VOID': r'\bvoid\b',
    'T_CALL': r'\bcall\b',
    'T_PRINT': r'\bprint\b',
    'T_READ': r'\bread\b',
    'T_FUNCTION': r'\bfunction\b',
    'T_Ident': r'[a-zA-Z_][a-zA-Z_0-9]*',
    'T_ICONST': r'\b\d+\b',
    'T_FCONST': r'\b\d+\.\d+\b',
    'T_COMMENT': r'/\*.*?\*/'
}

# save source code
source_code = ""
current_index = 0

class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

    def __str__(self):
        return f"token: {self.type} : |{self.value}|"

# create buffer
def initLexer(filename):
    global source_code
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
        return 1
    except FileNotFoundError:
        return 0

# return next token
def getNextToken():
    global current_index
    
    # end of file
    if current_index >= len(source_code): 
        return Token("T_EOF", "")

    # skip comment
    comment_pattern = re.compile(TOKENS['T_COMMENT'])
    match = comment_pattern.match(source_code, current_index)
    if match:
        current_index = match.end()
        return getNextToken()
    
    # skip spaces
    if source_code[current_index].isspace():
        current_index += 1
        return getNextToken()

    # match token
    for token_type, pattern in TOKENS.items():
        rr = re.compile(pattern)
        match = rr.match(source_code, current_index)
        if match:
            current_index = match.end()
            return Token(token_type, match.group())

    current_index += 1
    return Token("UNKNOWN", source_code[current_index-1])

# 테스트용 메인 함수
if __name__ == "__main__":
    filename = input("Enter the filename: ")
    if initLexer(filename)==0:
        print("File not found.")
    else:
        while 1:
            token = getNextToken()
            print(token)
            if token.type == "T_EOF":
                break

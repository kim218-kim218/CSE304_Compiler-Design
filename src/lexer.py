# Name: Nahyun Kim
# nahyun.kim.4@stonybrook.edu

# Define TOKENS dict (정규식은 쓰지 않음, 이름만 매핑에 사용)
TOKENS = {
    'T_SEMICOLON': ';',
    'T_LPAREN': '(',
    'T_RPAREN': ')',
    'T_COMMA': ',',
    'T_LBRACE': '{',
    'T_RBRACE': '}',
    'T_LBRACKET': '[',
    'T_RBRACKET': ']',
    'T_ASSIGN': '=',
    'T_LT': '<',
    'T_LE': '<=',
    'T_GT': '>',
    'T_GE': '>=',
    'T_EQ': '==',
    'T_NE': '!=',
    'T_PLUS': '+',
    'T_MINUS': '-',
    'T_MULT': '*',
    'T_DIV': '/',
    'T_NOT': '!',
    'T_AND': '&&',
    'T_OR': '||',
    'T_IF': 'if',
    'T_ELSE': 'else',
    'T_WHILE': 'while',
    'T_INT': 'int',
    'T_FLOAT': 'float',
    'T_VOID': 'void',
    'T_CALL': 'call',
    'T_PRINT': 'print',
    'T_READ': 'read',
    'T_FUNCTION': 'function',
    'T_Ident': 'ID',         # 사용자 정의 식별자
    'T_ICONST': 'ICONST',    # 정수 상수
    'T_FCONST': 'FCONST',    # 실수 상수
    'T_COMMENT': '/* */'     # 주석 (스킵)
}

source_code = ""
current_index = 0

# 역방향 매핑: 문자열 → 토큰 이름
string_to_token = {v: k for k, v in TOKENS.items()}

class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

    def __str__(self):
        return f"token: {self.type} : |{self.value}|"

def initLexer(filename):
    global source_code
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
        return 1
    except FileNotFoundError:
        return 0

def getNextToken():
    global current_index, source_code
    length = len(source_code)

    # Skip whitespace
    while current_index < length and source_code[current_index].isspace():
        current_index += 1

    if current_index >= length:
        return Token("T_EOF", "")

    # Skip comments
    if source_code[current_index:current_index+2] == '/*':
        end = source_code.find('*/', current_index + 2)
        if end == -1:
            current_index = length
        else:
            current_index = end + 2
        return getNextToken()

    ch = source_code[current_index]

    # Identifier or keyword
    if ch.isalpha() or ch == '_':
        start = current_index
        while current_index < length and (source_code[current_index].isalnum() or source_code[current_index] == '_'):
            current_index += 1
        text = source_code[start:current_index]
        token_type = string_to_token.get(text, "T_Ident")
        return Token(token_type, text)

    # Number (int or float)
    if ch.isdigit():
        start = current_index
        while current_index < length and source_code[current_index].isdigit():
            current_index += 1
        if current_index < length and source_code[current_index] == '.':
            current_index += 1
            if current_index < length and source_code[current_index].isdigit():
                while current_index < length and source_code[current_index].isdigit():
                    current_index += 1
                return Token("T_FCONST", source_code[start:current_index])
            else:
                return Token("UNKNOWN", source_code[start:current_index])
        return Token("T_ICONST", source_code[start:current_index])

    # Multi-character operators
    two_char = source_code[current_index:current_index+2]
    if two_char in string_to_token:
        current_index += 2
        return Token(string_to_token[two_char], two_char)

    # Single-character operators
    if ch in string_to_token:
        current_index += 1
        return Token(string_to_token[ch], ch)

    # Unknown token
    current_index += 1
    return Token("UNKNOWN", ch)

# For test
if __name__ == "__main__":
    filename = input("Enter the filename: ")
    if initLexer(filename) == 0:
        print("File not found.")
    else:
        while True:
            token = getNextToken()
            print(token)
            if token.type == "T_EOF":
                break

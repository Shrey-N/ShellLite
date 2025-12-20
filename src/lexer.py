import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Token:
    type: str
    value: str
    line: int

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.current_char_index = 0
        self.line_number = 1
        self.indent_stack = [0]

    def tokenize(self) -> List[Token]:
        source = self._remove_multiline_comments(self.source_code)
        lines = source.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self.line_number = line_num
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                continue

            indent_level = len(line) - len(line.lstrip())
            if indent_level > self.indent_stack[-1]:
                self.indent_stack.append(indent_level)
                self.tokens.append(Token('INDENT', '', self.line_number))
            elif indent_level < self.indent_stack[-1]:
                while indent_level < self.indent_stack[-1]:
                    self.indent_stack.pop()
                    self.tokens.append(Token('DEDENT', '', self.line_number))
                if indent_level != self.indent_stack[-1]:
                    raise IndentationError(f"Unindent does not match any outer indentation level on line {self.line_number}")

            self.tokenize_line(stripped_line)
            self.tokens.append(Token('NEWLINE', '', self.line_number))

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token('DEDENT', '', self.line_number))
            
        self.tokens.append(Token('EOF', '', self.line_number))
        return self.tokens

    def _remove_multiline_comments(self, source: str) -> str:
        result = []
        i = 0
        while i < len(source):
            if source[i:i+2] == '/*':
                end = source.find('*/', i + 2)
                if end == -1:
                    raise SyntaxError("Unterminated multi-line comment")
                comment = source[i:end+2]
                result.append('\n' * comment.count('\n'))
                i = end + 2
            else:
                result.append(source[i])
                i += 1
        return ''.join(result)

    def tokenize_line(self, line: str):
        pos = 0
        while pos < len(line):
            match = None
            
            if line[pos].isspace():
                pos += 1
                continue

            if line[pos].isdigit():
                match = re.match(r'^\d+(\.\d+)?', line[pos:])
                if match:
                    value = match.group(0)
                    self.tokens.append(Token('NUMBER', value, self.line_number))
                    pos += len(value)
                    continue

            if line[pos] in ('"', "'"):
                quote_char = line[pos]
                end_quote = line.find(quote_char, pos + 1)
                if end_quote == -1:
                    raise SyntaxError(f"Unterminated string on line {self.line_number}")
                value = line[pos+1:end_quote]
                self.tokens.append(Token('STRING', value, self.line_number))
                pos = end_quote + 1
                continue

            if line[pos:pos+3] == '...':
                self.tokens.append(Token('DOTDOTDOT', '...', self.line_number))
                pos += 3
                continue

            two_char = line[pos:pos+2]
            two_char_tokens = {
                '=>': 'ARROW', '==': 'EQ', '!=': 'NEQ',
                '<=': 'LE', '>=': 'GE', '+=': 'PLUSEQ',
                '-=': 'MINUSEQ', '*=': 'MULEQ', '/=': 'DIVEQ',
                '%=': 'MODEQ'
            }
            if two_char in two_char_tokens:
                self.tokens.append(Token(two_char_tokens[two_char], two_char, self.line_number))
                pos += 2
                continue
            
            char = line[pos]
            single_char_tokens = {
                '+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV',
                '%': 'MOD', '=': 'ASSIGN', '>': 'GT', '<': 'LT',
                '?': 'QUESTION', '(': 'LPAREN', ')': 'RPAREN',
                '[': 'LBRACKET', ']': 'RBRACKET', ':': 'COLON',
                '{': 'LBRACE', '}': 'RBRACE', ',': 'COMMA', '.': 'DOT'
            }
            if char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, self.line_number))
                pos += 1
                continue

            if char.isalpha() or char == '_':
                match = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*', line[pos:])
                if match:
                    value = match.group(0)
                    keywords = {
                        'if': 'IF', 'else': 'ELSE', 'elif': 'ELIF',
                        'for': 'FOR', 'in': 'IN', 'range': 'RANGE',
                        'loop': 'LOOP', 'times': 'TIMES',
                        'while': 'WHILE', 'until': 'UNTIL',
                        'repeat': 'REPEAT', 'forever': 'FOREVER',
                        'stop': 'STOP', 'skip': 'SKIP', 'exit': 'EXIT',
                        'each': 'FOR',
                        'unless': 'UNLESS', 'when': 'WHEN', 'otherwise': 'OTHERWISE',
                        'then': 'THEN', 'do': 'DO',
                        'print': 'PRINT', 'say': 'SAY', 'show': 'SAY',
                        'input': 'INPUT', 'ask': 'ASK',
                        'to': 'TO', 'can': 'TO',
                        'return': 'RETURN', 'give': 'RETURN',
                        'fn': 'FN',
                        'structure': 'STRUCTURE', 'thing': 'STRUCTURE', 'class': 'STRUCTURE',
                        'has': 'HAS', 'with': 'WITH',
                        'is': 'IS', 'extends': 'EXTENDS', 'from': 'FROM',
                        'make': 'MAKE', 'new': 'MAKE',
                        'yes': 'YES', 'no': 'NO',
                        'true': 'YES', 'false': 'NO',
                        'const': 'CONST',
                        'and': 'AND', 'or': 'OR', 'not': 'NOT',
                        'try': 'TRY', 'catch': 'CATCH', 'always': 'ALWAYS',
                        'error': 'ERROR',
                        'use': 'USE', 'as': 'AS', 'share': 'SHARE',
                        'execute': 'EXECUTE', 'run': 'EXECUTE',
                    }
                    token_type = keywords.get(value, 'ID')
                    self.tokens.append(Token(token_type, value, self.line_number))
                    pos += len(value)
                    continue
            
            raise SyntaxError(f"Unexpected character '{char}' on line {self.line_number}")

import unittest
from lexer import Lexer, TokenType
from parser import Parser, Program, FunctionDecl, VarDecl, Assignment, BinOp

class TestFrontend(unittest.TestCase):

    def test_lexer_basic(self):
        code = "func main() { let x = 10; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            TokenType.FUNC, TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE,
            TokenType.LET, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, TokenType.SEMI,
            TokenType.RBRACE, TokenType.EOF
        ]
        self.assertEqual([t.type for t in tokens], expected)
        self.assertEqual(tokens[1].value, 'main')
        self.assertEqual(tokens[8].value, 10)

    def test_parser_arithmetic(self):
        code = "1 + 2 * 3;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse()
        stmt = program.statements[0]
        # Should be (1 + (2 * 3))
        self.assertIsInstance(stmt, BinOp)
        self.assertEqual(stmt.op, TokenType.PLUS)
        self.assertEqual(stmt.left.value, 1)
        self.assertEqual(stmt.right.op, TokenType.MUL)
        self.assertEqual(stmt.right.left.value, 2)
        self.assertEqual(stmt.right.right.value, 3)

    def test_parser_variable_decl(self):
        code = "let x = 10;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse()
        stmt = program.statements[0]
        self.assertIsInstance(stmt, VarDecl)
        self.assertEqual(stmt.name, 'x')
        self.assertEqual(stmt.value.value, 10)

    def test_parser_function_decl(self):
        code = "func add(a, b) { return a + b; }"
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse()
        func_decl = program.statements[0]
        self.assertIsInstance(func_decl, FunctionDecl)
        self.assertEqual(func_decl.name, 'add')
        self.assertEqual(func_decl.params, ['a', 'b'])
        
        body = func_decl.body
        self.assertEqual(len(body), 1)
        # Check return statement
        ret = body[0]
        self.assertEqual(ret.value.op, TokenType.PLUS)

    def test_assignment(self):
        code = "x = 5;"
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse()
        # My parser parses simple `ID = expr;` as Assignment
        stmt = program.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertEqual(stmt.name, 'x')
        self.assertEqual(stmt.value.value, 5)

if __name__ == '__main__':
    unittest.main()

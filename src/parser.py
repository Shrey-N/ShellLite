from typing import List, Optional
from .lexer import Token, Lexer
from .ast_nodes import *
import re

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset: int = 0) -> Token:
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return self.tokens[-1]

    def consume(self, expected_type: str = None) -> Token:
        token = self.peek()
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type} but got {token.type} on line {token.line}")
        self.pos += 1
        return token

    def check(self, token_type: str) -> bool:
        return self.peek().type == token_type

    def parse(self) -> List[Node]:
        statements = []
        while not self.check('EOF'):
            # Skip newlines at the top level between statements
            while self.check('NEWLINE'):
                self.consume()
                if self.check('EOF'): break
            
            if self.check('EOF'): break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    def parse_statement(self) -> Node:
        if self.check('USE'):
            return self.parse_import()
        elif self.check('CONST'):
            return self.parse_const()
        elif self.check('PRINT') or self.check('SAY'):
            return self.parse_print()
        elif self.check('IF'):
            return self.parse_if()
        elif self.check('UNLESS'):
            return self.parse_unless()
        elif self.check('WHILE'):
            return self.parse_while()
        elif self.check('UNTIL'):
            return self.parse_until()
        elif self.check('FOREVER'):
            return self.parse_forever()
        elif self.check('TRY'):
            return self.parse_try()
        elif self.check('FOR') or self.check('LOOP'):
            return self.parse_for()
        elif self.check('REPEAT'):
            return self.parse_repeat()
        elif self.check('WHEN'):
            return self.parse_when()
        elif self.check('TO'):
            return self.parse_function_def()
        elif self.check('STRUCTURE'):
            return self.parse_class_def()
        elif self.check('RETURN'):
            return self.parse_return()
        elif self.check('STOP'):
            return self.parse_stop()
        elif self.check('SKIP'):
            return self.parse_skip()
        elif self.check('EXIT'):
            return self.parse_exit()
        elif self.check('ERROR'):
            return self.parse_error()
        elif self.check('EXECUTE'):
            return self.parse_execute()
        elif self.check('MAKE'):
            return self.parse_make()
        elif self.check('ID'):
            return self.parse_id_start_statement()
        else:
            return self.parse_expression_stmt()

    def parse_const(self) -> ConstAssign:
        token = self.consume('CONST')
        name = self.consume('ID').value
        self.consume('ASSIGN')
        value = self.parse_expression()
        self.consume('NEWLINE')
        node = ConstAssign(name, value)
        node.line = token.line
        return node

    # --- New English-like statement parsers ---
    
    def parse_stop(self) -> Stop:
        """Parse: stop"""
        token = self.consume('STOP')
        self.consume('NEWLINE')
        node = Stop()
        node.line = token.line
        return node

    def parse_skip(self) -> Skip:
        """Parse: skip"""
        token = self.consume('SKIP')
        self.consume('NEWLINE')
        node = Skip()
        node.line = token.line
        return node

    def parse_error(self) -> Throw:
        """Parse: error 'message'"""
        token = self.consume('ERROR')
        message = self.parse_expression()
        self.consume('NEWLINE')
        node = Throw(message)
        node.line = token.line
        return node

    def parse_execute(self) -> Execute:
        """Parse: execute 'code string'"""
        token = self.consume('EXECUTE')
        code = self.parse_expression()
        self.consume('NEWLINE')
        node = Execute(code)
        node.line = token.line
        return node

    def parse_unless(self) -> Unless:
        """Parse: unless condition (body)"""
        token = self.consume('UNLESS')
        condition = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        
        self.consume('DEDENT')
        
        else_body = None
        if self.check('ELSE'):
            self.consume('ELSE')
            self.consume('NEWLINE')
            self.consume('INDENT')
            else_body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                else_body.append(self.parse_statement())
            self.consume('DEDENT')
        
        node = Unless(condition, body, else_body)
        node.line = token.line
        return node

    def parse_until(self) -> Until:
        """Parse: until condition (body)"""
        token = self.consume('UNTIL')
        condition = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        
        self.consume('DEDENT')
        node = Until(condition, body)
        node.line = token.line
        return node

    def parse_forever(self) -> Forever:
        """Parse: forever (body) - infinite loop"""
        token = self.consume('FOREVER')
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        
        self.consume('DEDENT')
        node = Forever(body)
        node.line = token.line
        return node

    def parse_exit(self) -> Exit:
        """Parse: exit or exit 1"""
        token = self.consume('EXIT')
        code = None
        if not self.check('NEWLINE'):
            code = self.parse_expression()
        self.consume('NEWLINE')
        node = Exit(code)
        node.line = token.line
        return node

    def parse_make(self) -> Node:
        """Parse: make Robot 'name' 100  or  new Robot 'name' 100"""
        token = self.consume('MAKE')
        class_name = self.consume('ID').value
        
        args = []
        while not self.check('NEWLINE') and not self.check('EOF'):
            args.append(self.parse_expression())
        
        self.consume('NEWLINE')
        node = Make(class_name, args)
        node.line = token.line
        return node

    def parse_repeat(self) -> Repeat:
        """Parse: repeat 5 times (body) or repeat (body)"""
        token = self.consume('REPEAT')
        
        # Check if there's a count
        if self.check('NEWLINE'):
            # Infinite loop style - but we'll require a count
            raise SyntaxError(f"repeat requires a count on line {token.line}")
        
        count = self.parse_expression()
        
        # Optional 'times' keyword
        if self.check('TIMES'):
            self.consume('TIMES')
        
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        
        self.consume('DEDENT')
        node = Repeat(count, body)
        node.line = token.line
        return node

    def parse_when(self) -> Node:
        """Parse: when value is x => (body) ... OR when condition (body)"""
        token = self.consume('WHEN')
        condition_or_value = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        # Check first statement in block to decide if Switch or If
        if self.check('IS'):
             # It's a Switch Statement
            cases = []
            otherwise = None
            
            # Loop for Switch cases
            while not self.check('DEDENT') and not self.check('EOF'):
                if self.check('IS'):
                    self.consume('IS')
                    match_val = self.parse_expression()
                    self.consume('NEWLINE')
                    self.consume('INDENT')
                    
                    case_body = []
                    while not self.check('DEDENT') and not self.check('EOF'):
                        while self.check('NEWLINE'): self.consume()
                        if self.check('DEDENT'): break
                        case_body.append(self.parse_statement())
                    self.consume('DEDENT')
                    
                    cases.append((match_val, case_body))
                    
                elif self.check('OTHERWISE'):
                    self.consume('OTHERWISE')
                    self.consume('NEWLINE')
                    self.consume('INDENT')
                    
                    otherwise = []
                    while not self.check('DEDENT') and not self.check('EOF'):
                        while self.check('NEWLINE'): self.consume()
                        if self.check('DEDENT'): break
                        otherwise.append(self.parse_statement())
                    self.consume('DEDENT')
                elif self.check('NEWLINE'):
                    self.consume('NEWLINE')
                else:
                    break
            
            self.consume('DEDENT')
            node = When(condition_or_value, cases, otherwise)
            node.line = token.line
            return node
            
        else:
            # It's an IF statement (when condition -> body)
            body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                body.append(self.parse_statement())
            
            self.consume('DEDENT')
            
            # Allow else/elif for 'when' too?
            else_body = None
            if self.check('ELSE'):
                self.consume('ELSE')
                self.consume('NEWLINE')
                self.consume('INDENT')
                else_body = []
                while not self.check('DEDENT') and not self.check('EOF'):
                    while self.check('NEWLINE'): self.consume()
                    if self.check('DEDENT'): break
                    else_body.append(self.parse_statement())
                self.consume('DEDENT')
                
            node = If(condition_or_value, body, else_body)
            node.line = token.line
            return node

    def parse_return(self) -> Return:
        token = self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('NEWLINE')
        node = Return(expr)
        node.line = token.line
        return node

    def parse_function_def(self) -> FunctionDef:
        start_token = self.consume('TO')
        name = self.consume('ID').value
        
        args = []
        # Parse args (space separated IDs until Newline or Indent? usually on same line)
        # Syntax: to greet name
        while self.check('ID'):
            arg_name = self.consume('ID').value
            default_val = None
            if self.check('ASSIGN'):
                self.consume('ASSIGN')
                default_val = self.parse_expression()
            args.append((arg_name, default_val))
            
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
            
        self.consume('DEDENT')
        node = FunctionDef(name, args, body)
        node.line = start_token.line
        return node

    def parse_class_def(self) -> ClassDef:
        start_token = self.consume('STRUCTURE')
        name = self.consume('ID').value
        
        parent = None
        if self.check('LPAREN'):
            self.consume('LPAREN')
            parent = self.consume('ID').value
            self.consume('RPAREN')
            
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        properties = []
        methods = []
        
        while not self.check('DEDENT') and not self.check('EOF'):
            if self.check('HAS'):
                self.consume()
                properties.append(self.consume('ID').value)
                self.consume('NEWLINE')
            elif self.check('TO'):
                methods.append(self.parse_function_def())
            elif self.check('NEWLINE'):
                self.consume()
            else:
                self.consume('DEDENT') # break out if unexpected
                break

        self.consume('DEDENT')
        node = ClassDef(name, properties, methods, parent)
        node.line = start_token.line
        return node
    
    def parse_id_start_statement(self) -> Node:
        """
        Handles statements starting with ID.
        1. Assignment: name = expr
        2. Instantiation: name is Model arg1 arg2
        3. Function Call: name arg1 arg2
        4. Method Call: name.method
        5. Property Access (Expression stmt): name.prop
        """
        name_token = self.consume('ID')
        name = name_token.value
        
        if self.check('ASSIGN'):
            self.consume('ASSIGN')
            value = self.parse_expression()
            self.consume('NEWLINE')
            node = Assign(name, value)
            node.line = name_token.line
            return node
            
        elif self.check('PLUSEQ'):
            self.consume('PLUSEQ')
            value = self.parse_expression()
            self.consume('NEWLINE')
            # Desugar a += 1 to a = a + 1
            node = Assign(name, BinOp(VarAccess(name), '+', value))
            node.line = name_token.line
            return node
            
        elif self.check('MINUSEQ'):
            self.consume('MINUSEQ')
            value = self.parse_expression()
            self.consume('NEWLINE')
            node = Assign(name, BinOp(VarAccess(name), '-', value))
            node.line = name_token.line
            return node
            
        elif self.check('MULEQ'):
            self.consume('MULEQ')
            value = self.parse_expression()
            self.consume('NEWLINE')
            node = Assign(name, BinOp(VarAccess(name), '*', value))
            node.line = name_token.line
            return node
            
        elif self.check('DIVEQ'):
            self.consume('DIVEQ')
            value = self.parse_expression()
            self.consume('NEWLINE')
            node = Assign(name, BinOp(VarAccess(name), '/', value))
            node.line = name_token.line
            return node
        
        elif self.check('IS'):
            # Instantiation: my_dog is Dog "Buddy"
            self.consume('IS')
            class_name = self.consume('ID').value
            args = []
            while not self.check('NEWLINE') and not self.check('EOF'):
                args.append(self.parse_expression()) 
            
            self.consume('NEWLINE')
            node = Instantiation(name, class_name, args)
            node.line = name_token.line
            return node
            
        elif self.check('DOT'):
            # Method call or property access (or assignment)
            self.consume('DOT')
            member = self.consume('ID').value
            
            if self.check('ASSIGN'):
                self.consume('ASSIGN')
                value = self.parse_expression()
                self.consume('NEWLINE')
                return PropertyAssign(name, member, value)
                
            args = []
            while not self.check('NEWLINE') and not self.check('EOF'):
                args.append(self.parse_expression())
            
            self.consume('NEWLINE')
            node = MethodCall(name, member, args)
            node.line = name_token.line
            return node

        else:
            if not self.check('NEWLINE') and not self.check('EOF') and not self.check('EQ') and not self.check('IS'):
                args = []
                while not self.check('NEWLINE') and not self.check('EOF') and not self.check('IS'): 
                     args.append(self.parse_expression())
                
                self.consume('NEWLINE')
                node = Call(name, args)
                node.line = name_token.line
                return node

            self.consume('NEWLINE')
            # Standalone variable/identifier -> Just access it (invokes auto-call if needed)
            # Do NOT wrap in Print (avoids printing None for void functions)
            node = VarAccess(name)
            node.line = name_token.line
            return node
    def parse_print(self) -> Print:
        if self.check('PRINT'):
            token = self.consume('PRINT')
        else:
            token = self.consume('SAY')
        expr = self.parse_expression()
        self.consume('NEWLINE')
        node = Print(expression=expr)
        node.line = token.line
        return node

    def parse_assign(self) -> Assign:
        name = self.consume('ID').value
        self.consume('ASSIGN')
        value = self.parse_expression()
        self.consume('NEWLINE')
        return Assign(name, value)

    def parse_import(self) -> Import:
        token = self.consume('USE')
        path = self.consume('STRING').value
        self.consume('NEWLINE')
        node = Import(path)
        node.line = token.line
        return node

    def parse_if(self) -> If:
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        
        self.consume('DEDENT')
        
        else_body = None
        
        # Handle ELIF (as recursive If in else_body? Or flat? Let's use recursive for simplicity with AST)
        # AST is If(cond, body, else_body).
        # ELIF cond body -> else_body = [If(cond, body, ...)]
        
        if self.check('ELIF'):
            # This 'elif' becomes the 'if' of the else_body
            # But wait, 'elif' token needs to be consumed inside the recursive call?
            # Or we recursively call parse_if but trick it?
            # Better: Rewrite parse_if to NOT consume IF if called recursively?
            # No, standard way:
            else_body = [self.parse_elif()]
            
        elif self.check('ELSE'):
            self.consume('ELSE')
            self.consume('NEWLINE')
            self.consume('INDENT')
            else_body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                else_body.append(self.parse_statement())
            self.consume('DEDENT')

        return If(condition, body, else_body)

    def parse_elif(self) -> If:
        # Similar to parse_if but consumes ELIF
        token = self.consume('ELIF')
        condition = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
        self.consume('DEDENT')
        
        else_body = None
        if self.check('ELIF'):
            else_body = [self.parse_elif()]
        elif self.check('ELSE'):
            self.consume('ELSE')
            self.consume('NEWLINE')
            self.consume('INDENT')
            else_body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                else_body.append(self.parse_statement())
            self.consume('DEDENT')
            
        node = If(condition, body, else_body)
        node.line = token.line
        node = If(condition, body, else_body)
        node.line = token.line
        return node

    def parse_while(self) -> While:
        start_token = self.consume('WHILE')
        condition = self.parse_expression()
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            body.append(self.parse_statement())
            
        self.consume('DEDENT')
        node = While(condition, body)
        node.line = start_token.line
        return node
        
    def parse_try(self) -> Try:
        start_token = self.consume('TRY')
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        try_body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            try_body.append(self.parse_statement())
        self.consume('DEDENT')
        
        self.consume('CATCH')
        catch_var = self.consume('ID').value
        self.consume('NEWLINE')
        self.consume('INDENT')
        
        catch_body = []
        while not self.check('DEDENT') and not self.check('EOF'):
            while self.check('NEWLINE'): self.consume()
            if self.check('DEDENT'): break
            catch_body.append(self.parse_statement())
        self.consume('DEDENT')
        
        # Check for always block (finally)
        always_body = []
        if self.check('ALWAYS'):
            self.consume('ALWAYS')
            self.consume('NEWLINE')
            self.consume('INDENT')
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                always_body.append(self.parse_statement())
            self.consume('DEDENT')
        
        if always_body:
            node = TryAlways(try_body, catch_var, catch_body, always_body)
        else:
            node = Try(try_body, catch_var, catch_body)
        node.line = start_token.line
        return node

    def parse_list(self) -> Node:
        token = self.consume('LBRACKET')
        
        # Empty list
        if self.check('RBRACKET'):
            self.consume('RBRACKET')
            node = ListVal([])
            node.line = token.line
            return node
        
        # Check for spread operator
        if self.check('DOTDOTDOT'):
            return self._parse_list_with_spread(token)
        
        # Parse first expression
        first_expr = self.parse_expression()
        
        # Check for list comprehension: [expr for var in iterable]
        if self.check('FOR'):
            self.consume('FOR')
            var_name = self.consume('ID').value
            self.consume('IN')
            iterable = self.parse_expression()
            
            # Optional condition: [x for x in list if x > 0]
            condition = None
            if self.check('IF'):
                self.consume('IF')
                condition = self.parse_expression()
            
            self.consume('RBRACKET')
            node = ListComprehension(first_expr, var_name, iterable, condition)
            node.line = token.line
            return node
        
        # Regular list
        elements = [first_expr]
        while self.check('COMMA'):
            self.consume('COMMA')
            if self.check('RBRACKET'):
                break  # Trailing comma support
            if self.check('DOTDOTDOT'):
                self.consume('DOTDOTDOT')
                spread_val = self.parse_expression()
                spread_node = Spread(spread_val)
                spread_node.line = token.line
                elements.append(spread_node)
            else:
                elements.append(self.parse_expression())
        
        self.consume('RBRACKET')
        node = ListVal(elements)
        node.line = token.line
        return node

    def _parse_list_with_spread(self, token: Token) -> ListVal:
        """Parse list starting with spread operator"""
        elements = []
        self.consume('DOTDOTDOT')
        spread_val = self.parse_expression()
        spread_node = Spread(spread_val)
        spread_node.line = token.line
        elements.append(spread_node)
        
        while self.check('COMMA'):
            self.consume('COMMA')
            if self.check('RBRACKET'):
                break
            if self.check('DOTDOTDOT'):
                self.consume('DOTDOTDOT')
                spread_val = self.parse_expression()
                spread_node = Spread(spread_val)
                spread_node.line = token.line
                elements.append(spread_node)
            else:
                elements.append(self.parse_expression())
        
        self.consume('RBRACKET')
        node = ListVal(elements)
        node.line = token.line
        return node

    def parse_dict(self) -> Dictionary:
        token = self.consume('LBRACE')
        pairs = []
        if not self.check('RBRACE'):
            key = self.parse_expression()
            self.consume('COLON')
            value = self.parse_expression()
            pairs.append((key, value))
            
            while self.check('COMMA'):
                self.consume('COMMA')
                key = self.parse_expression()
                self.consume('COLON')
                value = self.parse_expression()
                pairs.append((key, value))
        
        self.consume('RBRACE')
        node = Dictionary(pairs)
        node.line = token.line
        return node

    def parse_factor_simple(self) -> Node:
        """Parse a simple factor (atomic) to be used as an argument."""
        token = self.peek()
        if token.type == 'NUMBER':
            self.consume()
            val = token.value
            if '.' in val:
                node = Number(float(val))
            else:
                node = Number(int(val))
            node.line = token.line
            return node
        elif token.type == 'STRING':
            self.consume()
            val = token.value
            if '{' in val and '}' in val:
                parts = re.split(r'\{([^}]+)\}', val)
                if len(parts) == 1:
                     node = String(val)
                     node.line = token.line
                     return node
                current_node = None
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        if not part: continue 
                        expr = String(part)
                        expr.line = token.line
                    else:
                        expr = VarAccess(part.strip())
                        expr.line = token.line
                    if current_node is None:
                        current_node = expr
                    else:
                        current_node = BinOp(current_node, '+', expr)
                        current_node.line = token.line
                return current_node if current_node else String("")
            node = String(token.value)
            node.line = token.line
            return node
        elif token.type == 'YES':
            self.consume()
            node = Boolean(True)
            node.line = token.line
            return node
        elif token.type == 'NO':
            self.consume()
            node = Boolean(False)
            node.line = token.line
            return node
        elif token.type == 'LBRACKET':
            return self.parse_list()
        elif token.type == 'LBRACE':
            return self.parse_dict()
        elif token.type == 'ID':
            self.consume()
            # Dont check for args here, just VarAccess or Dot
            if self.check('DOT'):
                self.consume('DOT')
                prop = self.consume('ID').value
                node = PropertyAccess(token.value, prop)
                node.line = token.line
                return node
            node = VarAccess(token.value)
            node.line = token.line
            return node
        elif token.type == 'LPAREN':
            self.consume()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        elif token.type == 'INPUT' or token.type == 'ASK':
            self.consume()
            prompt = None
            if self.check('STRING'):
                prompt = self.consume('STRING').value
            node = Input(prompt)
            node.line = token.line
            return node
        
        raise SyntaxError(f"Unexpected argument token {token.type} at line {token.line}")

    def parse_factor(self) -> Node:
        token = self.peek()
        
        if token.type == 'NOT':
            op = self.consume()
            right = self.parse_factor() # Recursive for not not x
            node = UnaryOp(op.value, right)
            node.line = op.line
            return node
            
        if token.type == 'NUMBER':
            self.consume()
            val = token.value
            if '.' in val:
                node = Number(float(val))
            else:
                node = Number(int(val))
            node.line = token.line
            return node
        elif token.type == 'STRING':
            self.consume()
            node = String(token.value)
            node.line = token.line
            return node
        elif token.type == 'YES':
            self.consume()
            node = Boolean(True)
            node.line = token.line
            return node
        elif token.type == 'NO':
            self.consume()
            node = Boolean(False)
            node.line = token.line
            return node
        elif token.type == 'LBRACKET':
            return self.parse_list()
        elif token.type == 'LBRACE':
            return self.parse_dict()
        elif token.type == 'ID':
            self.consume()
            instance_name = token.value
            method_name = None
            
            # Check for dot access in expression
            if self.check('DOT'):
                self.consume('DOT')
                method_name = self.consume('ID').value
            
            # Check for Function Call arguments (Haskell-style: func arg1 arg2)
            # Args must be simple factors (Number, String, Id, Paren)
            # This allows 'double 10' to work in expressions
            args = []
            force_call = False
            
            while True:
                next_t = self.peek()
                
                # Check for explicit empty call ()
                if next_t.type == 'LPAREN' and self.peek(1).type == 'RPAREN':
                    self.consume('LPAREN')
                    self.consume('RPAREN')
                    force_call = True
                    # Treat () as end of args or just an empty arg marker? 
                    # If we write func() 1, is it func(1)? Or func() then 1?
                    # For safety, let's treat () as a valid 'call trigger' and continue specific args if needed, 
                    # but typically () means 0 args.
                    continue

                if next_t.type in ('NUMBER', 'STRING', 'ID', 'LPAREN', 'INPUT', 'ASK', 'YES', 'NO', 'LBRACKET', 'LBRACE'):
                     args.append(self.parse_factor_simple())
                else:
                    break
                    
            if method_name:
                if args or force_call:
                    node = MethodCall(instance_name, method_name, args)
                else:
                    node = PropertyAccess(instance_name, method_name)
                node.line = token.line
                return node
            
            if args or force_call:
                node = Call(instance_name, args)
                node.line = token.line
                return node
                
            node = VarAccess(instance_name)
            node.line = token.line
            return node
        elif token.type == 'LPAREN':
            self.consume()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        elif token.type == 'INPUT' or token.type == 'ASK':
            self.consume()
            prompt = None
            if self.check('STRING'):
                prompt = self.consume('STRING').value
            node = Input(prompt)
            node.line = token.line
            return node
        
        raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def parse_for(self) -> Node:
        # Support:
        # 1. for x in list       -> ForIn loop
        # 2. for i in range 1 10 -> For loop with range
        # 3. for 20 in range     -> For loop (old style)
        # 4. loop 20 times       -> For loop
        
        if self.check('LOOP'):
            # loop N times
            start_token = self.consume('LOOP')
            count_expr = self.parse_expression()
            self.consume('TIMES')
            
            self.consume('NEWLINE')
            self.consume('INDENT')
            
            body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                body.append(self.parse_statement())

            self.consume('DEDENT')
            node = For(count_expr, body)
            node.line = start_token.line
            return node
        
        # for ...
        start_token = self.consume('FOR')
        
        # Check if it's: for VAR in ITERABLE (where VAR is an ID followed by IN)
        if self.check('ID') and self.peek(1).type == 'IN':
            var_name = self.consume('ID').value
            self.consume('IN')
            
            # Check if it's range syntax: for i in range 1 10
            if self.check('RANGE'):
                self.consume('RANGE')
                start_val = self.parse_expression()
                end_val = self.parse_expression()
                
                self.consume('NEWLINE')
                self.consume('INDENT')
                
                body = []
                while not self.check('DEDENT') and not self.check('EOF'):
                    while self.check('NEWLINE'): self.consume()
                    if self.check('DEDENT'): break
                    body.append(self.parse_statement())
                
                self.consume('DEDENT')
                
                # Create ForIn with a range call
                iterable = Call('range', [start_val, end_val])
                node = ForIn(var_name, iterable, body)
                node.line = start_token.line
                return node
            else:
                # for x in iterable
                iterable = self.parse_expression()
                
                self.consume('NEWLINE')
                self.consume('INDENT')
                
                body = []
                while not self.check('DEDENT') and not self.check('EOF'):
                    while self.check('NEWLINE'): self.consume()
                    if self.check('DEDENT'): break
                    body.append(self.parse_statement())
                
                self.consume('DEDENT')
                node = ForIn(var_name, iterable, body)
                node.line = start_token.line
                return node
        else:
            # Old style: for 20 in range (count-based)
            count_expr = self.parse_expression()
            self.consume('IN')
            self.consume('RANGE')
            
            self.consume('NEWLINE')
            self.consume('INDENT')
            
            body = []
            while not self.check('DEDENT') and not self.check('EOF'):
                while self.check('NEWLINE'): self.consume()
                if self.check('DEDENT'): break
                body.append(self.parse_statement())

            self.consume('DEDENT')
            node = For(count_expr, body)
            node.line = start_token.line
            return node

    def parse_expression_stmt(self) -> Node:
        # Implicit print for top-level expressions
        expr = self.parse_expression()
        self.consume('NEWLINE')
        # Wrap in Print node for implicit output behavior
        node = Print(expression=expr)
        node.line = expr.line
        return node

    def parse_expression(self) -> Node:
        # Check for lambda: fn x => expr or fn x y => expr
        if self.check('FN'):
            return self.parse_lambda()
        
        return self.parse_ternary()

    def parse_lambda(self) -> Lambda:
        token = self.consume('FN')
        params = []
        
        # Parse parameters until =>
        while self.check('ID'):
            params.append(self.consume('ID').value)
        
        self.consume('ARROW')
        body = self.parse_expression()
        
        node = Lambda(params, body)
        node.line = token.line
        return node

    def parse_ternary(self) -> Node:
        # condition ? true_expr : false_expr
        condition = self.parse_logic_or()
        
        if self.check('QUESTION'):
            self.consume('QUESTION')
            true_expr = self.parse_expression()
            self.consume('COLON')
            false_expr = self.parse_expression()
            node = Ternary(condition, true_expr, false_expr)
            node.line = condition.line
            return node
        
        return condition

    def parse_logic_or(self) -> Node:
        left = self.parse_logic_and()
        
        while self.check('OR'):
            op_token = self.consume()
            right = self.parse_logic_and()
            new_node = BinOp(left, op_token.value, right)
            new_node.line = op_token.line
            left = new_node
            
        return left

    def parse_logic_and(self) -> Node:
        left = self.parse_comparison()
        
        while self.check('AND'):
            op_token = self.consume()
            right = self.parse_comparison()
            new_node = BinOp(left, op_token.value, right)
            new_node.line = op_token.line
            left = new_node
            
        return left

    def parse_comparison(self) -> Node:
        # Simple binary operators handling
        # precedence: ==, !=, <, >, <=, >=, is
        left = self.parse_arithmetic()
        
        if self.peek().type in ('EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE', 'IS'):
            op_token = self.consume()
            op_val = op_token.value
            if op_token.type == 'IS':
                op_val = '==' # Treat 'is' as equality
                
            right = self.parse_arithmetic()
            node = BinOp(left, op_val, right)
            node.line = op_token.line
            return node
            
        return left

    def parse_arithmetic(self) -> Node:
        # precedence: +, -
        left = self.parse_term()
        
        while self.peek().type in ('PLUS', 'MINUS'):
            op_token = self.consume()
            right = self.parse_term()
            new_node = BinOp(left, op_token.value, right)
            new_node.line = op_token.line
            left = new_node
            
        return left

    def parse_term(self) -> Node:
        # precedence: *, /, %
        left = self.parse_factor()
        
        while self.peek().type in ('MUL', 'DIV', 'MOD'):
            op_token = self.consume()
            right = self.parse_factor()
            new_node = BinOp(left, op_token.value, right)
            new_node.line = op_token.line
            left = new_node
            
        return left



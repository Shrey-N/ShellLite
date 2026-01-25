from dataclasses import dataclass, field
from typing import List, Optional, Any, Callable
from .lexer import Token
from .ast_nodes import *

@dataclass
class GeoNode:
    """Represents a topological node in the source code geometry."""
    head_token: Token
    line: int
    indent_level: int
    tokens: List[Token] = field(default_factory=list)
    children: List['GeoNode'] = field(default_factory=list)
    parent: Optional['GeoNode'] = None

    def __repr__(self):
        return f"GeoNode(line={self.line}, indent={self.indent_level}, head={self.head_token.type})"

class GeometricBindingParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != 'COMMENT']  # Should keep NEWLINE/INDENT/DEDENT for context? 
        # Actually GBP relies on Tokens having indentation info or distinct INDENT/DEDENT tokens.
        # The lexer produces INDENT/DEDENT tokens. We can use those OR just check column.
        # Let's rely on the existing Lexer's INDENT/DEDENT tokens for safety, 
        # BUT we will map them to a tree structure linearly.
        self.root_nodes: List[GeoNode] = []
        
        # Precedence Table for Iterative Expression Parser
        self.precedence = {
            'OR': 1, 'AND': 2, 'NOT': 3,
            'EQ': 4, 'NEQ': 4, 'LT': 5, 'GT': 5, 'LE': 5, 'GE': 5, 'IS': 5,
            'PLUS': 6, 'MINUS': 6,
            'MUL': 7, 'DIV': 7, 'MOD': 7,
            'POW': 8,
            'DOT': 9, 'LPAREN': 10, 'LBRACKET': 10
        }

    def parse(self) -> List[Node]:
        """Main entry point."""
        # Phase 1 & 2: Topography Scan and Link
        self.topology_scan()
        
        # Phase 3: Binder
        ast_nodes = []
        for geo_node in self.root_nodes:
            ast_node = self.bind_node(geo_node)
            if ast_node:
                ast_nodes.append(ast_node)
        return ast_nodes

    def topology_scan(self):
        """
        Phase 1: Scans tokens to build GeoNodes.
        Phase 2: Links them into a tree based on nesting.
        """
        # We need to reconstruct lines first because tokens are a flat stream.
        # But wait, Lexer gives INDENT/DEDENT.
        # Strategy:
        # Iterate tokens. 
        # New "Block" starts when INDENT is found? 
        # Actually, in GBP, every "Statement" is a node.
        # Indentation determines parent/child.
        
        # Step 1: Group tokens into logical lines (Statements)
        # We split by NEWLINE.
        logical_lines = []
        current_line_tokens = []
        
        for token in self.tokens:
            if token.type == 'NEWLINE':
                if current_line_tokens:
                    logical_lines.append(current_line_tokens)
                current_line_tokens = []
            elif token.type in ('INDENT', 'DEDENT', 'EOF'):
                # These are structural markers. We can use them or ignore them if we calculate indentation manually?
                # The Lexer's INDENT/DEDENT are reliable.
                # Let's preserve them in the stream if needed, 
                # OR use them to track current 'active parent'.
                pass # logic handled below in a smarter way?
            else:
                current_line_tokens.append(token)
        
        if current_line_tokens:
             logical_lines.append(current_line_tokens)

        # Step 2: Build GeoNodes and Link
        # We use a stack of [ (indent_level, GeoNode) ] to track parents.
        # Root is level 0.
        
        # This is strictly for "Block Parents".
        # But wait, `if x:` is a parent. `x = 1` is a leaf.
        # How do we know indentation of a logical line?
        # We look at the first token's column? Or Lexer's INDENT tokens?
        # The Lexer FLATTENS indentation into tokens.
        # So we should actually process the raw token stream with INDENTs.
        
        node_stack: List[GeoNode] = [] # The active parents
        
        # We need a Dummy Root? 
        # Or just append to self.root_nodes if stack is empty.

        current_tokens_accumulator = []
        
        # Improved Algo: Linear Token Walk with Stack
        # We will create a "Current Node" when we encounter non-structural tokens.
        # When we hit NEWLINE, we finalize that node.
        # When we hit INDENT, the last node becomes a parent for future nodes.
        # When we hit DEDENT, we pop the parent.
        
        # Problem: `if x:` -> NEWLINE -> INDENT.
        # The `if x:` node must be created before INDENT.
        
        # Let's iterate.
        current_node: Optional[GeoNode] = None
        
        # Stack tracks the *Block Containers*.
        # List of (Node, explicit_indent_flag)
        block_stack: List[GeoNode] = [] 
        
        for token in self.tokens:
            if token.type == 'EOF':
                break
                
            if token.type == 'INDENT':
                # The PREVIOUS node is now a parent block.
                if current_node:
                     block_stack.append(current_node)
                     current_node = None # We are stepping "inside", so no current line active node yet
                continue
                
            if token.type == 'DEDENT':
                 if block_stack:
                     block_stack.pop()
                 continue
            
            if token.type == 'NEWLINE':
                # End of specific statement line.
                current_node = None
                continue
            
            # Normal Token
            if current_node is None:
                # START of a new logical line -> New GeoNode
                current_node = GeoNode(
                    head_token=token,
                    line=token.line,
                    indent_level=len(block_stack), # Logical depth
                    tokens=[token] # Start collecting tokens
                )
                
                # Link to parent immediately
                if block_stack:
                    parent = block_stack[-1]
                    parent.children.append(current_node)
                    current_node.parent = parent
                else:
                    self.root_nodes.append(current_node)
            else:
                # Accumulate tokens for the current line
                current_node.tokens.append(token)

    def bind_node(self, node: GeoNode) -> Node:
        """Phase 2: Semantic Binding Dispatcher."""
        head_type = node.head_token.type
        
        if head_type == 'IF':
            return self.bind_if(node)
        elif head_type == 'WHILE':
            return self.bind_while(node)
        elif head_type == 'FOR' or head_type == 'LOOP':
            return self.bind_for(node)
        elif head_type == 'FUNCTION' or head_type == 'TO' or (head_type == 'DEFINE' and self.peek_type(node, 1) == 'FUNCTION'):
             return self.bind_func(node)
        elif head_type == 'PRINT' or head_type == 'SAY':
            return self.bind_print(node)
        elif head_type == 'RETURN':
            return self.bind_return(node)
        elif head_type == 'REPEAT':
            return self.bind_repeat(node)
        elif head_type == 'ID':
            # Check for assignment or function call
            # We can scan the node's tokens.
            if any(t.type == 'ASSIGN' for t in node.tokens):
                return self.bind_assignment(node)
            return self.bind_expression_stmt(node)
        else:
            return self.bind_expression_stmt(node)

    def peek_type(self, node: GeoNode, offset: int) -> str:
        if offset < len(node.tokens):
            return node.tokens[offset].type
        return ""

    # --- Binders ---

    def bind_if(self, node: GeoNode) -> If:
        # Syntax: if <expr>
        # Body is in node.children
        # Checks for 'else' block? 
        # In GBP, 'else' would be a SIBLING node following this one.
        # Handled by looking ahead in the parent list? 
        # Complication: bind_node processes one at a time.
        # Solution: We might need to iterate root_nodes manually in 'parse' to handle 'else' chaining.
        # But for simplicity V1: strictly nested 'else' is not standard python style.
        # Python style: else is at same indent.
        # So 'else' is a sibling.
        
        # Extract expression tokens: from index 1 to end (excluding colon if present)
        expr_tokens = self._extract_expr_tokens(node.tokens, start=1)
        condition = self.parse_expr_iterative(expr_tokens)
        
        body = [self.bind_node(child) for child in node.children]
        
        # Check for Else in siblings? 
        # The parent list has this node. The next node might be 'ELSE'.
        # This requires access to the parent's children list.
        else_body = None
        
        # Look ahead for ELSE
        # A bit hacky given the current isolation, but feasible if we modify the main loop
        # or just assume Else is handled as a separate statement? 
        # If 'Else' is a separate statement, it needs to link back to the previous If.
        # But AST structure requires If(cond, body, else_body).
        # We will handle ELSE during the binding of the blocks, or we leave it for V2.
        # For now, let's assume no ELSE or implement a simple check in 'bind_node' loop?
        # Actually, let's implement the `If` properly later.
        
        return If(condition, body, else_body)

    def bind_while(self, node: GeoNode) -> While:
        expr_tokens = self._extract_expr_tokens(node.tokens, start=1)
        condition = self.parse_expr_iterative(expr_tokens)
        body = [self.bind_node(child) for child in node.children]
        return While(condition, body)
        
    def bind_repeat(self, node: GeoNode) -> Repeat:
        # repeat 5 times
        expr_tokens = self._extract_expr_tokens(node.tokens, start=1)
        # remove 'times' if present at end
        if expr_tokens and expr_tokens[-1].type == 'TIMES':
            expr_tokens.pop()
            
        count = self.parse_expr_iterative(expr_tokens)
        body = [self.bind_node(child) for child in node.children]
        return Repeat(count, body)

    def bind_print(self, node: GeoNode) -> Print:
        expr_tokens = self._extract_expr_tokens(node.tokens, start=1)
        expr = self.parse_expr_iterative(expr_tokens)
        return Print(expr)
        
    def bind_return(self, node: GeoNode) -> Return:
        expr_tokens = self._extract_expr_tokens(node.tokens, start=1)
        expr = self.parse_expr_iterative(expr_tokens)
        return Return(expr)

    def bind_assignment(self, node: GeoNode) -> Assign:
        # ID = Expr
        # Find index of ASSIGN
        assign_idx = -1
        for i, t in enumerate(node.tokens):
            if t.type == 'ASSIGN':
                assign_idx = i
                break
        
        name = node.tokens[0].value # Simplification: Assume simple ID assignment
        expr_tokens = node.tokens[assign_idx+1:]
        value = self.parse_expr_iterative(expr_tokens)
        return Assign(name, value)

    def bind_expression_stmt(self, node: GeoNode) -> Any:
        # Just an expression
        return self.parse_expr_iterative(node.tokens)

    def bind_func(self, node: GeoNode) -> FunctionDef:
        # to name arg1 arg2
        # or define function name ...
        start = 1
        if node.tokens[0].type == 'DEFINE': start = 2
        
        name = node.tokens[start].value
        args = []
        # Parse args (simple tokens for now)
        for t in node.tokens[start+1:]:
             if t.type == 'ID':
                 args.append((t.value, None, None))
             elif t.type == 'COLON': break # End of signature
        
        body = [self.bind_node(child) for child in node.children]
        return FunctionDef(name, args, body)

    # --- Utilities ---

    def _extract_expr_tokens(self, tokens: List[Token], start: int = 0) -> List[Token]:
        end = len(tokens)
        if tokens[-1].type == 'COLON':
            end -= 1
        return tokens[start:end]

    # --- Phase 3: Iterative Expression Parser ---
    
    def parse_expr_iterative(self, tokens: List[Token]) -> Node:
        """
        Shunting-yard variant to produce AST directly.
        Two stacks: 
        1. values: [Node]
        2. ops: [Token (operator)]
        """
        if not tokens: return None
        
        values: List[Node] = []
        ops: List[str] = []
        
        def apply_op():
            if not ops: return
            op_type = ops.pop()
            
            # Binary Ops
            if len(values) >= 2:
                right = values.pop()
                left = values.pop()
                
                op_map = {
                    'PLUS': '+', 'MINUS': '-', 'MUL': '*', 'DIV': '/', 'MOD': '%',
                    'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=', 'EQ': '==', 'NEQ': '!=',
                    'AND': 'and', 'OR': 'or'
                }
                
                op_str = op_map.get(op_type, op_type)
                values.append(BinOp(left, op_str, right))
            # Unary ops TODO (not, -)
        
        def precedence(op_type):
            return self.precedence.get(op_type, 0)
            
        i = 0
        while i < len(tokens):
            t = tokens[i]
            
            if t.type == 'NUMBER':
                values.append(Number(int(t.value) if '.' not in t.value else float(t.value)))
            elif t.type == 'STRING':
                values.append(String(t.value))
            elif t.type == 'ID':
                # Check for call? Next token LPAREN
                if i+1 < len(tokens) and tokens[i+1].type == 'LPAREN':
                    # Handle Call - Simplification: consume tokens until RPAREN recursion or iteratively?
                    # For V1 GBP, let's just make ID a var.
                    values.append(VarAccess(t.value))
                else:
                    values.append(VarAccess(t.value))
            elif t.type == 'LPAREN':
                ops.append('LPAREN')
            elif t.type == 'RPAREN':
                while ops and ops[-1] != 'LPAREN':
                    apply_op()
                if ops: ops.pop() # Pop LPAREN
            elif t.type in self.precedence:
                while (ops and ops[-1] != 'LPAREN' and 
                       precedence(ops[-1]) >= precedence(t.type)):
                    apply_op()
                ops.append(t.type)
            
            i += 1
            
        while ops:
            apply_op()
            
        return values[0] if values else None

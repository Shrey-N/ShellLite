from dataclasses import dataclass, field
from typing import Any, List, Optional

@dataclass
class Node:
    line: int = field(default=0, init=False)

@dataclass
class Number(Node):
    value: int

@dataclass
class String(Node):
    value: str

@dataclass
class VarAccess(Node):
    name: str

@dataclass
class Assign(Node):
    name: str # variable name
    value: Node

@dataclass
class PropertyAssign(Node):
    instance_name: str
    property_name: str
    value: Node

@dataclass
class UnaryOp(Node):
    op: str
    right: Node

@dataclass
class BinOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class Print(Node):
    expression: Node

@dataclass
class If(Node):
    condition: Node
    body: List[Node]
    else_body: Optional[List[Node]] = None

@dataclass
class While(Node):
    condition: Node
    body: List[Node]

@dataclass
class For(Node):
    count: Node
    body: List[Node]

@dataclass
class ListVal(Node):
    elements: List[Node]

@dataclass
class Dictionary(Node):
    pairs: List[tuple[Node, Node]]

@dataclass
class Boolean(Node):
    value: bool

@dataclass
class Input(Node):
    prompt: Optional[str] = None

@dataclass
class FunctionDef(Node):
    name: str
    args: List[tuple[str, Optional[Node]]] # [(name, default_node), ...]
    body: List[Node]

@dataclass
class Call(Node):
    name: str
    args: List[Node]

@dataclass
class Return(Node):
    value: Node

@dataclass
class ClassDef(Node):
    name: str
    properties: List[str]
    methods: List[FunctionDef]
    parent: Optional[str] = None

@dataclass
class Instantiation(Node):
    var_name: str
    class_name: str
    args: List[Node]

@dataclass
class MethodCall(Node):
    instance_name: str
    method_name: str
    args: List[Node]

@dataclass
class PropertyAccess(Node):
    instance_name: str
    property_name: str

@dataclass
class Import(Node):
    path: str

@dataclass
class Try(Node):
    try_body: List[Node]
    catch_var: str
    catch_body: List[Node]

@dataclass
class Lambda(Node):
    params: List[str]
    body: Node  # Single expression

@dataclass
class Ternary(Node):
    condition: Node
    true_expr: Node
    false_expr: Node

@dataclass
class ListComprehension(Node):
    expr: Node
    var_name: str
    iterable: Node
    condition: Optional[Node] = None

@dataclass
class Spread(Node):
    value: Node

@dataclass
class ConstAssign(Node):
    name: str
    value: Node

@dataclass
class ForIn(Node):
    var_name: str
    iterable: Node
    body: List[Node]

@dataclass
class IndexAccess(Node):
    obj: Node
    index: Node

@dataclass
class Stop(Node):
    """Break out of loop"""
    pass

@dataclass
class Skip(Node):
    """Continue to next iteration"""
    pass

@dataclass
class When(Node):
    """Pattern matching - when x is value1 => ... otherwise => ..."""
    value: Node
    cases: List[tuple[Node, List[Node]]]  # [(match_value, body), ...]
    otherwise: Optional[List[Node]] = None

@dataclass
class Throw(Node):
    """Throw an error - error 'message'"""
    message: Node

@dataclass
class TryAlways(Node):
    """Try with always block - try ... catch ... always ..."""
    try_body: List[Node]
    catch_var: str
    catch_body: List[Node]
    always_body: List[Node]

@dataclass
class Unless(Node):
    """Negative if - unless condition"""
    condition: Node
    body: List[Node]
    else_body: Optional[List[Node]] = None

@dataclass
class Execute(Node):
    """Execute code from string - execute 'say hello'"""
    code: Node

@dataclass
class Repeat(Node):
    """Simple repeat loop - repeat 5 times"""
    count: Node
    body: List[Node]

@dataclass
class ImportAs(Node):
    """Import with alias - use 'math' as m"""
    path: str
    alias: str

@dataclass
class Until(Node):
    """Loop until condition - until done"""
    condition: Node
    body: List[Node]

@dataclass
class Forever(Node):
    """Infinite loop - forever"""
    body: List[Node]

@dataclass
class Exit(Node):
    """Exit program - exit or exit 1"""
    code: Optional[Node] = None

@dataclass  
class Make(Node):
    """Create object - make Robot or new Robot"""
    class_name: str
    args: List[Node]

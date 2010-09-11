


'''# comment
a = 0
b = [1, 2, 3]
for x in b:
    pass

'''


import lucylexer
import lucyast
import ply.yacc as yacc
from compiler import ast
from compiler.consts import *

tokens = lucylexer.tokens


# AST
class Node(object):
    def __init__(self, type, children=None, leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
	 
    def __repr__(self):
        return "Node(%s, %r)"%(self.type, self.leaf)


binary_ops = {
    # operators
    "+": lucyast.Add,
    "-": lucyast.Sub,
    "*": lucyast.Mul,
    "/": lucyast.Div,
    "%": lucyast.Mod,
    "<<": lucyast.LeftShift,
    ">>": lucyast.RightShift,
    "&": lucyast.Bitand,
    "^": lucyast.Bitxor,
    "|": lucyast.Bitor,
    # augmented assigns
    "+=": lucyast.AugAssign,
    "-=": lucyast.AugAssign,
    "*=": lucyast.AugAssign,
    "**=": lucyast.AugAssign,
    "/=": lucyast.AugAssign,
    "%=": lucyast.AugAssign,
    "<<=": lucyast.AugAssign,
    ">>=": lucyast.AugAssign,
    "&=": lucyast.AugAssign,
    "^=": lucyast.AugAssign,
    "|=": lucyast.AugAssign,
    # comparison
    "==": lambda (left, right): lucyast.Compare(left, [('==', right)]),
    "<" : lambda (left, right): lucyast.Compare(left, [('<', right)]),
    "<=": lambda (left, right): lucyast.Compare(left, [('<=', right)]),
    ">" : lambda (left, right): lucyast.Compare(left, [('>', right)]),
    ">=": lambda (left, right): lucyast.Compare(left, [('>=', right)]),
    "!=": lambda (left, right): lucyast.Compare(left, [('!=', right)]),
    # identity
    "is": lambda (left, right): lucyast.Compare(left, [('is', right)]),
    "is not": lambda (left, right): lucyast.Compare(left, [('is not', right)]),
    # contains
    "in": lambda (left, right): lucyast.Compare(left, [('in', right)]),
    "not in": lambda (left, right): lucyast.Compare(left, [('not in', right)]),
}


unary_ops = {
    "+": lucyast.UnaryAdd,
    "-": lucyast.UnarySub,
}
#shift/reduce conflict in state 5 resolved as shift.
#shift/reduce conflict in state 5 resolved as shift.
#shift/reduce conflict in state 32 resolved as shift.
#shift/reduce conflict in state 34 resolved as shift.

precedence = (
    ('left', 'NEWLINE'),
    ('left', 'ASSIGN'),
    #('left', 'COMMA'), # conflicts in state 46 without this, tuple
                         # building fails with it
    ('left', 'BOR'),
    ('left', 'BAND'),
    ('right', 'BNOT'),
    ('left', 'IN'),
    ('left', 'IS'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'NE', 'EQ'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'UPLUS', 'UMINUS'),
    ('right', 'UNOT'),
    ('left', 'POW'),
#    ('left', 'DOT'),
    )



# start here
def p_file_input_end(p):
    """file_input_end : file_input ENDMARKER    
    """
    p[0] = lucyast.Stmt(p[1])


def p_file_input(p):
    """file_input : file_input NEWLINE
                  | file_input stmt
                  | NEWLINE
                  | stmt
                  """
    if len(p) == 3:
        if isinstance(p[2], basestring):
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]
    else:
        if isinstance(p[1], basestring):
            p[0] = []
        else:
            p[0] = p[1]


# stmt: simple_stmt | compound_stmt
def p_stmt_simple(p):
    """stmt : simple_stmt
    """
    p[0] = p[1]


def p_stmt_compound(p):
    """stmt : compound_stmt
    """
    p[0] = [p[1]]
  

# simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
def p_simple_stmt(p):
    """simple_stmt : small_stmts NEWLINE
                   | small_stmts SEMICOLON NEWLINE
                   """
    p[0] = p[1]


# compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt
# | with_stmt | funcdef| classdef | decorated
def p_compound_stmt(p):
    """compound_stmt : if_stmt
                     | while_stmt
                     | for_stmt
                     | let_stmt
                     | define_stmt
    """
    p[0] = p[1]
    

def p_small_stmts(p):
    """small_stmts : small_stmts SEMICOLON small_stmt
                   | small_stmt
                   """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


# small_stmt: expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
#    import_stmt | global_stmt | exec_stmt | assert_stmt
def p_small_stmt(p):
    """small_stmt : expr_stmt
                  | assert_stmt
                  | flow_stmt
                  | exec_stmt
    """
    p[0] = p[1]


def p_break(p):
    """flow_stmt : BREAK
    """
    p[0] = lucyast.Break(None)
    

def p_continue(p):
    """flow_stmt : CONTINUE
    """
    p[0] = lucyast.Continue(None)

def p_pass(p):
    """flow_stmt : PASS
    """
    p[0] = lucyast.Pass(None)

# assert_stmt: 'assert' test [',' test]
def p_assert(p):
    """assert_stmt : ASSERT test
                   | ASSERT test COMMA test
                   """
    if len(p) == 3:
        p[0] = lucyast.Assert(p[2], None)
    else:
        p[0] = lucyast.Assert(p[2], p[4])
    

# expr_stmt: testlist (augassign (yield_expr|testlist) |
#                      ('=' (yield_expr|testlist))*)
# augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
#             '<<=' | '>>=' | '**=' | '//=')

# FIXME: only single assignment for now, no augmented and multiple
# assignments
def p_aug_assign(p):
    """expr_stmt : testlist IPLUS testlist
                 | testlist IMINUS testlist
                 | testlist IDIV testlist
                 | testlist IMUL testlist
                 | testlist IMOD testlist
                 | testlist IPOW testlist
                 | testlist ILSHIFT testlist
                 | testlist IRSHIFT testlist
                 | testlist IAND testlist
                 | testlist IOR testlist
                 | testlist INOT testlist
                 | testlist IXOR testlist
                 """
    left, op, right = p[1], p[2], p[3]
    p[0] = lucyast.AugAssign(p[1], p[2], p[3])
    
def p_expr_stmt(p):
    """expr_stmt : testlist ASSIGN testlist
                 | testlist
                 """
    if len(p) == 2:
        # expressions, not assigned anywhere
        p[0] = lucyast.Discard(p[1])
    else:
        left, right = p[1], p[3]
        # make sure assignment to literal fails
        if isinstance(left, lucyast.Const):
            raise SyntaxError("Cannot assign to literal")
        
        # simple assignment
        if isinstance(left, lucyast.Name):
            p[0] = lucyast.Assign([lucyast.AssName(left.name, OP_ASSIGN)], right)

        # attribute assignment
        elif isinstance(left, lucyast.Getattr):
            var, attr = left.asList()
            p[0] = lucyast.Assign([lucyast.AssAttr(var, attr, OP_ASSIGN)], right)

        else:
            raise NotImplementedError("only single assignments: %r"%left)

        

def p_define_code_stmt(p):
    """define_stmt : DEFINE NAME COLON suite
                   | DEFINE expr NAME COLON suite
                   """

    if len(p) == 5:
        p[0] = lucyast.Code(p[2], p[4], lazy=True)
    elif len(p) == 6:
        p[0] = lucyast.Code(p[3], p[5], wrapper=p[2], lazy=True)
    else:
        raise NotImplementedError(len(p))


def p_let_code_stmt(p):
    """let_stmt : LET NAME COLON suite 
                | LET expr NAME COLON suite
                """

    if len(p) == 5:
        p[0] = lucyast.Code(p[2], p[4], lazy=False)
    elif len(p) == 6:
        p[0] = lucyast.Code(p[3], p[5], wrapper=p[2], lazy=False)
    else:
        raise NotImplementedError(len(p))


def p_while_stmt(p):
    """while_stmt : WHILE test COLON suite
                  | WHILE test COLON suite else_stmt
    """
    if len(p) == 5:
        p[0] = lucyast.While(p[2], p[4], None)
    else:
        p[0] = lucyast.While(p[2], p[4], p[5])
    

def p_for_stmt(p):
    """for_stmt : FOR NAME IN test COLON suite
                | FOR NAME IN test COLON suite else_stmt
    """
    assign = lucyast.AssName(p[2], OP_ASSIGN)
    if len(p) == 7:
        p[0] = lucyast.For(assign, p[4], p[6], None)
    else:
        p[0] = lucyast.For(assign, p[4], p[6], p[7])        


def p_exec_stmt(p):
    # FIXME: conflict with "test IN test"
    """exec_stmt : EXEC NAME IN test"""
    # exec code in global, local
    p[0] = lucyast.Exec(p[2], None, p[4])


def p_if_stmt(p):
    """if_stmt : conds 
               | conds else_stmt
    """
    if len(p) == 2:
        p[0] = lucyast.If(p[1], None)
    elif len(p) == 3:
        p[0] = lucyast.If(p[1], p[2])


def p_conds(p):
    """conds : if_cond
             | if_cond elif_conds
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]+p[2]


def p_else_stmt(p):
    """else_stmt : ELSE COLON suite
    """
    p[0] = p[3]


def p_elif_conds(p):
    """elif_conds : elif_conds elif_cond
                  | elif_cond
                  """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_elif_cond(p):
    """elif_cond : ELIF test COLON suite
    """
    p[0] = [(p[2], p[4])]


def p_if_cond(p):
    """if_cond : IF test COLON suite
    """
    p[0] = [(p[2], p[4])]

# suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
def p_suite(p):
    """suite : simple_stmt
             | NEWLINE INDENT stmts DEDENT
            """
    if len(p) == 2:
        p[0] = lucyast.Stmt(p[1])
    else:
        p[0] = lucyast.Stmt(p[3])


### statements
def p_stmts(p):
    """stmts : stmts stmt
             | stmt
             """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]



### expressions, tuples, lists, etc
# or_test: and_test ('or' and_test)*
def p_or_test(p):
    """or_test : or_test BOR and_test
               | and_test
               """
    if len(p) == 4:
        p[0] = lucyast.Or((p[1], p[3]))
    else:
        p[0] = p[1]


# and_test: not_test ('and' not_test)*
def p_and_test(p):
    """and_test : and_test BAND not_test
                | not_test
                """
    if len(p) == 4:
        p[0] = lucyast.And((p[1], p[3]))
    else:
        p[0] = p[1]
        

# not_test: 'not' not_test | comparison
def p_not_test(p):
    """not_test : BNOT not_test
                | comparison
                """
    if len(p) == 3:
        p[0] = lucyast.Not(p[2])
    else:
        p[0] = p[1]


# I can go straight to comparison here
# comparison: expr (comp_op expr)*
# comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
def p_comparison(p):
    """comparison : expr LT expr
                  | expr LE expr
                  | expr GT expr
                  | expr GE expr
                  | expr NE expr
                  | expr EQ expr
                  | expr IS expr
                  | expr IS BNOT expr
                  | expr IN expr
                  | expr BNOT IN expr
                  | expr
               """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    elif len(p) == 5:
        op = p[2] + ' ' + p[3]
        p[0] = binary_ops[op]((p[1], p[4]))
        
    else:
        p[0] = p[1]


# expr: xor_expr ('|' xor_expr)*
def p_expr(p):
    """expr : expr OR xor_expr
            | xor_expr
            """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]
    

# xor_expr: and_expr ('^' and_expr)*
def p_xor_expr(p):
    """xor_expr : xor_expr XOR and_expr
                | and_expr
                """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]
    

# and_expr: shift_expr ('&' shift_expr)*
def p_and_expr(p):
    """and_expr : and_expr AND shift_expr
                | shift_expr
                """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]


# shift_expr: arith_expr (('<<'|'>>') arith_expr)*
def p_shift_expr(p):
    """shift_expr : shift_expr LSHIFT arith_expr
                  | shift_expr RSHIFT arith_expr
                  | arith_expr
                  """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]


# arith_expr: term (('+'|'-') term)*
def p_arith_expr(p):
    """arith_expr : arith_expr PLUS term
                  | arith_expr MINUS term
                  | term
                  """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]

    
# term: factor (('*'|'/'|'%'|'//') factor)*
def p_term(p):
    # FIXME: truediv missing? 
    """term : term MULT factor
            | term DIV factor
            | term MOD factor
            | factor
            """
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    else:
        p[0] = p[1]

    
# factor: ('+'|'-'|'~') factor | power 
def p_factor(p):
    # unary operators
    # FIXME: | NOT factor
    
    """factor : PLUS factor %prec UPLUS
              | MINUS factor %prec UMINUS
              | NOT factor %prec UNOT
              | power
              """
    if len(p) == 3:
        p[0] = unary_ops[p[1]](p[2])
    else:
        p[0] = p[1]


def p_power(p):
    """power : power POW atom_attr
             | atom_attr
             """
    if len(p) == 4:
        p[0] = lucyast.Power((p[1], p[3]))
    else:
        p[0] = p[1]


def p_atom_attr(p):
    """atom_attr : atom_call
                 | atom_call DOT atom_call
    """
    if len(p) == 4:
        # FIXME: name?
        p[0] = lucyast.Getattr(p[1], p[3].name)
    else:
        p[0] = p[1]
                          

    

# power: atom trailer* ['**' factor]
# FIXME: *args, **kwds
def p_atom_call(p):
    """atom_call : atom
                 | atom trailer
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[2][0] == 'CALL':
            p[0] = lucyast.CallFunc(p[1], p[2][1], None, None)
        else:
            raise NotImplementedError('not CALL')
    else:
        raise NotImplementedError(len(p))
        

# varname 
def p_atom_name(p):
    """atom : NAME"""
    p[0] = lucyast.Name(p[1])

# constants: FIXME: use Decimal for numbers?
def p_atom_int(p):
    """atom : ICONST
    """
    p[0] = lucyast.Const(int(p[1]))

def p_atom_float(p):
    """atom : FCONST
    """
    p[0] = lucyast.Const(float(p[1]))
    
def p_atom_string(p):
    """atom : SCONST
    """
    p[0] = lucyast.Const(p[1])#FIXME

def p_atom_list(p):
    """atom : LBRACKET testlist RBRACKET
    """
    p[0] = lucyast.List(p[2].nodes)

# tuple
def p_atom_tuple(p):
    """atom : LPAREN testlist RPAREN"""
    p[0] = p[2]

def p_atom_dict(p):
    """atom : LBRACE keyvaluelist RBRACE"""
    p[0] = lucyast.Dict(p[2])

def p_keyvaluelist(p):
    """keyvaluelist : keyvalue COMMA keyvaluelist
                    | keyvalue COMMA
                    | keyvalue
                    """
    if len(p) in (2, 3):
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        raise NotImplementedError

def p_keyvalue(p):
    """keyvalue : SCONST COLON test
    """
    p[0] = (lucyast.Const(p[1]), p[3]) #FIXME

# trailer : '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
def p_trailer(p):
    # FIXME: single call, no subscript, no .NAME
    """trailer : LPAREN arglist RPAREN
               | LPAREN RPAREN
    """
    if len(p) == 4:
        p[0] = ("CALL", p[2])
    elif len(p) == 3:
        p[0] = ("CALL", [])
    else:
        raise NotImplementedError("args?")



# testlist: test (',' test)* [',']
# FIXME: missing trailing comma
# FIXED, but with shift/reduce conflict
def p_testlist(p):
    """testlist : test COMMA testlist
                | test COMMA
                | test
                """
    
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = lucyast.Tuple([p[1]])
    elif len(p) == 4:
        if isinstance(p[3], lucyast.Tuple):
            p[0] = lucyast.Tuple((p[1],) + p[3].asList())
        else:
            p[0] = lucyast.Tuple((p[1], p[3]))
    else:
        raise NotImplementedError(len(p))
       

# test: or_test ['if' or_test 'else' test] | lambdef
def p_test(p):
    """test : or_test
            | or_test IF or_test ELSE test
            """
    if len(p) == 6:
        p[0] = lucyast.IfExp(p[3], p[1], p[5])
    else:
        p[0] = p[1]
        

#arglist: (argument ',')* (argument [',']
#                         |'*' test (',' argument)* [',' '**' test]
#                         |'**' test)
def p_arglist(p):
    # FIXME: no *args **kwds support
    """arglist : argument COMMA arglist
               | argument COMMA
               | argument
               """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = [p[1]]
    elif len(p) == 4:
        if isinstance(p[3], list):
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1], p[3]]
    else:
        raise NotImplementedError(len(p))

        


# argument: test [gen_for] | test '=' test  # Really [keyword '='] test
def p_argument(p):
    # FIXME: no keyword support
    """argument : test
    """
    p[0] = p[1]


def p_error(t):
    if t is None:
        raise SyntaxError('End of file reached: %r'%yacc.parser.symstack)
    else:
        raise SyntaxError('Lucy Syntax Error: %r'%t)
    


class LucyParser(object):
    def __init__(self, lexer=None):
        if lexer is None:
            lexer = lucylexer.LucyLexer()
        self._lexer = lexer
        self._parser = yacc.yacc()

    def parse(self, code, add_endmarker=True):
        code = code.strip()
        self._lexer.input(code, add_endmarker=add_endmarker)
        result = self._parser.parse(lexer=self._lexer)
        module = lucyast.Module(None, result)
        return module
              

def traverse(node, level=""):
    if node is None:
        raise StopIteration
    
    yield "%s%s"%(level, node.__class__.__name__)
    for subnode in node:
        if not isinstance(subnode, lucyast.Node):
            yield "%s%r"%(level+" ", subnode)
            continue
        for subiter in traverse(subnode, level+" "):
            yield "%s%s"%(level, subiter)


def test_parser():
    from compiler import syntax
    
    parser = LucyParser()
    tree = parser.parse(open('testfull.ly').read())
    for t in traverse(tree):
        print t
    syntax.check(tree)
    

if __name__ == '__main__':
    test_parser()

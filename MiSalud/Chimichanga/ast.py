import operator
from types import LambdaType
#from Chimichanga.exceptions import *
from MiSalud.Chimichanga.exceptions import *
#import Chimichanga.symbol_table
from MiSalud.Chimichanga import symbol_table
import traceback, sys

symbols = symbol_table.SymbolTable()


class InstructionList:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        return '<InstructionList {0}>'.format(self.children)

    def eval(self):
        ret = []
        for n in self:
            if isinstance(n, BreakStatement):
                return n

            res = n.eval()

            if isinstance(res, BreakStatement):
                return res
            elif res is not None:
                ret.append(res)

        return ret


class BaseExpression:
    def eval(self):
        raise NotImplementedError()


class BreakStatement(BaseExpression):
    def __iter__(self):
        return []

    def eval(self):
        pass


class ReturnStatement(BreakStatement):
    def __init__(self, expr: BaseExpression):
        self.expr = expr

    def __repr__(self):
        return '<Return expr={0}>'.format(self.expr)

    def eval(self):
        return full_eval(self.expr)


def full_eval(expr: BaseExpression):
    while isinstance(expr, BaseExpression):
        expr = expr.eval()

    return expr


class Primitive(BaseExpression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Primitive "{0}"({1})>'.format(self.value, self.value.__class__)

    def eval(self):
        return self.value


class Identifier(BaseExpression):
    is_function = False

    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return '<Identifier name={0} line={1}>'.format(self.name, self.line)

    def assign(self, val):
        if self.is_function:
            if symbols.setfunc(self.name, val) == -1:
                print(" ")
                raise SimboloDuplicado("Error en linea %s.\n ---La función '%s' no puede ser re-declarada, asegurese de no usar palabras reservadas para definir funciones.." % (self.line, self.name))
        else:
            symbols.setsym(self.name, val)

    def eval(self):
        if self.is_function:
            return symbols.getfunc(self.name, self.line)

        return symbols.getsym(self.name, self.line)


class Array(BaseExpression):
    def __init__(self, values: InstructionList):
        self.values = values

    def __repr__(self):
        return '<Array len={0} items={1}>'.format(len(self.values.children), self.values)

    def eval(self):
        return self.values.eval()


class ArrayAccess(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression):
        self.array = array
        self.index = index

    def __repr__(self):
        return '<Array index={0}>'.format(self.index)

    def eval(self):
        return self.array.eval()[self.index.eval()]


class ArrayAssign(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression, value: BaseExpression):
        self.array = array
        self.index = index
        self.value = value

    def __repr__(self):
        return '<Array arr={0} index={1} value={2}>'.format(self.array, self.index, self.value)

    def eval(self):
        self.array.eval()[self.index.eval()] = self.value.eval()


class ArraySlice(BaseExpression):
    def __init__(self, array: Identifier, start: BaseExpression=None, end: BaseExpression=None):
        self.array = array
        self.start = start
        self.end = end

    def __repr__(self):
        return '<ArraySlice array={0} start={1} end={2}>'.format(self.array, self.start, self.end)

    def eval(self):
        if self.start is not None and self.end is not None:
            # access [start : end]
            return self.array.eval()[self.start.eval():self.end.eval()]

        elif self.start is None and self.end is not None:
            # access [: end]
            return self.array.eval()[:self.end.eval()]

        elif self.start is not None and self.end is None:
            # access [start :]
            return self.array.eval()[self.start.eval():]
        else:
            return self.array.eval()[:]


class Assignment(BaseExpression):
    def __init__(self, identifier: Identifier, val, line):
        self.identifier = identifier
        self.val = val
        self.line = line

    def __repr__(self):
        return '<Assignment sym={0}; val={1} line={2}>'.format(self.identifier, self.val, self.line)

    def eval(self):
        if self.identifier.is_function:
            self.identifier.assign(self.val)
        else:
            self.identifier.assign(self.val.eval())


class BinaryOperation(BaseExpression):
    __operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '**': operator.pow,
        '/': operator.truediv,
        '%': operator.mod,

        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,

        'and': lambda a, b: a.eval() and b.eval(),
        'or': lambda a, b: a.eval() or b.eval(),

        '&': operator.and_,
        '|': operator.or_,
        '^': operator.xor,
        '>>': operator.rshift,
        '<<': operator.lshift,
    }

    def __repr__(self):
        return '<BinaryOperation left ={0} right={1} operation="{2}" line={3}>'.format(self.left, self.right, self.op, self.line)

    def __init__(self, left, right, op, line):
        self.left = left
        self.right = right
        self.op = op
        self.line = line

    def eval(self):
        left = None
        right = None

        try:
            # find the operation that needs to be performed
            op = self.__operations[self.op]

            # in case of lambda, pass the arguments unevaluated as they will
            # be properly evaluated only when necessary during the lambda call.
            if isinstance(op, LambdaType):
                return op(self.left, self.right)

            # otherwise, straight up call the operation, also save the variables
            # in case they are to be used for the exception block
            left = self.left.eval()
            right = self.right.eval()
            return op(left, right)
        except TypeError:
            fmt = (self.line, left.__class__.__name__, left, self.op, right.__class__.__name__, right)
            raise ErrorAritmetico("\nError semantico en la linea %s. \n ---No es posible aplicar la operación (%s: %s) %s (%s: %s)" % fmt)


class CompoundOperation(BaseExpression):
    __operations = {
        '+=': operator.iadd,
        '-=': operator.isub,
        '/=': operator.itruediv,
        '*=': operator.imul,
        '%=': operator.imod,
        '**=': operator.ipow,
    }

    def __init__(self, identifier: Identifier, modifier: BaseExpression, operation: str):
        self.identifier = identifier
        self.modifier = modifier
        self.operation = operation

    def __repr__(self):
        fmt = '<Compound identifier={0} mod={1} operation={2}>'
        return fmt.format(self.identifier, self.modifier, self.operation)

    def eval(self):
        # Express the compound operation as a 'simplified' binary op
        # does not return anything as compound operations
        # are statements and not expressions

        l = self.identifier.eval()
        r = self.modifier.eval()

        try:
            self.identifier.assign(self.__operations[self.operation](l, r))
        except TypeError:
            fmt = (l.__class__.__name__, l, self.operation, r.__class__.__name__, r)
            raise ErrorAritmetico("\nError semanticos en la linea . \n ---No es posible aplicar la operación (%s: %s) %s (%s: %s)" % fmt)


class UnaryOperation(BaseExpression):
    __operations = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
        'not': operator.not_
    }

    def __repr__(self):
        return '<Unary operation: operation={0} expr={1}>'.format(self.operation, self.expr)

    def __init__(self, operation, expr: BaseExpression):
        self.operation = operation
        self.expr = expr

    def eval(self):
        return self.__operations[self.operation](self.expr.eval())


class If(BaseExpression):
    def __init__(self, condition: BaseExpression, truepart: InstructionList, elsepart=None):
        self.condition = condition
        self.truepart = truepart
        self.elsepart = elsepart

    def __repr__(self):
        return '<If condition={0} then={1} else={2}>'.format(self.condition, self.truepart, self.elsepart)

    def eval(self):
        if self.condition.eval():
            return self.truepart.eval()
        elif self.elsepart is not None:
            if isinstance(self.elsepart, BaseExpression):
                return self.elsepart.eval()
            else:
                return self.elsepart.eval()


class For(BaseExpression):
    def __init__(self, variable: Identifier, start: Primitive, end: Primitive, asc: bool, body: InstructionList):
        self.variable = variable
        self.start = start
        self.end = end
        self.asc = asc  # ascending order
        self.body = body

    def __repr__(self):
        fmt = '<For start={0} direction={1} end={2} body={3}>'
        return fmt.format(self.start, 'asc' if self.asc else 'desc', self.end, self.body)

    def eval(self):
        if self.asc:
            lo = self.start.eval()
            hi = self.end.eval() + 1
            sign = 1
        else:
            lo = self.start.eval()
            hi = self.end.eval() - 1
            sign = -1

        for i in range(lo, hi, sign):
            self.variable.assign(i)

            # in case of BREAK statement prematurely break the loop
            if isinstance(self.body.eval(), BreakStatement):
                break


class ForIn(BaseExpression):
    def __init__(self, variable: Identifier, sequence: BaseExpression, body: InstructionList):
        self.variable = variable
        self.sequence = sequence
        self.body = body

    def __repr__(self):
        return '<ForIn var={0} in iterable={1} do body={2}>'.format(self.variable, self.sequence, self.body)

    def eval(self):
        for i in self.sequence.eval():
            self.variable.assign(i)
            if isinstance(self.body.eval(), BreakStatement):
                break


class While(BaseExpression):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return '<While cond={0} body={1}>'.format(self.condition, self.body)

    def eval(self):
        while self.condition.eval():
            if isinstance(self.body.eval(), BreakStatement):
                break


class PrintStatement(BaseExpression):
    def __init__(self, items: InstructionList):
        self.items = items

    def __repr__(self):
        return '<Print {0}>'.format(self.items)

    def eval(self):
        print(*self.items.eval(), end='', sep='')


class FunctionCall(BaseExpression):
    def __init__(self, name: Identifier, params: InstructionList, line):
        self.name = name
        self.params = params
        self.line = line

    def __repr__(self):
        return '<Function call name={0} params={1} line={2}>'.format(self.name, self.params, self.line)

    def __eval_builtin_func(self):
        func = self.name.eval()
        args = []

        for p in self.params:
            args.append(full_eval(p))
        res = func.eval(args)
        if type(res) == str:
            if res[-5:] == "_err_":
                print("\n")
                msg = "\nError en la linea {1} . \n ---Error de tipos en la función {0}(). Se esperaba un tipo {2} y se encontró un {3} \n"
                raise ArgumentosInvalidos(msg.format(self.name.name, self.line, res[:-5], type(args[0])))
            if res[-9:] == "_cantErr_":
                print("\n")
                msg = "\nError en la linea {1} . \n ---La función {0}() esperaba {2} argumentos (se encontraron {3}) \n"
                raise ArgumentosInvalidos(msg.format(self.name.name, self.line, res[:-9], len(args)))
            if res[-9:] == "_convErr_":
                print("\n")
                msg = "\nError en la linea {1} . \n ---La función {0}() no puede convertir el valor '{2}' al tipo {3} \n"
                raise ArgumentosInvalidos(msg.format(self.name.name, self.line, args[0], res[:-9]))
            return res
        return res

    def __eval_udf(self):
        func = self.name.eval()
        args = {}

        # check param count
        l1 = len(func.params)
        l2 = len(self.params)

        if l1 != l2:
            msg = "Error en la linea . \n ---Numero invalido de argumentos para la función {0}(_error_). Se esperaban {1} argumentos y se encontraron {2} \n"
            raise ArgumentosInvalidos(msg.format(self.name.name, l1, l2))

        # pair the defined parameters in the function signature with
        # whatever is being passed on.
        #
        # On the parameters we only need the name rather than fully evaluating them
        for p, v in zip(func.params, self.params):
            args[p.name] = full_eval(v)

        return func.eval(args)

    def eval(self):
        if isinstance(self.name.eval(), BuiltInFunction):
            return self.__eval_builtin_func()

        return self.__eval_udf()


class Function(BaseExpression):
    def __init__(self, params: InstructionList, body: InstructionList):
        self.params = params
        self.body = body

    def __repr__(self):
        return '<Function params={0} body={1}>'.format(self.params, self.body)

    def eval(self, args):
        symbols.set_local(True)

        for k, v in args.items():
            symbols.setsym(k, v)

        try:
            ret = self.body.eval()

            if isinstance(ret, ReturnStatement):
                return ret.eval()
        finally:
            symbols.set_local(False)

        return None


class BuiltInFunction(BaseExpression):
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return '<Builtin function {0}>'.format(self.func)

    def eval(self, args):
        res = self.func(*args)
        return res


class InExpression(BaseExpression):
    def __init__(self, a: BaseExpression, b: BaseExpression, not_in: bool=False):
        self.a = a
        self.b = b
        self.not_in = not_in

    def __repr__(self):
        return '<In {0} in {1}>'.format(self.a, self.b)

    def eval(self):
        if self.not_in:
            return self.a.eval() not in self.b.eval()
        return self.a.eval() in self.b.eval()


class TernaryOperator(BaseExpression):
    def __init__(self, cond: BaseExpression, trueval: BaseExpression, falseval: BaseExpression):
        self.cond = cond
        self.trueval = trueval
        self.falseval = falseval

    def __repr__(self):
        return '<Ternary cond={0} true={1} false={2}>'.format(self.cond, self.trueval, self.falseval)

    def eval(self):
        return self.trueval.eval() if self.cond.eval() else self.falseval.eval()

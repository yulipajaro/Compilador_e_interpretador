class InterpreterException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SimboloNoEncontrado(InterpreterException):
    pass


class UnexpectedCharacter(InterpreterException):
    pass


class ParserSyntaxError(InterpreterException):
    pass


class SimboloDuplicado(InterpreterException):
    pass


class ErrorAritmetico(InterpreterException):
    pass


class ArgumentosInvalidos(InterpreterException):
    pass

class VariableNoInicializada(InterpreterException):
    pass

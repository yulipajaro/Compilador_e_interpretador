#from Chimichanga.exceptions import *
from MiSalud.Chimichanga.exceptions import *;

class SymbolTable:
    __func = 'functions'
    __sym = 'symbols'
    __local = 'local'

    __table = {
        __func: {},
        __sym: {},
        __local: []
    }

    def __is_local(self):
        '''
        Returns true if symbol table is being called from inside
        a function rather than the global scope

        :return: bool
        '''
        return len(self.__table[self.__local]) > 0

    def table(self):
        return self.__table

    def get_local_table(self):
        '''
        Returns the active local symbol table (the last one on the stack)
        '''

        t = self.__table[self.__local]

        return t[len(t) - 1]

    def set_local(self, flag):
        if flag:
            self.__table[self.__local].append({})
        else:
            self.__table[self.__local].pop()

    def getsym(self, sym, line):
        # busca la variable en la tabla de simbolos local
        if self.__is_local() and sym in self.get_local_table():
            return self.get_local_table()[sym]

        # si no se encuentra, se buscar en las variables globales
        if sym in self.__table[self.__sym]:
            return self.__table[self.__sym][sym]

        # no se encuentra en ningun lado... sorry :(
        raise SimboloNoEncontrado("Error en linea %s.\n ---Variable '%s' no identificada." % (line,sym))

    def setsym(self, sym, val):
        if self.__is_local():
            self.get_local_table()[sym] = val
        else:
            self.__table[self.__sym][sym] = val

    def getfunc(self, name, line):
        if name in self.__table[self.__func]:
            return self.__table[self.__func][name]

        raise SimboloNoEncontrado("Error en linea %s.\n ---Funcion '%s' no identificada." % (line, name))

    def setfunc(self, name, val):
        if name in self.__table[self.__func]:
            return -1

        self.__table[self.__func][name] = val

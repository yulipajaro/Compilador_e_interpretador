from MiSalud.Chimichanga import parser as p
from MiSalud.Chimichanga import ast
from MiSalud.Chimichanga import environment
from MiSalud.Chimichanga import exceptions
from pprint import pprint
import sys, traceback


def execute(source, filename, data_log: bool=False, disable_warnings: bool=True):
    p.disable_warnings = disable_warnings

    try:
        res = p.get_parser().parse(source)
        environment.declare_env(ast.symbols)

        for node in res.children:
            node.eval()

        if data_log:
            lenStr = len(filename)-1
            name = ""
            curCh = filename[lenStr]
            while curCh != '/':
                name = name + curCh
                lenStr -= 1
                curCh = filename[lenStr]
            name = name[::-1]
            name = name[:-4] + "_Log.txt"
            with open(name, 'wt') as archivo_log:
                archivo_log.write('=' * 50 + ' == Arbol sintactico ==' + '=' * 50 + "\n\n")
                pprint(res.children, stream=archivo_log)
                archivo_log.write("\n\n" + '=' * 50 + ' == Tabla de Simbolos ==' + '=' * 50 + "\n\n")
                pprint(ast.symbols.table(), stream=archivo_log)           
            archivo_log.close()
    except Exception as e:
        print(e.__class__.__name__ + ': ' + str(e), file=sys.stderr)
        if not disable_warnings:
            raise e
    
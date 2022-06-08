#import Chimichanga
from MiSalud import Chimichanga
#import Chimichanga.ast as ast
from MiSalud.Chimichanga import ast
#import Chimichanga.symbol_table
from MiSalud.Chimichanga.symbol_table import *
import math
import time
import random


def substr(s: str, start: int, length: int):
    return s[start:start + length]


def str_pos(sub: str, string: str):
    return string.index(sub)


def str_format(string, *args):
    return string % tuple(args)

#push(list, obj)
def push(*args):
    if len(args) != 2:
        return "2_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return args[0].append(args[1])

#pop(list)
def pop(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return args[0].pop(0)

#insert(list, int, obj)
def insert(*args):
    if len(args) != 3:
        return "3_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    if type(args[1]) != int:
        return "Int_err_"
    else:
        args[0].insert(i, x)

#delete(list,int)
def delete(*args):
    if len(args) != 2:
        return "2_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return args[0].remove(args[1])

#reverse(list)
def reverse(arr: list):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        args[0].reverse()

#sortAsc(list)
def sortAsc(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        args[0].sort()

#sortDesc(list)
def sortDesc(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        args[0].sort()
        args[0].reverse()

#count(list, obj)
def count(*args):
    if len(args) != 2:
        return "2_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return args[0].count(args[1])

#length(list)
def length(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return len(args[0])

#minList(list)
def minList(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:   
        return min(args[0])

#maxList(list)
def maxList(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return max(args[0])

#search(list, obj)
def search(*args):
    if len(args) != 2:
        return "2_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return args[1] in args[0]

#promList(list)
def promList(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != list:
        return "List_err_"
    else:
        return sum(args[0])/len(args[0])
    
#prom(*int)
def prom(*args):
    if len(args) == 0:
        return "al menos 1_cantErr_"
    for arg in args:
        if type(arg) != int:
            return "Int_err_"
    return sum(args)/len(args)

#minArg(*int)
def minArg(*args):
    if len(args) == 0:
        return "al menos 1_cantErr_"
    for arg in args:
        if type(arg) != int:
            return "Int_err_"
    return min(args)

#maxArg(*int)
def maxArg(*args):
    if len(args) == 0:
        return "al menos 1_cantErr_"
    for arg in args:
        if type(arg) != int:
            return "Int_err_"
    return max(args)

#toInt(str o chr)
def toInt(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != str and type(args[0]) != chr:
        return "String_err_"
    try:
        return int(args[0])
    except:
        return "Int_convErr_"

#toFloat(str o chr)
def toFloat(*args):
    if len(args) != 1:
        return "1_cantErr_"
    if type(args[0]) != str and type(args[0]) != chr:
        return "String o Char_err_"
    try:
        return float(args[0])
    except:
        return "Int_convErr_"

#toInt(str o chr)
def toStr(*args):
    if len(args) != 1:
        return "1_cantErr_"
    try:
        return str(args[0])
    except:
        return "String_convErr_"
    
    
def declare_env(s: Chimichanga.symbol_table.SymbolTable):
    f = ast.BuiltInFunction

    # "constants"
    s.setsym('pi', math.pi)
    s.setsym('e', math.e)

    # Built in functions

    # math
    s.setfunc('toInt', f(toInt))
    s.setfunc('toFloat', f(toFloat))
    s.setfunc('round', f(round))
    s.setfunc('abs', f(abs))
    s.setfunc('log', f(math.log))
    s.setfunc('log2', f(math.log))
    s.setfunc('rand', f(random.randint))
    s.setfunc('randrange', f(random.randrange))

    s.setfunc('sin', f(int))
    s.setfunc('cos', f(int))
    s.setfunc('tan', f(math.tan))
    s.setfunc('atan', f(math.atan))

    s.setfunc('prom', f(prom))
    s.setfunc('promList', f(promList))
    s.setfunc('minArg', f(minArg))
    s.setfunc('maxArg', f(maxArg))

    # string
    s.setfunc('substr', f(substr))
    s.setfunc('len', f(len))
    s.setfunc('pos', f(str_pos))
    s.setfunc('upper', f(str.upper))
    s.setfunc('lower', f(str.lower))
    s.setfunc('replace', f(str.replace))
    s.setfunc('format', f(str_format))
    s.setfunc('toStr', f(toStr))

    # misc
    s.setfunc('toChr', f(chr))
    s.setfunc('ord', f(ord))
    s.setfunc('time', f(time.time))

    # arrays
    s.setfunc('insert', f(insert))
    s.setfunc('pop', f(pop))
    s.setfunc('push', f(push))
    s.setfunc('delete', f(delete))
    s.setfunc('reverse', f(reverse))
    s.setfunc('sortAsc', f(sortAsc))
    s.setfunc('sortDesc', f(sortDesc))
    s.setfunc('count', f(count))
    s.setfunc('length', f(length))
    s.setfunc('minList', f(minList))
    s.setfunc('maxList', f(maxList))
    s.setfunc('search', f(search))

    # input
    s.setfunc('read', f(input))

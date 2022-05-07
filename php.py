from __future__ import annotations
import sys


def echo(*args: str)->None:
    for arg in args:
        sys.stdout.buffer.write(arg.encode("raw_unicode_escape"));
    #sys.stdout.flush();

def strpos(haystack: int, needle: str, offset: int = 0)-> int|None:
    # cheat sheet: https://stackoverflow.com/a/17143335/1067003
    pos = haystack.find(needle, offset);
    if pos == -1:
        return None;
    return pos;


def escapeshellarg(s: str)->str:
    #Todo: escapeshellarg for windows? it's hell though: https://docs.microsoft.com/en-us/archive/blogs/twistylittlepassagesallalike/everyone-quotes-command-line-arguments-the-wrong-way
    # this is the bash method: 
    if s.find("\x00") != -1:
        raise ValueError("String contains null bytes, it is impossible to escape null bytes in bash!");
    return "'" + s.replace("'", "'\\''") + "'"

def array_push(array: list|dict, *args: str)->int:
    # todo this can be optimized to only check the type of array once.
    for arg in args:
        if isinstance(array, list):
            array.append(arg);
        elif isinstance(array, dict):
            array[len(array)] = arg;
        else:
            raise TypeError("array_push() only works on lists and dicts!");
    return len(array);

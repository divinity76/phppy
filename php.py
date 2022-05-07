from __future__ import annotations
import sys


def echo(*args: str)->None:
    for arg in args:
        sys.stdout.buffer.write(arg.encode("raw_unicode_escape"));



def strpos(haystack: int, needle: str, offset: int = 0)-> int|None:
    # cheat sheet: https://stackoverflow.com/a/17143335/1067003
    pos = haystack.find(needle, offset);
    if pos == -1:
        return None;
    return pos;


def escapeshellarg(s: str)->str:
    #Todo: escapeshellarg for windows? it's hell though: https://docs.microsoft.com/en-us/archive/blogs/twistylittlepassagesallalike/everyone-quotes-command-line-arguments-the-wrong-way
    # this is the bash method: 
    if b'\x00' in s:
        raise ValueError("String contains null bytes, it is impossible to escape null bytes in bash!");
    return "'" + s.replace("'", "'\\''") + "'"

from __future__ import annotations
import typing
import sys
import inspect
import time
import math
# from var_dump import var_dump

def __FILE__() -> str:
    # ptyhon has a native __file__ 
    return inspect.currentframe().f_back.f_code.co_filename

def __LINE__() -> int:
    # python has no native __line__, the closest thing I could find was: sys._getframe().f_lineno
    return inspect.currentframe().f_back.f_lineno



def echo(*args: str | bytes | int | float) -> None:
    for arg in args:
        if isinstance(arg, bytes):
            sys.stdout.buffer.write(arg)
        elif isinstance(arg, str):
            sys.stdout.buffer.write(arg.encode("raw_unicode_escape"))
        elif isinstance(arg, (int, float)):
            sys.stdout.buffer.write(str(arg).encode("ascii"))
        else:
            raise TypeError(
                "echo() only accepts str, bytes, int, and float arguments, got " + str(type(arg)))
    sys.stdout.flush();


def strpos(haystack: str, needle: str, offset: int = 0) -> int | None:
    # cheat sheet: https://stackoverflow.com/a/17143335/1067003
    pos = haystack.find(needle, offset)
    if pos == -1:
        return None
    return pos


# this function is mis-named, it should have been called quoteshellarg
def escapeshellarg(s: str) -> str:
    # Todo: escapeshellarg for windows? it's hell though: https://docs.microsoft.com/en-us/archive/blogs/twistylittlepassagesallalike/everyone-quotes-command-line-arguments-the-wrong-way
    # this is the bash method:
    if s.find("\x00") != -1:
        raise ValueError(
            "String contains null bytes, it is impossible to escape null bytes in bash!")
    return "'" + s.replace("'", "'\\''") + "'"


def array_push(array: list | dict, *args: any) -> int:
    if isinstance(array, list):
        array.extend(args)
        return len(array)
    elif isinstance(array, dict):
        # wouldn't surprise me if there's a significantly faster way to do this,
        # but this the first solution I could think of that worked
        key = -1
        # i tried using key = max(array.keys()), but that breaks if the dict has string keys..
        for existingkey in array.keys():
            if isinstance(existingkey, int) and existingkey > key:
                key = existingkey
        for arg in args:
            # loop should not be needed because we already started with the highest key?
            # while key in array:
            key += 1
            array[key] = arg
        return len(array)
    else:
        raise TypeError(
            "array_push() expects a list or dict as first argument, got " + str(type(array)))


def sleep(seconds: float | int) -> None:
    time.sleep(seconds)

def microtime(get_as_float: bool = False) -> float | str:
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())

def exit(status: int | str | None = None) -> typing.NoReturn:
    if status is None:
        sys.exit(0)
    elif isinstance(status, str):
        echo(status)
        sys.exit(0)
    elif isinstance(status, int):
        sys.exit(status)
    else:
        raise TypeError(
            "exit() expects an int | str | None as argument, got " + str(type(status)))

# just an alias for exit
def die(status: int | str | None = None) -> typing.NoReturn:
    exit(status)

def file_get_contents(filename: str, ignored1_use_include_path: None = None, ignored2_context: None = None, offset: int = 0, length: int | None = None) -> str | bytes:
    # with() automatically closes the file. open() throws if it cannot open.
    with open(filename, 'rb') as f:
        ret = ""
        if offset != 0:
            f.seek(offset)
        if length is None:
            ret = f.read()
        else:
            ret = f.read(length)
        try:
            return ret.decode("utf-8", errors = "strict")
        except UnicodeDecodeError:
            try:
                return ret.decode("raw_unicode_escape", errors = "strict")
            except UnicodeDecodeError:
                # possibly unreachable?
                # binary file
                return ret

def bin2hex(string: str|bytes|bytearray) -> str:
    if isinstance(string, str):        
        return string.encode("utf-8").hex()
    if isinstance(string, (bytes, bytearray)):
        return string.hex()
    raise ValueError("bin2hex: string must be str, bytes or bytearray")

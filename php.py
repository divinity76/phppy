from __future__ import annotations
import sys


def echo(*args: str) -> None:
    for arg in args:
        sys.stdout.buffer.write(arg.encode("raw_unicode_escape"))
    # sys.stdout.flush();


def strpos(haystack: int, needle: str, offset: int = 0) -> int | None:
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
        for arg in args:
            # i wonder why list.append() doesn't take *args
            array.append(arg)
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


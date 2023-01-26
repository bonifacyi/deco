#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps


def disable():
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """
    return


def decorator():
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    :return:
    """

    return


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        # print(f'{func.__name__} -> call {wrapper.calls}')
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_args_key = hash(str(args) + str(kwargs))
        if cache_args_key not in wrapper.cache:
            result = func(*args, **kwargs)
            wrapper.cache[cache_args_key] = result
        #    print(f'{func.__name__} - cache added')
        #else:
        #    print(f'{func.__name__} - answer find in cache')
        return wrapper.cache[cache_args_key]

    wrapper.cache = {}
    return wrapper


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """

    @wraps(func)
    def wrapper(*args):
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return func(*args)
        else:
            return func(args[0], wrapper(*args[1:]))

    return wrapper


def trace(label):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    ->>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """
    def trace_deco(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(''.join(func.tab), '-->', fib.__name__ + '(' + str(args[0]) + ')')
            func.tab.append(label)

            result = func(*args, **kwargs)

            func.tab.pop()
            print(''.join(func.tab), '<--', fib.__name__ + '(' + str(args[0]) + ')', '==', result)
            return result

        func.tab = []
        return wrapper

    return trace_deco


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")
    print(foo.cache)

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print(bar(4, 3, 2))
    print("bar was called", bar.calls, "times")
    print(bar.cache)

    print(fib.__doc__)
    print(fib(3))
    print("fib was", fib.calls, 'calls made')


if __name__ == '__main__':
    main()


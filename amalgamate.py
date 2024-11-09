'''
Luamalg -- Lua 5.4.7 core, libraries and interpreter in a single header.
This is the amalgamation generator. Licensing information follows:

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
'''

import os

LUA_VER = '5.4.7'

PROLOGUE = F'''/* Luamalg -- Lua {LUA_VER} core, libraries and interpreter in a single header
file.

  Do this:
    #define LUA_IMPLEMENTATION
  before you include this file in *one* C or C++ file to create the implementation.

Lua is free software distributed under the terms of the MIT license:
Copyright © 1994-2024 Lua.org, PUC-Rio.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <float.h>
#include <limits.h>
#include <locale.h>
#include <math.h>
#include <setjmp.h>
#include <signal.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* setup for luaconf.h */
#define LUA_CORE
#define LUA_LIB
#define ltable_c
#define lvm_c
'''

LUACONF_EPILOGUE = '''/* do not export internal symbols */
#undef LUAI_FUNC
#undef LUAI_DDEC
#undef LUAI_DDEF
#define LUAI_FUNC	static
#define LUAI_DDEC(def)	/* empty */
#define LUAI_DDEF	static
'''

SOURCE_FILES = [
    # core -- used by all
    'lzio.c',
    'lctype.c',
    'lopcodes.c',
    'lmem.c',
    'lundump.c',
    'ldump.c',
    'lstate.c',
    'lgc.c',
    'llex.c',
    'lcode.c',
    'lparser.c',
    'ldebug.c',
    'lfunc.c',
    'lobject.c',
    'ltm.c',
    'lstring.c',
    'ltable.c',
    'ldo.c',
    'lvm.c',
    'lapi.c',
    # auxiliary library -- used by all
    'lauxlib.c',
    # standard library  -- not used by luac
    'lbaselib.c',
    'lcorolib.c',
    'ldblib.c',
    'liolib.c',
    'lmathlib.c',
    'loadlib.c',
    'loslib.c',
    'lstrlib.c',
    'ltablib.c',
    'lutf8lib.c',
    'linit.c',
]

LUA_DIR = 'lua'

# collect headers from sources
# hardcoded base header order
headers = ['lprefix.h', 'luaconf.h', 'lua.h', 'llimits.h', 'lobject.h', 'ltm.h']
for file in SOURCE_FILES:
    with open(os.path.join(LUA_DIR, file), 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('#include "l'):
                header = line.strip().split('"')[1]
                if header not in headers and header != 'ljumptab.h':
                    headers.append(header)

def writeline(ff, lline):
    if lline.strip().startswith('#include "l'):
        ff.write(f'/* {lline.rstrip()} */\n')
    else:
        ff.write(lline)

with open('luamalg.h', 'w', encoding='utf-8') as f:
    print('-- PROLOGUE --')
    f.write(PROLOGUE)

    print('-- HEADERS --')
    for header in headers:
        print(f'{header}')
        f.write(f'/* === {header} === */\n')
        with open(os.path.join(LUA_DIR, header), 'r', encoding='utf-8') as f2:
            for line in f2:
                writeline(f, line)
        if header == 'luaconf.h':
            f.write(LUACONF_EPILOGUE)
            f.write('\n')

    print('-- LUA_IMPLEMENTATION --')
    f.write('#if defined(LUA_IMPLEMENTATION) || defined(LUAMALG_IMPLEMENTATION)\n')
    for file in SOURCE_FILES:
        print(f'{file}')
        f.write(f'/* === {file} === */\n')
        with open(os.path.join(LUA_DIR, file), 'r', encoding='utf-8') as f2:
            for line in f2:
                writeline(f, line)
    f.write('#endif /* defined(LUA_IMPLEMENTATION) || defined(LUAMALG_IMPLEMENTATION) */\n')

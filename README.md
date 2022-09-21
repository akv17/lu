# lu
tiny and simple educational asm-like language featuring its own compiler and python-based interpreter  

# demo-program
```
DEF foo (x, y)
    ADD x, y
END

SET x 3
SET y 1
CALL foo(x, y)  # stores to r0
```
# instructions
```
SET:
    dloc*|did* (sets zero)
    sloc|sid|const   dloc*|did*

DEL:
    dloc|did

ADD, SUB, MUL, DIV:
    sloc|const|sid   dloc|did
    sloc|const|sid   sloc|sid|const   [dloc*|did*]

DEF:
    did* (did*, ...)

RET:
    loc|id

CALL:
    id (id|loc, ...)   [dloc*|did*]
```

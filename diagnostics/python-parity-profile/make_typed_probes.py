"""Emit two hand-written typed Wasm kernels for bounded standard inputs.

This is a feasibility experiment, not an Aquarius compiler or general Wasm tool.
The algorithms retain naive Fibonacci recursion and unmemoized Collatz iteration.
Only fib(28) and collatz(10000) are used for performance comparisons; both stay
within signed 32-bit arithmetic. No cancellation/GC/suspension guards are present.
"""
from pathlib import Path
import sys


def unsigned(n):
    out = bytearray()
    while True:
        b = n & 127
        n >>= 7
        out.append(b | (128 if n else 0))
        if not n:
            return out


def text(s):
    data = s.encode("utf-8")
    return unsigned(len(data)) + data


def section(tag, data):
    return bytes([tag]) + unsigned(len(data)) + data


# (func (param i32) (result i32))
types = bytes([1, 0x60, 1, 0x7f, 1, 0x7f])
functions = bytes([2, 0, 0])
exports = bytes([2]) + text("fib") + bytes([0, 0]) + text("collatz") + bytes([0, 1])
fib = bytes.fromhex("00 20 00 41 02 48 04 7f 20 00 05 20 00 41 01 6b 10 00 20 00 41 02 6b 10 00 6a 0b 0b")
collatz = bytes.fromhex("""
    01 04 7f
    41 01 21 01
    02 40 03 40
      20 01 20 00 4a 0d 01
      20 01 21 02
      02 40 03 40
        20 02 41 01 46 0d 01
        20 02 41 02 6d 21 04
        20 04 41 02 6c 20 02 46 04 40
          20 04 21 02
        05
          20 02 41 03 6c 41 01 6a 21 02
        0b
        20 03 41 01 6a 21 03
        0c 00
      0b 0b
      20 01 41 01 6a 21 01
      0c 00
    0b 0b
    20 03 0b
""")
code = bytes([2]) + unsigned(len(fib)) + fib + unsigned(len(collatz)) + collatz
module = b"\0asm\x01\0\0\0" + section(1, types) + section(3, functions) + section(7, exports) + section(10, code)
if __name__ == "__main__":
    Path(sys.argv[1]).write_bytes(module)

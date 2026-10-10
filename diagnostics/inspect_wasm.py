"""Inventory opcodes in Aquarius's emitted Wasm subset, decoding immediates.

Fail on unknown instructions instead of mistaking immediate bytes for opcodes.
This is an artifact inspection tool, not a general WebAssembly disassembler.
"""
from collections import Counter
import json
from pathlib import Path
import sys


class Reader:
    def __init__(self, data):
        self.data, self.position = data, 0

    def byte(self):
        value = self.data[self.position]
        self.position += 1
        return value

    def leb(self):
        value, shift = 0, 0
        while True:
            byte = self.byte()
            value |= (byte & 127) << shift
            if not byte & 128:
                return value
            shift += 7

    def take(self, size):
        start = self.position
        self.position += size
        return self.data[start:self.position]


NAMES = {0x00: "unreachable", 0x02: "block", 0x03: "loop", 0x04: "if",
         0x05: "else", 0x0B: "end", 0x0C: "br", 0x0D: "br_if",
         0x0E: "br_table", 0x0F: "return", 0x10: "call", 0x20: "local.get",
         0x21: "local.set", 0x22: "local.tee", 0x41: "i32.const"}


def inspect(path):
    data = path.read_bytes()
    if data[:8] != b"\0asm\1\0\0\0":
        raise ValueError("Expected WebAssembly 1.0")
    reader = Reader(data[8:])
    counts, call_targets = Counter(), Counter()
    functions, declared_locals = 0, 0
    while reader.position < len(reader.data):
        section = reader.byte()
        payload = Reader(reader.take(reader.leb()))
        if section != 10:
            continue
        functions = payload.leb()
        for _ in range(functions):
            body = Reader(payload.take(payload.leb()))
            for _ in range(body.leb()):
                declared_locals += body.leb()
                body.byte()
            while body.position < len(body.data):
                opcode = body.byte()
                if opcode not in NAMES:
                    raise ValueError(f"Unsupported opcode {opcode:#x} in {path.name}")
                counts[NAMES[opcode]] += 1
                if opcode in (0x02, 0x03, 0x04, 0x0C, 0x0D, 0x20, 0x21, 0x22, 0x41):
                    body.leb()
                elif opcode == 0x10:
                    call_targets[body.leb()] += 1
                elif opcode == 0x0E:
                    size = body.leb()
                    for _ in range(size + 1):
                        body.leb()
    return {"functions": functions, "declared_locals": declared_locals,
            "opcodes": dict(counts), "call_targets": dict(call_targets)}


if __name__ == "__main__":
    directory, output = map(Path, sys.argv[1:])
    results = {path.stem: inspect(path) for path in sorted(directory.glob("*.wasm"))}
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for name, result in results.items():
        print(f"{name}: {result['functions']} functions, {result['declared_locals']} locals, {result['opcodes']}")

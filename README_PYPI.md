# ShellLite (LLVM Edition)

ShellLite is an English-like programming language with a high-performance LLVM backend.

## Installation

```bash
pip install shell-lite
```

## Compilation

To compile ShellLite code to native machine code (LLVM IR):

```bash
shl compile script.shl
```

(This automatically uses the LLVM backend to generate `.ll` files, which can be compiled with Clang).

## Usage

```bash
shl script.shl       # Run interpreter
shl                  # Start REPL
```

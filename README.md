# ShellLite: The Comprehensive Guide
## By Shrey Naithani

Welcome to the official documentation for **ShellLite**, the programming language designed to be as readable as plain English,

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Your First Program](#your-first-program)
3. [Language Basics](#language-basics)
   - [Comments](#comments)
   - [Printing Output](#printing-output)
   - [Input](#input)
4. [Variables and Data Types](#variables-and-data-types)
   - [Variables](#variables)
   - [Constants](#constants)
   - [Numbers](#numbers)
   - [Strings](#strings)
   - [Booleans](#booleans)
   - [Lists](#lists)
   - [Dictionaries](#dictionaries)
5. [Control Flow](#control-flow)
   - [If / Else / Elif](#if-else-elif)
   - [Unless](#unless)
   - [Pattern Matching (When)](#pattern-matching-when)
6. [Loops](#loops)
   - [Repeat](#repeat)
   - [While / Until](#while-until)
   - [For Loops](#for-loops)
   - [Loop Control](#loop-control)
7. [Functions](#functions)
   - [Defining Functions](#defining-functions)
   - [Arguments and Defaults](#arguments-and-defaults)
   - [Return Values](#return-values)
   - [Anonymous Functions (Lambdas)](#anonymous-functions-lambdas)
8. [Object-Oriented Programming](#object-oriented-programming)
   - [Things (Classes)](#things-classes)
   - [Properties (Has)](#properties-has)
   - [Methods (Can)](#methods-can)
   - [Inheritance (Extends)](#inheritance-extends)
9. [Modules and Imports](#modules-and-imports)
   - [Using Modules](#using-modules)
   - [Sharing Code](#sharing-code)
10. [Error Handling](#error-handling)
     - [Try / Catch](#try-catch)
     - [Throwing Errors](#throwing-errors)
11. [Standard Library Reference](#standard-library-reference)
    - [Math Module](#math-module)
    - [Time Module](#time-module)
    - [HTTP Module](#http-module)

---

## Introduction

ShellLite was built with a single philosophy: code should be readable by humans first, and machines second. It strips away the curly braces, semicolons, and cryptic keywords of traditional languages, replacing them with natural English words.

Whether you are a beginner writing your first script or an expert looking for a clean way to express logic, ShellLite is for you.

---

## Getting Started

### Installation

ShellLite is distributed as a Python package. Ensure you have Python 3.8+ installed.

```bash
# Clone the repository
git clone https://github.com/Shrey-N/ShellLite.git

# Navigate to the folder
cd ShellLite

# Run the interpreter wrapper
python -m src.main
```

### Your First Program

Create a file named `hello.shl` (ShellLite uses `.shl` extension).

```javascript
say "Hello, World!"
```

Run a script:
```bash
sh your_script.shl
```

Start the REPL:
```bash
sh
```

---

## Language Basics

### Comments
Comments explain your code and are ignored by the computer. Use `#`.

```javascript
# This is a comment
say "Hi" # This prints output
```

### Printing Output
Use `say`, `print`, or `show` to display text.

```javascript
say "Hello"
print "World"
show "!"
```

### Input
Ask the user for input using `ask`.

```javascript
name = ask "What is your name? "
say "Hello, " + name
```

---

## Variables and Data Types

### Variables
Variables store data. You don't need to declare types.

```javascript
score = 100
player_name = "Player 1"
is_active = yes
```

### Constants
Use `const` for values that shouldn't change.

```javascript
const GRAVITY = 9.8
const MAX_LIVES = 3
```

### Numbers
Integers and floating-point numbers.

```javascript
x = 10
y = 3.14
z = -5
```

Math operations work as expected:
```javascript
result = (10 + 5) * 2 / 4
level = 1
level += 1  # Increment
```

### Strings
Text is enclosed in `"doubles"` or `'singles'`.

```javascript
message = "Hello"
description = 'A simple language'
```

Concatenation:
```javascript
full_text = "Part 1" + " and " + "Part 2"
```

### Booleans
Use `yes` (true) and `no` (false).

```javascript
can_fly = no
is_grounded = yes
```

### Lists
Ordered collections of items.

```javascript
# Creating a list
fruits = a list of "apple", "banana", "cherry"

# Accessing items (0-indexed)
say fruits[0]  # apple

# Adding items
fruits.add("date")

# Length
say len(fruits)
```

### Dictionaries
Key-value pairs.

```javascript
user = {
    name: "John",
    age: 30,
    city: "New York"
}

say user["name"]
```

---

## Control Flow

### If / Else / Elif
Make decisions based on conditions.

```javascript
score = 85

if the score is at least 90
    say "A Grade"
elif score is at least 80
    say "B Grade"
else
    say "Keep trying!"
```

### Unless
The opposite of `if`. Executes if the condition is `no` (false).

```javascript
tired = no

unless tired
    say "Keep working!"
```

### Pattern Matching (When)
A cleaner alternative to many `if/elif` blocks.

```javascript
day = "Monday"

when day
    is "Saturday"
        say "Weekend!"
    is "Sunday"
        say "Weekend!"
    is "Monday"
        say "Back to work..."
    otherwise
        say "Mid-week grind"
```

---

## Loops

### Repeat
Run code a specific number of times.

```javascript
repeat 3 times
    say "Hip Hip Hooray!"
```

### While / Until
Loop while a condition is true, or until it becomes true.

```javascript
count = 5
while count is more than 0
    say count
    count -= 1
    
# 'until' is equivalent to 'while not'
energy = 0
until energy == 100
    say "Charging..."
    energy += 10
```

### For Loops
Iterate over lists or ranges.

```javascript
# Loop over list
names = ["Alice", "Bob", "Charlie"]
for name in names
    say "Hello, " + name

# Loop over numbers
for i in range 1 5
    say i  # 1, 2, 3, 4, 5
```

### Loop Control
- `break`: Exit the loop immediately.
- `continue`: Skip to the next iteration.
- `stop`: Alias for break.
- `skip`: Alias for continue.

```javascript
forever
    cmd = ask "> "
    if cmd == "exit"
        stop
```

---

## Functions

### Defining Functions
Use `to` or `fn` to define a function.

```javascript
to greet
    say "Hello there!"

# Call it
greet
```

### Arguments and Defaults
Arguments follow the function name. You can provide default values.

```javascript
to multiply a b=1
    return a * b

say multiply 5 2  # 10
say multiply 5    # 5
```

### Return Values
Use `return` or `give` to send a value back.

```javascript
to square x
    give x * x

result = square 4
say result
```

### Anonymous Functions (Lambdas)
For short, one-line functions.

```javascript
add = fn a, b => a + b
say add 10 20
```

---

## Object-Oriented Programming

ShellLite uses unique keywords to make OOP less intimidating.

### Things (Classes)
Define a blueprint using `thing`.

```javascript
thing Animal
    has species
    has age
```

### Properties (Has)
Instance variables are defined with `has`.

### Methods (Can)
Functions inside a class are defined with `can`.

```javascript
thing Dog
    has name
    
    can bark
        say name + " says Woof!"
```

### Inheritance (Extends)
Build upon existing things.

```javascript
thing Poodle extends Dog
    can dance
        say "Dancing!"
```

### Creating Objects (New)
Use `new` or `make` to create an instance.

```javascript
my_dog = new Dog
my_dog.name = "Rex"
my_dog.bark
```

---

## Modules and Imports

### Using Modules
Import standard modules with `use` or `import`.

```javascript
use "math"
say math.sqrt 16
```

### Sharing Code
Import your own files.

File `utils.sh`:
```javascript
to helper
    say "Helping"
share helper
```

File `main.sh`:
```javascript
use "utils"
utils.helper
```

---

## Error Handling

### Try / Catch
Handle potential errors gracefully.

```javascript
try
    result = 10 / 0
catch error
    say "Oops, something went wrong: " + error
always
    say "Cleanup complete"
```

### Throwing Errors
Raise your own errors.

```javascript
to check_age age
    if age < 0
        throw "Age cannot be negative"
```

---

## Standard Library Reference

### Math Module
`use "math"`

| Function | Description |
|----------|-------------|
| `math.pi` | Value of PI |
| `math.abs(x)` | Absolute value |
| `math.sin(x)` | Sine of x (radians) |
| `math.cos(x)` | Cosine of x |
| `math.random()` | Random float 0.0-1.0 |
| `math.randint(a,b)`| Random int between a and b |

### Time Module
`use "time"`

| Function | Description |
|----------|-------------|
| `time.now()` | Current epoch time |
| `time.sleep(s)` | Pause for s seconds |

### HTTP Module
`use "http"`

| Function | Description |
|----------|-------------|
| `http.get(url)` | GET request |
| `http.post(url, data)` | POST request |

---


## Natural Syntax (v0.02.1)

# ShellLite (v0.02.2)

### Natural Comparisons
Use phrases instead of symbols.

```javascript
score = 100
if score is at least 100
    say "Pass"
    
# Equivalents:
# >=  -> is at least
# ==  -> is exactly
# <   -> is less than
# >   -> is more than
```

### Filler Words
Words like `the` are ignored, allowing for more natural phrasing.

```javascript
if the score is more than 50
    say "Good job"
```

### Natural Wait
Readable pauses.

```javascript
wait for 2 seconds
# Equivalent to: wait 2
```

### Descriptive Collections
Create lists and sets using natural language.

```javascript
fruits = a list of "apple", "banana"
ids = a unique set of 1, 2, 3
```

---

## Advanced Features (v0.02)

### Native GUI
ShellLite 2.0 introduces native support for basic GUI dialogs.

- `alert "Message"`: Show an information box.
- `name = prompt "What is your name?"`: Ask for input via dialog.
- `confirmed = confirm "Are you sure?"`: Ask Yes/No (returns true/false).

```javascript
name = prompt "Enter Name"
if confirm "Is " + name + " correct?"
    alert "Welcome, " + name
```

### Regular Expressions
First-class support for Regex literals.

- Literal syntax: `/pattern/`
- Check match: `string matches /pattern/`

```javascript
email = "test@example.com"
if email matches /^[a-z]+@[a-z]+\.[a-z]+$/
    say "Valid Email"
```

### File System Watcher
React to file changes in real-time.

```javascript
on file_change "data.txt"
    say "File updated!"
```

### Asynchronous Tasks
Run heavy tasks in the background without blocking using `spawn` and `await`.

```javascript
to heavy_work
    sleep 5
    give "Done"

task = spawn heavy_work
say "Working..."
result = await task
```

### Sets
Collections of unique items.

```javascript
unique_ids = a unique set of 1, 2, 2, 3 # -> {1, 2, 3}
unique_ids.add(4)
```

### Type Hints
Optional type safety for functions.

```javascript
to add a:int b:int
    give a + b

add 5 10      # OK
add "5" 10    # Error!
```

### String Interpolation
Embed expressions directly into strings using `{}`.

```javascript
name = "ShellLite"
say "Welcome to {name}, 5+5 is {5+5}"
```

---


---

## Advanced Features (v0.03) - Utilities & Web

### Colored Output
Enhance your terminal output with natural language styling.
Supported colors: `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `bold`.

```javascript
say in red "Error!"
say bold green "Success!"
```

### Progress Bars
Automatically visualize loops with a progress bar.

```javascript
show progress for i in range 1 100
    wait 0.1 # Simulate work
```

### Data Conversion
Convert objects to JSON strings easily.

```javascript
data = { name: "ShellLite", id: 1 }
json = convert data to json
```

### Task Scheduling
Schedule code execution using natural timing phrasing.

```javascript
# Run after a delay
in 10 seconds
    say "Time is up!"

# Run periodically
every 5 minutes
    say "Heartbeat..."
```

### Simple Web Server
Create a basic web server with route handlers.

```javascript
on request to "/hello"
    give "Hello World"

listen on port 8080
```

---


---

## Desktop Automation (v0.04)

ShellLite now supports powerful desktop automation and data handling.

### Date & Time
Natural date handling for scheduling.

```javascript
deadline = date "next friday"
if today is after deadline
    say "Late!"
```

### File Operations
Download files and manage archives.

```javascript
download "https://example.com/data.zip"
extract "data.zip" to "data_folder"
compress folder "backup" to "backup.zip"
```

### CSV Handling
One-line CSV reading and writing.

```javascript
users = load csv "users.csv"
say users[0]["name"]

save users to csv "backup_users.csv"
```

### System Automation
Control your mouse, keyboard, and clipboard.
*(Requires `keyboard`, `mouse`, `pyperclip`, `plyer` packages)*

```javascript
copy "Hello" to clipboard
text = paste from clipboard

type "Hello World"
press "enter"
click at 100, 200
notify "Task Done" "Script finished successfully."
```

---

*Project Developed and maintained by Shrey Naithani.*


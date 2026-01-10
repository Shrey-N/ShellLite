---
title: 'ShellLite: An English-Like Programming Language for Accessible Automation and Education'
tags:
  - Python
  - interpreter
  - education
  - automation
  - natural language programming
authors:
  - name: Shrey Naithani
    affiliation: 1
affiliations:
  - name: Independent Researcher, India
    index: 1
date: 10 January 2026
bibliography: paper.bib
---

# Summary

ShellLite is an interpreted programming language that uses open source development tools and was designed in such a way to let it be more human readable and to focus on greater simplicity in learning programming. Development of ShellLite is based on Python programming. ShellLite overcomes the difficulties of programming by utilizing programming syntax with symbols marked with braces, semicolons, and parentheses to English commands. This tool makes programming seem like performing actions with pseudocode to execute whatever commands or programming in a script format like a story.

The toolkit consists of a lexer, parser, and interpreter all written in Python along with a set of tools that includes a package manager called “The Universe,” a native Python connection called “The Bridge” that allows the use of any library in Python, and a declarative GUI system called “The Canvas.” ShellLite is for educators, students, or automation developers looking for a rapid scripting language that does not require boilerplate coding like traditional languages.

# Statement of need

"ShellLite allows programming tasks to be expressed in a form closer to natural language. This goes toward filling in the chasm that currently exists between a machine parseable form of coding and an expressively attractive form. Classic programming has generally emphasized what the machine is capable of parsing as code rather than what the human mind finds easiest to comprehend. This makes the initial learning curve more daunting. Even the so called friendly language Python uses notations such as indentation and the colon symbol. It has a vocabulary of words that intimidates the novice.

On the other hand, the syntax of ShellLite is understandable by those who know the English language. For example, instead of using print("Hello World"), it would say "Hello World". They could also tell it to add an element x to a list named list instead of using list.append(x). Such resemblance to the English language makes the code or programming self explaining.

The language of A theory of Figures is particularly useful in:

Education: Building foundational concepts in logic, control flow, and data structures without tripping over syntax.
Rapidly automate organizing files, system commands, or processing data in a way that the code reads like it was written for documentation. Accessibility: A coding experience which requires fewer specialized characters, assisting those with certain types of motor skills or vision impairments. Full programming: Though maintainable, ShellLite can be fully functional, support Object Oriented Programming and act as a web server.

# Installation

ShellLite can be installed via pip:
```bash
pip install shell lite
```

Or from source:
```bash
git clone https://github.com/Shrey-N/ShellLite
cd ShellLite
pip install .
```

The language requires Python 3.8 or higher and runs on Windows, macOS, and Linux.

# Example Usage

ShellLite's natural syntax makes common programming tasks intuitive:
```shelllite
# Basic output
say "Hello, World!"

# Variables and arithmetic
age = 25
next_year = age + 1
say "Next year you'll be " + next_year

# Control flow
if age is more than 18
    say "You are an adult"
else
    say "You are a minor"

# Loops
repeat 5 times
    say "Counting..."

# File automation
for file in listdir("./downloads")
    if file.endswith(".pdf")
        copy file "./documents/" + file
    if file.endswith(".jpg")
        copy file "./images/" + file

# Functions
to greet name
    say "Hello, " + name + "!"
    return "Greeted " + name

greet "Alice"

# Web server
listen on port 8080

when someone visits "/"
    h1 "Welcome to ShellLite"
    p "A human readable programming language"
    
when someone visits "/about"
    h1 "About"
    p "ShellLite makes coding accessible to everyone"
```

# Key Features

ShellLite is not a "toy" language that can only print text, it's a powerful environment in which complex applications can be developed.

## Object Oriented Programming

ShellLite supports class definitions, inheritance, and encapsulation, allowing for structured software design:
```shelllite
structure Dog
    has name
    has age
    
    to bark
        say name + " says woof!"
    
    to get_info
        return name + " is " + age + " years old"

my_dog = make Dog
my_dog.name = "Buddy"
my_dog.age = 3
my_dog.bark()
```

Users can define custom types and logic using English like definitions, making advanced concepts approachable even for beginners.

## The Python Bridge

A critical feature for research utility is interoperability. "The Bridge" allows ShellLite code to directly import and utilize any Python library installed in the environment. This is implemented via Python's `importlib` mechanism, allowing ShellLite to serve as a readable orchestration layer over Python's computational libraries:
```shelllite
use python "numpy" as np
use python "pandas" as pd

# Load and analyze data
data = pd.read_csv("data.csv")
mean_value = np.mean(data["sales"])
say "Average sales: " + mean_value

# Statistical analysis
correlation = data.corr()
say correlation
```

This means researchers can utilize `pandas`, `numpy`, `scikit learn`, or any other Python library for data analysis while writing the orchestration logic in human readable ShellLite.

## Web Server & Self Hosting

The language currently provides a built in web server module that is capable of routing. To prove its production viability, the official ShellLite website [@shelllite] is written entirely in ShellLite itself, including all the routing logics and dynamic content rendering. This proves the language's capability to handle HTTP requests, routing, and content serving in a productionlike environment.

## Native UI Capabilities (The Canvas)

For desktop applications, ShellLite provides a declarative way to build GUIs, abstracting away the complexities of event loops and widget management found in traditional frameworks like Tkinter:

```shelllite
app "My Desktop App" size 400 300:
    column:
        heading "Welcome"
        text "Click the button below"
        button "Click Me" as my_btn do:
            alert "The button was clicked!"
```

# State of the field

Natural language programming was pursued since COBOL [@Sammet1969] which aimed to be readable by business managers. Yet the verbosity of COBOL (e.g., `ADD A TO B GIVING C`) and rigid column based formatting made maintenance problematic and hard to adapt to modern development practices.

AppleScript [@Cook2007] managed to reach high readability thanks to instructions such as `tell application "Finder" to open file "document.txt"`, but it was afflicted by platform lock in, and ambiguous parsing rules made debugging hard. The development of this language has largely stalled since the mid 2000s.

Limitation Modern educational languages like Scratch [@Resnick2009] and Blockly [@Fraser2015] use visual blocks instead of text. This clearly eliminates syntax errors, but does limit expressiveness for complex programs and does not teach text based programming skills.

Inform 7 demonstrated that natural language like syntax could be made to work for domain specific tasks in this case, interactive fiction; its very specialized nature means, however, that it could never be appropriate for general purpose programming.

Python's[@VanRossum2009] is the contemporary standard for readable code in which clarity of syntax is favored over concise notation. The philosophy of this language has been articulated as PEP 20 ("The Zen of Python") and emphasizes readability. Python nonetheless requires knowledge of symbolic conventions (colons, parentheses, indentation rules) that erect obstacles to the absolute beginner[@Pane2001;@Kelleher2005].

ShellLite continues this tradition by bringing together the following:

COBOL's prose like readability without its verbosity or rigid formatting.
Natural language operators of AppleScript without platform lock in or parsing ambiguity

Python's ecosystem access via The Bridge

Modern tooling: IDE support, package manager, web framework Unlike purely educational languages, ShellLite is general purpose and production capable. The fact that shelllite.tech is self hosted proves the language is capable of doing real world web applications, not just educational exercises.

# Quality Assurance

ShellLite ensures code quality by:
**Full suite of tests** for lexer, parser and interpreter components
**Sample programs** showing the language features and typical usage
**Documentation**: available at shelllite.tech and in the GitHub repository

Syntax highlighting & code snippets to boost developer productivity through this VS Code extension. **Actively Maintained:** Regular bug fixes and additions of features are being added based on community input. The interpreter itself features solid error reporting, complete with line numbers and descriptive messages, which greatly enhances debugging necessary for educational use.

# Acknowledgements
This work builds upon the effort of the open source community, notably the maintainers of Python and its ecosystem, on which this project is based. I would like to thank all the early adopters of ShellLite whose comments have been greatly valued during the refinement process of the language design.

# References
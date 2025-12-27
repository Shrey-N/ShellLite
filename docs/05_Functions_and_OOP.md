# Chapter 5: Functions & OOP

As your code gets longer, you'll want to organize it into reusable blocks.

## 1. Functions
A function is a block of code you can call by name.

### Defining Functions
Use `to` or `fn`.

```javascript
to greet name
    say "Hello, " + name

# Calling it
greet "Alice"
```

### Default Arguments
You can set default values for arguments if the user assumes them.
```javascript
to shout text, volume=10
    if volume > 5
        say text.upper()
    else
        say text

shout "hey"      # volume is 10
shout "hey", 1   # volume is 1
```

### Return Values
Use `return` or `give` to send data back.
```javascript
to add_numbers a, b
    give a + b

result = add_numbers 5, 10
say result
```

### Anonymous Functions (Lambdas)
For quick, one-line functions.
```javascript
square = fn x => x * x
say square 5
```

## 2. Object-Oriented Programming (OOP)
OOP allows you to create your own "types" of data. In ShellLite, we use friendly terms:
- **thing**: Class
- **has**: Property (Variables)
- **can**: Method (Functions)

### Defining a Thing
```javascript
thing Car
    has make
    has model
    has speed = 0

    can drive amount
        speed += amount
        say "Vroom! Going " + speed
```

### Creating and Using Objects
Use `new` or `make`.
```javascript
my_car = new Car
my_car.make = "Tesla"
my_car.drive 50
```

### Inheritance
You can create a new Thing that builds upon an old Thing using `extends`.

```javascript
thing SportsCar extends Car
    can turbo
        speed += 100
        say "Turbo boost!"
```

---
[Next: Modules & Standard Library ->](06_Modules_and_StdLib.md)

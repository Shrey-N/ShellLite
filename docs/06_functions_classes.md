# Functions & Object Oriented Programming

## Functions
Define reusable blocks of code.
```javascript
to greet name
    say "Hello " + name

greet("Alice")
```

## Classes (Things)
ShellLite simplifies OOP by calling classes "Things".

```javascript
thing Robot
    has name
    has battery = 100
    
    to speak message
        say name + " says: " + message

# Create instance
bot = make Robot "R2D2" 100
bot.speak("Beep Boop")
```

## Error Handling
```javascript
try
    dangerous_code()
catch err
    say "Something went wrong: " + err
```

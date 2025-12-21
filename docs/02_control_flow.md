# Control Flow

## Conditionals
Use `if`, `else if`, `else`.

```javascript
if x is "red"
    say "Stop"
else if x is "green"
    say "Go"
else
    say "Wait"
```

## Comparisons
You can use natural helpers instead of symbols.

- `is` (==)
- `is not` (!=)
- `is greater than` (>)
- `is less than` (<)
- `and`, `or`, `not`

## Loops

### Range Loop
```javascript
for i in range 1 10
    say i
```

### Iterate List
```javascript
items = ["apple", "banana"]
for item in items
    say item
```

### Infinite Loop
```javascript
forever
    say "Running..."
    wait 1
```

### While Loop (Repeat)
```javascript
repeat 5 times
    say "Echo"
```

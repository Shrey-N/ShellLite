# ShellLite Robot Program
# Demonstrating how structures work in our new language!

structure Robot
    has name
    has battery
    
    to say_hello
        say "Bleep Bloop! I am " + name
        say "Battery: " + battery + "%"
        
    to walk
        say name + " is walking... 🚶"
        battery = battery - 10

# --- Let's use it! ---

# Create two different robots
# Note: In ShellLite, we list 'has' properties in order as arguments
robby is Robot "Robby" 100
sparky is Robot "Sparky" 100

# Make them do things
robby.say_hello
robby.walk
robby.say_hello

say ""
say "---"
say ""

# Notice how Sparky still has 100% battery!
sparky.say_hello

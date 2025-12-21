# Desktop Automation

ShellLite allows you to control your computer directly.

## Files
```javascript
# Download
download "https://example.com/file.zip"

# Archives
compress folder "src" to "src.zip"
extract "src.zip" to "build"

# CSV
users = load csv "data.csv"
save users to csv "backup.csv"
```

## Input / Output
```javascript
copy "Text" to clipboard
pasted = paste from clipboard

press "ctrl+s"
type "Hello"
click at 500, 300

notify "Done" "Script completed"
```

## Scheduling
```javascript
in 5 minutes
    say "Alarm!"

every 1 hour
    say "Hourly check..."
```

# Web Server

ShellLite includes a built-in simple web server.

## Basic Server
```javascript
# Define routes first
on request to "/"
    give "Welcome to ShellLite Web!"

on request to "/api/status"
    give "OK"

# Start listening (Blocking)
listen on port 8080
```

## JSON Conversion
Useful for API responses.
```javascript
data = { status: "active", code: 200 }
json_str = convert data to json
```

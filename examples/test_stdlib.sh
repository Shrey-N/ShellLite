say "Testing Standard Library"

say ""
say "--- Math ---"
# Calculate Sin(PI/2) which is approx 1
# roughly 3.14159 / 2 = 1.5707
val = math_sin 1.57079
say "Sin(PI/2): " + val

root = math_sqrt 16
say "Sqrt(16): " + root

rnd = random
say "Random (0-1): " + rnd

say ""
say "--- Time ---"
now = time_now
say "Timestamp: " + now
say "Date: " + date_str
say "Sleeping for 1 second..."
sleep 1
say "Awake!"

say ""
say "--- HTTP ---"
# We can test with a public API like jsonplaceholder
# Only run if internet available
try
    say "Fetching todo..."
    json_txt = http_get "https://jsonplaceholder.typicode.com/todos/1"
    data = json_parse json_txt
    say "Title: " + data.title
catch e
    say "Network error (expected if offline): " + e

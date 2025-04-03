import os

# List all environment variables, sorted by name
sorted(os.environ.items(), key=lambda y: y[0].lower())

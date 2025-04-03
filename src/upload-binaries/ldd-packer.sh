#!/bin/bash

# Check if the executable is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <executable>"
  exit 1
fi

executable="$1"
# Check if the executable exists
if [ ! -f "$executable" ]; then
  echo "Error: Executable $executable not found."
  exit 1
fi

# Create a temporary directory to store the files and copy the executable to it
temp_dir=$(mktemp -d)
cp "$executable" "$temp_dir"

# Use ldd to get the list of shared libraries and copy them to the temporary directory
ldd "$executable" | awk '{ if (match($3, "/")) { print $3 } }' | while read lib; do
  cp "$lib" "$temp_dir"
done

# Create a zip file containing the executable and its libraries and clean up
zip_file="${executable##*/}_bundle.zip"
zip -r "$zip_file" "$temp_dir"
rm -rf "$temp_dir"

echo "Created zip file: $zip_file"

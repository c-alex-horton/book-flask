#!/bin/bash

# Array of data entries
entries=(
'{
	"name": "Specter of the Abyss",
	"author": "Phineas J. Whipple",
	"genre": "horror",
	"pages": "105",
	"read": false
}'
'{
	"name": "Ethereal Enigma",
	"author": "Madison O'"'"'Rourke",
	"genre": "fantasy",
	"pages": "88",
	"read": true
}'
# Add the remaining entries here
)

# Endpoint URL
endpoint="http://localhost:8000/book"

# Iterate over each entry and curl it
for entry in "${entries[@]}"; do
    curl -X POST -H "Content-Type: application/json" -d "$entry" "$endpoint"
    echo ""  # Optional: Print a newline for better readability between requests
done

#!/bin/bash

# Define the directory path
DIR="./media"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    # Create the directory if it does not exist
    mkdir -p "$DIR"
    echo "Directory 'media' created."
else
    echo "Directory 'media' already exists."
fi
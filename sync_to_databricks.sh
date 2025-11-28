#!/bin/bash

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "Databricks CLI not found. Installing..."
    pip install databricks-cli
fi

# Check if configured
if ! databricks workspace ls / &> /dev/null; then
    echo "Databricks CLI not configured. Please run 'databricks configure --token'"
    exit 1
fi

# Set target path (customize this or pass as argument)
TARGET_PATH=${1:-"/Workspace/Users/$(databricks current-user me | jq -r .userName)/ps_engagement_assistant"}

echo "Syncing databricks/ folder to $TARGET_PATH..."

# Create target directory if it doesn't exist
databricks workspace mkdirs "$TARGET_PATH"

# Import files
for file in databricks/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        extension="${filename##*.}"
        
        case "$extension" in
            py) language="PYTHON" ;;
            sql) language="SQL" ;;
            scala) language="SCALA" ;;
            r) language="R" ;;
            *) language="PYTHON" ;; # Default
        esac
        
        echo "Uploading $filename as $language..."
        databricks workspace import "$file" "$TARGET_PATH/$filename" --overwrite --format SOURCE --language "$language"
    fi
done

echo "Sync complete!"

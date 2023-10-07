#! /bin/bash

set -e

# Check for the correct number of arguments: 1

if [ $# -ne 1 ]; then
    echo "Usage: setup.sh <project_name>"
    exit 1
fi

PROJECT_NAME=$1

# Rename the project folder to $PROJECT_NAME

mv {{PROJECT_NAME}} $PROJECT_NAME

# Rename the project name in all the files, skip the .git folder, the .gitignore file, node_modules, and setup.sh
find . -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./setup.sh" -not -path "./.gitignore" -exec sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" {} \;
#!/bin/bash

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Please provide a version number (e.g. 1.0.0)"
    exit 1
fi

VERSION=$1

# Update version in pyproject.toml
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# Commit the version change
git add pyproject.toml
git commit -m "Bump version to $VERSION"

# Create and push the tag
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin main "v$VERSION"

echo "Released version $VERSION" 
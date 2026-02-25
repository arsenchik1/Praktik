#!/bin/bash

echo "🧪 Running tests..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Run tests
docker-compose run --rm test

# Check test result
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed"
    exit 1
fi

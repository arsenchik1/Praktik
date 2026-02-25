#!/bin/bash

echo "Starting URL Shortener Service..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Start the services
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Show status
docker-compose ps

echo ""
echo "✅ Service started successfully!"
echo "📝 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "To view logs: docker-compose logs -f app"
echo "To stop: docker-compose down"

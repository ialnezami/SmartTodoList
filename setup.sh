#!/bin/bash

echo "🚀 Setting up Smart AI TodoList..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Copying environment file..."
    cp env.example .env
    echo "✅ Environment file created. Please edit .env with your configuration."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/staticfiles
mkdir -p backend/media

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose exec -T backend python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Admin Panel: http://localhost:8000/admin"
echo "   API Documentation: http://localhost:8000/api/docs/"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env file with your OpenAI API key"
echo "   2. Create a superuser: docker-compose exec backend python manage.py createsuperuser"
echo "   3. Start using the application!"
echo ""
echo "🛑 To stop the application: docker-compose down" 
# Smart AI TodoList

An intelligent task management application powered by AI, built with Django REST Framework, Vue.js, and MongoDB.

## 🎯 Overview

Smart AI TodoList is a modern task management application that leverages artificial intelligence to help users organize, prioritize, and complete their tasks more efficiently. The application provides intelligent suggestions, automatic categorization, priority scoring, and smart scheduling capabilities.

## 🚀 Features

### Core Features
- **Task Management**: Create, update, delete, and organize tasks
- **Smart Categorization**: AI-powered automatic task categorization
- **Priority Intelligence**: Intelligent priority scoring based on deadlines, importance, and context
- **Natural Language Processing**: Create tasks using natural language input
- **Smart Scheduling**: AI-suggested optimal time slots for task completion
- **Progress Tracking**: Visual progress indicators and completion analytics
- **Collaborative Tasks**: Share and collaborate on tasks with team members

### AI-Powered Features
- **Intelligent Task Suggestions**: AI recommends related tasks and next steps
- **Deadline Prediction**: Smart deadline estimation based on task complexity
- **Habit Recognition**: Learn user patterns and suggest recurring tasks
- **Context-Aware Reminders**: Location and time-based intelligent notifications
- **Task Dependencies**: Automatic detection of task relationships
- **Productivity Insights**: AI-generated reports on productivity patterns

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js SPA    │    │  Django REST    │    │    MongoDB      │
│   (Frontend)    │◄──►│     API         │◄──►│   (Database)    │
│                 │    │   (Backend)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   AI Services   │
                    │  (OpenAI/Hugging│
                    │     Face)       │
                    └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: MongoDB with MongoEngine ODM
- **AI Integration**: OpenAI API / Hugging Face Transformers
- **Authentication**: JWT Authentication
- **Task Queue**: Celery with Redis
- **API Documentation**: DRF Spectacular (OpenAPI 3.0)

### Frontend
- **Framework**: Vue.js 3 with Composition API
- **State Management**: Pinia
- **UI Components**: Vuetify 3
- **HTTP Client**: Axios
- **Routing**: Vue Router 4
- **Build Tool**: Vite
- **Testing**: Vitest + Vue Test Utils

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)
- **Process Manager**: Gunicorn (production)
- **Caching**: Redis
- **File Storage**: AWS S3 / Local Storage

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- MongoDB 5.0+
- Redis 6.0+
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smart-todolist.git
cd smart-todolist
```

2. **Copy environment variables**
```bash
cp env.example .env
```

3. **Edit .env file with your configurations**
```bash
# Add your OpenAI API key, MongoDB connection string, etc.
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key-here
```

4. **Start all services**
```bash
docker-compose up -d
```

5. **Run initial setup**
```bash
# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Documentation: http://localhost:8000/api/docs/

### Manual Installation

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
export MONGODB_URL="mongodb://localhost:27017/smart_todolist"
export OPENAI_API_KEY="your-openai-api-key"
export SECRET_KEY="your-secret-key"
```

4. **Run migrations and create superuser**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Start development server**
```bash
python manage.py runserver
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set environment variables**
```bash
cp .env.example .env.local
# Edit .env.local with your API endpoints
```

4. **Start development server**
```bash
npm run dev
```

## 📁 Project Structure

```
smart-todolist/
├── backend/
│   ├── apps/
│   │   ├── authentication/
│   │   ├── tasks/
│   │   ├── ai_services/
│   │   ├── notifications/
│   │   └── analytics/
│   ├── config/
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requirements/
│   ├── manage.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── composables/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## 🔧 API Endpoints

### Authentication
```
POST   /api/auth/register/          - User registration
POST   /api/auth/login/             - User login
POST   /api/auth/refresh/           - Token refresh
POST   /api/auth/logout/            - User logout
```

### Tasks
```
GET    /api/tasks/                  - List tasks
POST   /api/tasks/                  - Create task
GET    /api/tasks/{id}/             - Get task details
PUT    /api/tasks/{id}/             - Update task
DELETE /api/tasks/{id}/             - Delete task
POST   /api/tasks/bulk-create/      - Bulk create tasks
```

### AI Services
```
POST   /api/ai/categorize/          - Auto-categorize task
POST   /api/ai/suggest-priority/    - Suggest task priority
POST   /api/ai/parse-natural/       - Parse natural language input
GET    /api/ai/suggestions/         - Get task suggestions
POST   /api/ai/schedule-optimize/   - Optimize task schedule
```

### Analytics
```
GET    /api/analytics/productivity/ - Productivity metrics
GET    /api/analytics/patterns/     - Usage patterns
GET    /api/analytics/insights/     - AI-generated insights
```

## 🧠 AI Features Implementation

### 1. Natural Language Processing
```python
# Example: Parse "Buy groceries tomorrow at 2pm"
{
    "title": "Buy groceries",
    "due_date": "2024-03-15T14:00:00Z",
    "category": "shopping",
    "priority": "medium"
}
```

### 2. Smart Categorization
- Personal, Work, Health, Shopping, Finance
- Custom categories based on user behavior
- Automatic tagging with confidence scores

### 3. Priority Intelligence
- Deadline urgency
- Task complexity estimation
- Historical completion patterns
- User-defined importance factors

### 4. Productivity Insights
- Peak productivity hours
- Task completion patterns
- Bottleneck identification
- Personalized recommendations

## 🔒 Security Features

- JWT-based authentication
- Rate limiting on API endpoints
- Input validation and sanitization
- CORS configuration
- Secure headers implementation
- Environment-based configuration

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report -m
```

### Frontend Tests
```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

## 📊 Database Schema

### Task Document
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  category: String,
  priority: Number,
  status: String, // pending, in_progress, completed
  due_date: Date,
  created_at: Date,
  updated_at: Date,
  user_id: ObjectId,
  ai_metadata: {
    confidence_score: Number,
    suggested_category: String,
    estimated_duration: Number,
    complexity_score: Number
  },
  tags: [String],
  dependencies: [ObjectId],
  attachments: [String]
}
```

## 🚀 Deployment

### Production Setup
1. Set up MongoDB Atlas or self-hosted MongoDB
2. Configure Redis instance
3. Set up AWS S3 for file storage
4. Configure environment variables
5. Deploy using Docker Compose or Kubernetes

### Environment Variables
```bash
# Database
MONGODB_URL=mongodb://localhost:27017/smart_todolist
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-hf-key

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- Hugging Face for transformer models
- Django and Vue.js communities
- MongoDB for flexible document storage

## 📞 Support

For support, email support@smarttodolist.com or join our Slack channel.

## 🗺️ Roadmap

- [x] Core task management
- [x] AI-powered features
- [x] User authentication
- [x] Analytics and insights
- [x] Natural language processing
- [ ] Mobile app (React Native)
- [ ] Offline synchronization
- [ ] Team workspaces
- [ ] Advanced AI models
- [ ] Integration with calendar apps
- [ ] Voice commands
- [ ] Smart home integration
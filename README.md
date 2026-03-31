# 🐾 Take A Paw - Pet Adoption Platform
A Tinder-style pet adoption web application built with Flask, PostgreSQL, and modern CI/CD practices.

## 🚀 Features
- **Tinder-style Swiping**: Swipe right to like pets, left to skip.
- **Compatibility Quiz**: Find pets that match your lifestyle.
- **Favorites System**: Save pets you're interested in.
- **Admin Dashboard**: Manage pets and track adoptions.
- **Responsive Design**: Works on desktop and mobile.

## 🛠 Tech Stack
- **Backend**: Flask, Python
- **Database**: PostgreSQL (Neon)
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render

## 📦 Quick Start

### 🌐 Production Environment
- **Live Application**: [https://take-a-paw.onrender.com](https://take-a-paw.onrender.com)
- **Health Monitor**: [https://take-a-paw.onrender.com/health](https://take-a-paw.onrender.com/health)
- **API Status**: [https://take-a-paw.onrender.com/api/status](https://take-a-paw.onrender.com/api/status)

### 🏗️ Architecture
```

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   GitHub Actions │    │   Render        │
│   Repository    │───▶│   CI/CD Pipeline │───▶│   Production    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
│                        │                        │
│                        │                        │
▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Code Changes  │    │   Auto Testing   │    │   Auto Deploy   │
│   & Commits     │    │   & Building     │    │   & Scaling     │
└─────────────────┘    └──────────────────┘    └─────────────────┘

````

## 🛠 Quick Start

### Prerequisites
- Python 3.12+
- Docker
- Git

### Local Development

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/your-username/takeapaw.git
   cd takeapaw
2. **Virtual Environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .venv\Scripts\Activate.ps1 # Windows using PowerShell
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**:

   ```bash
   cd src
   python app.py
   ```

   Visit: [http://localhost:5000](http://localhost:5000)

### Docker Development

1. **Build image**:

   ```bash
   docker build -t takeapaw:latest .
   ```

2. **Run container**:

   ```bash
   docker run -p 5000:5000 takeapaw:latest
   ```

3. **Or with Docker Compose**:

   ```bash
   docker-compose up
   ```

### 🧪 Testing

1. **Run all tests**:

   ```bash
   cd tests
   pytest test_app.py -v
   ```

2. **Run with coverage**:

   ```bash
   pytest --cov=src --cov-report=html
   ```

3. **Specific test category**:

   ```bash
   pytest tests/test_app.py::test_health_endpoint -v
   ```

## 📁 Project Structure

```
takeapaw/
├── .github/workflows/          # CI/CD Automation
│   ├── ci.yml                  # Continuous Integration
│   └── cd.yml                  # Continuous Deployment
├── src/                        # Application Source
│   ├── static/
│   │   └── style.css           # Styling
│   ├── templates/              # Jinja2 Templates
│   │   ├── base.html           # Base Layout
│   │   ├── index.html          # Homepage
│   │   ├── pet_detail.html     # Pet Profiles
│   │   ├── adopt_form.html     # Adoption Forms
│   │   ├── quiz.html           # Matching Quiz
│   │   ├── admin.html          # Admin Dashboard
│   │   └── ...                 # Other Templates
│   ├── app.py                  # Flask Application
│   └── requirements.txt        # Dependencies
├── tests/                      # Test Suite
│   └── test_app.py             # Application Tests
├── Dockerfile                  # Container Definition
├── docker-compose.yml          # Multi-container Setup
├── requirements.txt            # Project Dependencies
└── README.md                   # Documentation
```

## 🔌 API Endpoints

### Application Routes

* `GET /` - Homepage with pet listings
* `GET /search` - Advanced pet search
* `GET /pet/<id>` - Individual pet profiles
* `GET /adopt/<id>` - Adoption application forms
* `GET /quiz` - Personality matching quiz
* `GET /favorites` - User favorite pets
* `GET /admin` - Administration dashboard

### JSON APIs

* `GET /api/pets` - All available pets (JSON)
* `GET /api/status` - System health and API status
* `GET /health` - Health check endpoint
* `GET /debug` - System debugging information

## 🚀 Automated Deployment (CI/CD)

### Pipeline Flow

1. **Code Push** → Trigger GitHub Actions
2. **CI Pipeline** → Run automated tests (pytest)
3. **CD Pipeline** → Build Docker image → Push to GHCR
4. **Auto-Deploy** → Render detects changes → Deploys automatically
5. **Live Update** → Application updated in production

### Manual Trigger Demo

To make a visible change for presentation:

```bash
echo "# Demo auto-deployment" >> demo.txt
git add .
git commit -m "demo: testing CI/CD pipeline"
git push origin main
```

## 🔐 Admin Panel

Take A Paw includes a fully featured **Admin Panel** for managing the platform.

### Admin Login
🔑 **Admin Login Page:**  
https://take-a-paw.onrender.com/admin/login

### Admin Features
The admin dashboard allows you to:

- Add, edit, and remove pets  
- View user accounts  
- Monitor adoption statistics  
- Manage favorites and listings  
- Access platform-wide metrics  
- Moderate system activity  

> ⚠️ Note: In demo mode, an admin session may be automatically enabled for easier access during testing.

## ⚙️ Configuration

### Environment Variables

* `SECRET_KEY=your-secret-key-here`
* `FLASK_ENV=production`
* `CAT_API_KEY=your-cat-api-key`
* `DOG_API_KEY=your-dog-api-key`

### Production Settings

* **WSGI Server**: Gunicorn
* **Process Manager**: Render
* **Health Checks**: Automatic monitoring
* **Logging**: Structured application logs

## 🔒 Security Features

* Non-root Docker user execution
* Environment variable configuration
* SQL injection prevention
* XSS protection through template escaping
* Secure headers configuration

## 📊 Monitoring & Analytics

### Health Monitoring

* **Internal**: Render application logs and metrics
* **External**: UptimeRobot with 5-minute checks
* **Custom**: `/health` endpoint for service status

### Performance Metrics

* Response time tracking
* Error rate monitoring
* Uptime statistics
* Deployment success rates

## 🚨 Rollback Procedures

If deployment issues occur:

1. Access Render Dashboard → **Events** tab
2. Select Stable Deployment → **Click "Rollback"**
3. Confirm Action → System reverts instantly
4. **Auto-Deploy Disabled** → Prevents repeated issues
5. Re-enable After Fix → Settings → Auto-Deploy → Yes

## 👥 Collaborators

This project was created and maintained by:

- **Shahin Alakparov** – [GitHub Profile](https://github.com/shahin1717)
- **Nazrin Aliyeva** – [GitHub Profile](https://github.com/Lachi7)
- **Fidan Alizada** – [GitHub Profile](https://github.com/Fidannnnn)



## 🤝 Contributing

We welcome contributions! Please see our workflow:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/improvement`
3. **Commit changes**: `git commit -m 'Add some improvement'`
4. **Push to branch**: `git push origin feature/improvement`
5. **Open a Pull Request**

### Development Standards

* **Run tests before committing**:

  ```bash
  pytest
  ```

* **Check code quality**:

  ```bash
  flake8 src/ tests/
  ```

* **Format code**:

  ```bash
  black src/ tests/
  ```

## 🐛 Troubleshooting

### Common Issues

#### Docker Build Failures

* Clean build:

  ```bash
  docker system prune
  docker build --no-cache -t takeapaw:latest .
  ```

#### Port Conflicts

* Resolve conflicts if port 5000 is in use.

### Development

```bash
git clone https://github.com/your-username/take-a-paw.git
cd take-a-paw
pip install -r requirements.txt
cd src && python run.py
```

### Docker

```bash
docker build -t takeapaw .
docker run -p 5000:5000 takeapaw
```


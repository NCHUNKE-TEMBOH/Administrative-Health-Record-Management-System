# medicare Health Record Management System - Deployment Guide

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed on your system
- Git (optional, for cloning the repository)

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd Administrative_Hospital_Management_System
   ```

2. **Start the application**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Open your browser and navigate to: `http://localhost:5001`
   - The application will be available with a pre-initialized database

### Option 2: Using Docker Build

1. **Build the Docker image**:
   ```bash
   docker build -t medicare:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 5001:5001 --name medicare-app medicare:latest
   ```

3. **Access the application**:
   - Open your browser and navigate to: `http://localhost:5001`

## 🔧 Manual Installation

### Prerequisites
- Python 3.11 or higher
- SQLite3

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Administrative_Hospital_Management_System
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   cd scripts
   python init_users.py
   cd ..
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   - Open your browser and navigate to: `http://localhost:5001`

## 🏥 Default User Accounts

The system comes with pre-configured user accounts for testing:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Admin | admin | admin123 | Full system access |
| Doctor | doctor | doctor123 | Patient records, prescriptions |
| Nurse | nurse | nurse123 | Assigned patients, vital signs |
| Lab Technician | labtech | lab123 | Lab tests, results |
| Pharmacist | pharmacist | pharma123 | Prescriptions, dispensing |
| Patient | patient | patient123 | Personal health records |

## 🌐 Production Deployment

### Environment Variables

For production deployment, set the following environment variables:

```bash
export FLASK_ENV=production
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5001
```

### Using a Production WSGI Server

For production, use a proper WSGI server like Gunicorn:

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

### Nginx Reverse Proxy (Optional)

Create an Nginx configuration file:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Security Considerations

1. **Change Default Passwords**: Update all default user passwords before production use
2. **Secret Key**: Change the Flask secret key in `config.json`
3. **Database Security**: Implement proper database backup and security measures
4. **HTTPS**: Use HTTPS in production with proper SSL certificates
5. **Firewall**: Configure firewall rules to restrict access

## 📊 Health Monitoring

The application includes health check endpoints:

- **Health Check**: `GET /login.html` (returns 200 if healthy)
- **Docker Health Check**: Automatically configured in the Dockerfile

## 🔄 Updates and Maintenance

### Updating the Application

1. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

2. **Rebuild Docker image**:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### Database Backup

```bash
# Backup database
sqlite3 database/database.db ".backup backup_$(date +%Y%m%d_%H%M%S).db"

# Restore database
sqlite3 database/database.db ".restore backup_file.db"
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 5001
   lsof -i :5001
   # Kill the process
   kill -9 <PID>
   ```

2. **Database permission issues**:
   ```bash
   # Fix database permissions
   chmod 664 database/database.db
   chown -R appuser:appuser database/
   ```

3. **Docker container not starting**:
   ```bash
   # Check container logs
   docker logs medicare-app
   ```

## 📞 Support

For support and issues:
- Check the application logs
- Review the troubleshooting section
- Contact the development team

## 🔗 Useful Commands

```bash
# View running containers
docker ps

# Stop the application
docker-compose down

# View application logs
docker-compose logs -f

# Access container shell
docker exec -it medicare-app /bin/bash

# Check application status
curl -f http://localhost:5001/login.html
```

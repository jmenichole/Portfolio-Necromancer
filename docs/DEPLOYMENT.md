# Deployment Guide - Portfolio Necromancer

This guide covers various deployment options for the Portfolio Necromancer fullstack application.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Deployments](#cloud-deployments)

## Local Development

### Quick Start

```bash
# Install dependencies
pip install -e .

# Run the development server
python -m portfolio_necromancer.api.server

# Access the application
# Dashboard: http://localhost:5000
# API: http://localhost:5000/api/health
```

### Custom Configuration

```bash
# Run on different port
python -m portfolio_necromancer.api.server --port 8080

# Enable debug mode
python -m portfolio_necromancer.api.server --debug

# Bind to specific host
python -m portfolio_necromancer.api.server --host 127.0.0.1
```

## Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t portfolio-necromancer .

# Run the container
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret-key-here" \
  --name portfolio-necromancer \
  portfolio-necromancer

# View logs
docker logs -f portfolio-necromancer

# Stop the container
docker stop portfolio-necromancer
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Docker Compose with Custom Configuration

Create a `.env` file:

```env
SECRET_KEY=your-random-secret-key-change-this
FLASK_ENV=production
```

Then run:

```bash
docker-compose up -d
```

### Persistent Data

The docker-compose.yml includes volume mappings for:
- `./config:/app/config` - Configuration files
- `./generated_portfolios:/app/generated_portfolios` - Generated portfolios

Your data will persist across container restarts.

## Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 'portfolio_necromancer.api.app:create_app()'

# With better configuration
gunicorn \
  --workers 4 \
  --bind 0.0.0.0:5000 \
  --timeout 300 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  'portfolio_necromancer.api.app:create_app()'
```

### Systemd Service

Create `/etc/systemd/system/portfolio-necromancer.service`:

```ini
[Unit]
Description=Portfolio Necromancer API Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/portfolio-necromancer
Environment="PATH=/opt/portfolio-necromancer/venv/bin"
Environment="SECRET_KEY=your-secret-key"
ExecStart=/opt/portfolio-necromancer/venv/bin/gunicorn \
  --workers 4 \
  --bind 0.0.0.0:5000 \
  --timeout 300 \
  'portfolio_necromancer.api.app:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable portfolio-necromancer
sudo systemctl start portfolio-necromancer
sudo systemctl status portfolio-necromancer
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/portfolio-necromancer`:

```nginx
server {
    listen 80;
    server_name portfolio.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for portfolio generation
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Serve static files directly
    location /static {
        alias /opt/portfolio-necromancer/src/portfolio_necromancer/api/static;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/portfolio-necromancer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d portfolio.yourdomain.com

# Auto-renewal is configured by default
# Test renewal
sudo certbot renew --dry-run
```

## Cloud Deployments

### Heroku

1. Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 300 'portfolio_necromancer.api.app:create_app()'
```

2. Deploy:
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.9 portfolio-necromancer
```

3. Create environment:
```bash
eb create portfolio-necromancer-env
```

4. Deploy:
```bash
eb deploy
```

### Google Cloud Run

1. Create `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/portfolio-necromancer', '.']
images:
  - 'gcr.io/$PROJECT_ID/portfolio-necromancer'
```

2. Deploy:
```bash
gcloud builds submit --config cloudbuild.yaml
gcloud run deploy portfolio-necromancer \
  --image gcr.io/PROJECT_ID/portfolio-necromancer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### DigitalOcean App Platform

1. Create `app.yaml`:
```yaml
name: portfolio-necromancer
services:
  - name: api
    github:
      repo: yourusername/Portfolio-Necromancer
      branch: main
    build_command: pip install -e .
    run_command: gunicorn -w 4 -b 0.0.0.0:8080 --timeout 300 'portfolio_necromancer.api.app:create_app()'
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    http_port: 8080
    envs:
      - key: SECRET_KEY
        value: ${SECRET_KEY}
```

2. Deploy via UI or CLI:
```bash
doctl apps create --spec app.yaml
```

## Environment Variables

### Required

- `SECRET_KEY` - Flask secret key for sessions (required in production)

### Optional

- `FLASK_ENV` - Set to `production` for production deployment
- `PORT` - Port number (default: 5000)
- `WORKERS` - Number of worker processes for gunicorn

### Setting Environment Variables

**Linux/Mac:**
```bash
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
```

**Windows:**
```cmd
set SECRET_KEY=your-secret-key
set FLASK_ENV=production
```

**Docker:**
```bash
docker run -e SECRET_KEY="your-secret-key" -e FLASK_ENV="production" portfolio-necromancer
```

## Security Best Practices

1. **Change the SECRET_KEY**
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Use HTTPS in production**
   - Use Let's Encrypt for free SSL certificates
   - Configure nginx/Apache to redirect HTTP to HTTPS

3. **Set secure CORS origins**
   - Modify `app.py` to restrict CORS origins in production

4. **Use environment variables**
   - Never commit secrets to git
   - Use `.env` files (add to `.gitignore`)

5. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

6. **Enable rate limiting** (optional)
   ```bash
   pip install Flask-Limiter
   ```

## Monitoring and Logging

### Application Logs

```bash
# View logs in real-time
tail -f /var/log/portfolio-necromancer.log

# With systemd
journalctl -u portfolio-necromancer -f

# With Docker
docker logs -f portfolio-necromancer
```

### Health Checks

The application includes a health endpoint:
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-11-21T10:00:00.000000+00:00"
}
```

### Monitoring Services

Consider integrating with:
- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **Datadog** - Infrastructure monitoring
- **Prometheus + Grafana** - Metrics and visualization

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Permission Denied

```bash
# Run on port > 1024 without sudo
python -m portfolio_necromancer.api.server --port 8080
```

### Out of Memory

```bash
# Reduce number of workers
gunicorn -w 2 ...

# Or increase container/VM memory
```

### Slow Portfolio Generation

```bash
# Increase timeout
gunicorn --timeout 600 ...
```

## Scaling

### Horizontal Scaling

Use a load balancer with multiple instances:

```nginx
upstream portfolio_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    location / {
        proxy_pass http://portfolio_backend;
    }
}
```

### Vertical Scaling

Increase worker processes:
```bash
gunicorn -w 8 ...  # More workers for more CPU cores
```

## Backup and Recovery

### Backup Generated Portfolios

```bash
# Create backup
tar -czf portfolios-backup-$(date +%Y%m%d).tar.gz generated_portfolios/

# Restore backup
tar -xzf portfolios-backup-YYYYMMDD.tar.gz
```

### Database Backup (if using future DB features)

```bash
# SQLite backup
cp portfolio.db portfolio.db.backup
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/jmenichole/Portfolio-Necromancer/issues
- Documentation: Check the README.md and API_GUIDE.md

---

**Ready to deploy!** Choose the method that best fits your needs and infrastructure. 🚀

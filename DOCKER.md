# Docker Deployment Guide

## Running with Docker

The Talk to Jesus AI application can be run in Docker for easier deployment and consistency across environments.

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

### Quick Start with Docker

#### Option 1: Using Docker Compose (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Open your browser to http://localhost:5000

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

#### Option 2: Using Docker CLI

1. **Build the Docker image:**
   ```bash
   docker build -t talktojesus-ai .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 5000:5000 --name talktojesus-ai talktojesus-ai
   ```

3. **Access the application:**
   - Open your browser to http://localhost:5000

4. **View logs:**
   ```bash
   docker logs -f talktojesus-ai
   ```

5. **Stop the container:**
   ```bash
   docker stop talktojesus-ai
   docker rm talktojesus-ai
   ```

### Environment Variables

You can customize the application using environment variables:

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_DEBUG=False \
  -e PORT=5000 \
  -e SECRET_KEY=your-secret-key-here \
  --name talktojesus-ai \
  talktojesus-ai
```

Or with docker-compose, create a `.env` file:

```env
FLASK_DEBUG=False
PORT=5000
SECRET_KEY=your-secret-key-here
```

### Health Check

The Docker container includes a health check that monitors the `/health` endpoint:

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' talktojesus-ai
```

### Using a Different Port

To run on a different port (e.g., 8080):

```bash
docker run -d -p 8080:5000 --name talktojesus-ai talktojesus-ai
```

Then access at http://localhost:8080

### Production Deployment

For production deployment with Docker:

1. **Set a secure secret key:**
   ```bash
   export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
   ```

2. **Run with production settings:**
   ```bash
   docker run -d \
     -p 5000:5000 \
     -e FLASK_DEBUG=False \
     -e SECRET_KEY=$SECRET_KEY \
     --restart unless-stopped \
     --name talktojesus-ai \
     talktojesus-ai
   ```

3. **Use a reverse proxy (nginx/traefik) for SSL/TLS**

### Docker Commands Cheat Sheet

```bash
# Build image
docker build -t talktojesus-ai .

# Run container
docker run -d -p 5000:5000 --name talktojesus-ai talktojesus-ai

# View logs
docker logs talktojesus-ai
docker logs -f talktojesus-ai  # Follow logs

# Execute commands in container
docker exec -it talktojesus-ai bash

# Stop container
docker stop talktojesus-ai

# Start container
docker start talktojesus-ai

# Remove container
docker rm talktojesus-ai

# Remove image
docker rmi talktojesus-ai

# View container stats
docker stats talktojesus-ai

# Inspect container
docker inspect talktojesus-ai
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Stop and remove all containers, networks
docker-compose down -v
```

### Troubleshooting Docker Issues

#### Container won't start
```bash
# Check logs
docker logs talktojesus-ai

# Check if port is already in use
lsof -i :5000  # On macOS/Linux
netstat -ano | findstr :5000  # On Windows
```

#### Can't access localhost:5000
1. Ensure container is running: `docker ps`
2. Check port mapping: `docker port talktojesus-ai`
3. Try 127.0.0.1:5000 instead of localhost:5000
4. Check firewall settings

#### Container keeps restarting
```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' talktojesus-ai

# View detailed logs
docker logs --tail 50 talktojesus-ai
```

### Multi-Stage Build (Advanced)

For smaller production images, use multi-stage builds. Edit the Dockerfile:

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python3", "app.py"]
```

### Kubernetes Deployment (Optional)

For Kubernetes deployment, create a deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: talktojesus-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: talktojesus-ai
  template:
    metadata:
      labels:
        app: talktojesus-ai
    spec:
      containers:
      - name: talktojesus-ai
        image: talktojesus-ai:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_DEBUG
          value: "False"
---
apiVersion: v1
kind: Service
metadata:
  name: talktojesus-ai
spec:
  selector:
    app: talktojesus-ai
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

## Benefits of Using Docker

✅ **Consistent Environment** - Works the same on all machines  
✅ **Easy Deployment** - One command to run  
✅ **Isolated Dependencies** - No conflicts with system packages  
✅ **Portable** - Run anywhere Docker is installed  
✅ **Scalable** - Easy to deploy multiple instances  
✅ **Production Ready** - Includes health checks and proper security  

## Support

For Docker-specific issues, check:
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

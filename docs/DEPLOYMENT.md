# Deployment Guide for Production

## Prerequisites

- Docker installed
- AWS CLI configured (for AWS deployment)
- Python 3.10+
- Linux/Unix server (recommended)

## Local Docker Deployment

### 1. Build Docker Image

```bash
docker build -t medical-chatbot:latest .
docker tag medical-chatbot:latest medical-chatbot:v1.0
```

### 2. Run Container Locally

```bash
docker run -d \
  -p 5000:5000 \
  --env-file .env \
  --name medical-chatbot \
  medical-chatbot:latest
```

### 3. Verify Container

```bash
docker ps
docker logs -f medical-chatbot
curl http://localhost:5000/health
```

## AWS Deployment (ECS)

### 1. Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name medical-chatbot --region us-east-1

# Get ECR login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag medical-chatbot:v1.0 <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:v1.0
docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:v1.0
```

### 2. Create ECS Task Definition

Create `task-definition.json`:

```json
{
  "family": "medical-chatbot",
  "containerDefinitions": [
    {
      "name": "medical-chatbot",
      "image": "<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:v1.0",
      "memory": 512,
      "cpu": 256,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

### 3. Register Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 4. Create and Run Service

```bash
aws ecs create-service \
  --cluster default \
  --service-name medical-chatbot-service \
  --task-definition medical-chatbot:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

## Kubernetes Deployment

### 1. Create Deployment Manifest

Create `kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medical-chatbot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: medical-chatbot
  template:
    metadata:
      labels:
        app: medical-chatbot
    spec:
      containers:
      - name: medical-chatbot
        image: medical-chatbot:v1.0
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
```

### 2. Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get deployments
```

## Monitoring

### Health Check

```bash
curl http://<your-domain>/health
```

### Logs

```bash
# Docker
docker logs -f medical-chatbot

# Kubernetes
kubectl logs -f deployment/medical-chatbot

# AWS CloudWatch
aws logs tail /ecs/medical-chatbot --follow
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

```bash
sudo certbot certonly --standalone -d yourdomain.com
```

### Configure Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Container won't start

```bash
docker logs medical-chatbot
docker run -it medical-chatbot bash  # Debug mode
```

### API key errors

- Verify `.env` file is mounted
- Check environment variables: `docker exec medical-chatbot env`

### Performance issues

- Check resource allocation: `docker stats`
- Monitor API response time with APM tools
- Optimize database queries

## Scaling

### Horizontal Scaling (Multiple Instances)

```bash
# Docker Compose with scaling
docker-compose up -d --scale web=3

# Kubernetes auto-scaling
kubectl autoscale deployment medical-chatbot --min=2 --max=10 --cpu-percent=80
```

## Backup & Recovery

### Database Backup

```bash
# Backup Pinecone index (manual export)
# Document index snapshot regularly

# Backup application data
docker exec medical-chatbot backup_data.sh
```

## Performance Optimization

- Enable response caching
- Use CDN for static assets
- Implement rate limiting
- Monitor and optimize database queries

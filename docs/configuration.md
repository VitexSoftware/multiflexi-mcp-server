# Configuration Examples

This document provides various configuration examples for different deployment scenarios.

## Basic Configuration

### Development Environment

```bash
# .env
MULTIFLEXI_HOST=http://localhost:8080
MULTIFLEXI_USERNAME=devuser
MULTIFLEXI_PASSWORD=devpass
MULTIFLEXI_DEBUG=true
MULTIFLEXI_VERIFY_SSL=false
```

### Production Environment

```bash
# .env
MULTIFLEXI_HOST=https://multiflexi.yourcompany.com
MULTIFLEXI_USERNAME=prod-service-account
MULTIFLEXI_PASSWORD=secure-production-password
MULTIFLEXI_VERIFY_SSL=true
MULTIFLEXI_TIMEOUT=60
MULTIFLEXI_MAX_RETRIES=5
MULTIFLEXI_DEBUG=false
```

### Testing Environment

```bash
# .env
MULTIFLEXI_HOST=https://test-multiflexi.yourcompany.com
MULTIFLEXI_USERNAME=testuser
MULTIFLEXI_PASSWORD=testpass
MULTIFLEXI_VERIFY_SSL=true
MULTIFLEXI_TIMEOUT=30
MULTIFLEXI_DEBUG=true
```

## Docker Configuration

### Docker Compose

```yaml
version: '3.8'
services:
  multiflexi-mcp-server:
    image: multiflexi/mcp-server:latest
    environment:
      - MULTIFLEXI_HOST=https://multiflexi.example.com
      - MULTIFLEXI_USERNAME=service-account
      - MULTIFLEXI_PASSWORD_FILE=/run/secrets/multiflexi_password
      - MULTIFLEXI_VERIFY_SSL=true
      - MULTIFLEXI_TIMEOUT=60
    secrets:
      - multiflexi_password
    ports:
      - "3001:3001"
    restart: unless-stopped

secrets:
  multiflexi_password:
    external: true
```

### Kubernetes Configuration

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: multiflexi-credentials
type: Opaque
stringData:
  username: service-account
  password: your-secure-password
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: multiflexi-config
data:
  MULTIFLEXI_HOST: "https://multiflexi.example.com"
  MULTIFLEXI_VERIFY_SSL: "true"
  MULTIFLEXI_TIMEOUT: "60"
  MULTIFLEXI_MAX_RETRIES: "5"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multiflexi-mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: multiflexi-mcp-server
  template:
    metadata:
      labels:
        app: multiflexi-mcp-server
    spec:
      containers:
      - name: multiflexi-mcp-server
        image: multiflexi/mcp-server:latest
        env:
        - name: MULTIFLEXI_USERNAME
          valueFrom:
            secretKeyRef:
              name: multiflexi-credentials
              key: username
        - name: MULTIFLEXI_PASSWORD
          valueFrom:
            secretKeyRef:
              name: multiflexi-credentials
              key: password
        envFrom:
        - configMapRef:
            name: multiflexi-config
        ports:
        - containerPort: 3001
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

## Authentication Methods

### Basic Authentication

```bash
MULTIFLEXI_USERNAME=your-username
MULTIFLEXI_PASSWORD=your-password
```

### Token-based Authentication (if supported)

```bash
MULTIFLEXI_TOKEN=your-api-token
# Note: Implementation would need to be added for token auth
```

## SSL/TLS Configuration

### Production with SSL Verification

```bash
MULTIFLEXI_HOST=https://secure.multiflexi.com
MULTIFLEXI_VERIFY_SSL=true
```

### Development with Self-signed Certificates

```bash
MULTIFLEXI_HOST=https://dev.multiflexi.com
MULTIFLEXI_VERIFY_SSL=false
# Only disable SSL verification in development!
```

### Custom CA Certificate (if needed)

```bash
MULTIFLEXI_HOST=https://internal.multiflexi.com
MULTIFLEXI_VERIFY_SSL=true
MULTIFLEXI_CA_CERT_PATH=/path/to/ca-cert.pem
# Note: Implementation would need to be added for custom CA
```

## Performance Tuning

### High-throughput Configuration

```bash
MULTIFLEXI_HOST=https://multiflexi.example.com
MULTIFLEXI_TIMEOUT=120
MULTIFLEXI_MAX_RETRIES=10
MULTIFLEXI_CONNECTION_POOL_SIZE=20
# Note: Connection pool size would need implementation
```

### Low-latency Configuration

```bash
MULTIFLEXI_HOST=https://multiflexi.example.com
MULTIFLEXI_TIMEOUT=5
MULTIFLEXI_MAX_RETRIES=1
MULTIFLEXI_CONNECTION_TIMEOUT=2
# Note: Connection timeout would need implementation
```

## Monitoring and Logging

### Debug Configuration

```bash
MULTIFLEXI_DEBUG=true
MULTIFLEXI_LOG_LEVEL=DEBUG
MULTIFLEXI_LOG_FORMAT=detailed
# Note: LOG_LEVEL and LOG_FORMAT would need implementation
```

### Production Logging

```bash
MULTIFLEXI_DEBUG=false
MULTIFLEXI_LOG_LEVEL=INFO
MULTIFLEXI_LOG_FORMAT=json
MULTIFLEXI_LOG_FILE=/var/log/multiflexi-mcp-server.log
# Note: Additional logging options would need implementation
```

## Load Balancing

### Multiple Backend Configuration

```bash
MULTIFLEXI_HOSTS=https://mf1.example.com,https://mf2.example.com,https://mf3.example.com
MULTIFLEXI_LOAD_BALANCE_METHOD=round_robin
# Note: Multiple hosts support would need implementation
```

## Security Best Practices

### Secure Password Management

```bash
# Use environment files with restricted permissions
chmod 600 .env

# Or use Docker secrets, Kubernetes secrets, etc.
# Never hardcode passwords in configuration files
```

### Network Security

```bash
# Use internal networks when possible
MULTIFLEXI_HOST=https://internal-multiflexi.company.internal

# Enable SSL verification in production
MULTIFLEXI_VERIFY_SSL=true

# Use service accounts with minimal permissions
MULTIFLEXI_USERNAME=mcp-server-service-account
```
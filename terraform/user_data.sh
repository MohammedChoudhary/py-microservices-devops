#!/bin/bash

# Update system
apt-get update -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application directory
mkdir -p /home/ubuntu/app
chown ubuntu:ubuntu /home/ubuntu/app

# Create docker-compose.yml file for the application
cat > /home/ubuntu/app/docker-compose.yml << 'EOF'
services:
  postgres:
    image: postgres:13-alpine
    container_name: devops_postgres
    environment:
      POSTGRES_DB: devops_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  backend:
    image: mohxmd77/devops-backend:latest
    container_name: devops_backend
    environment:
      DB_HOST: postgres
      DB_NAME: devops_db
      DB_USER: postgres
      DB_PASS: password123
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  frontend:
    image: mohxmd77/devops-frontend:latest
    container_name: devops_frontend
    environment:
      BACKEND_URL: http://backend:5000/api/data
    ports:
      - "8080:80"
    depends_on:
      - backend
    restart: unless-stopped

  logger:
    image: mohxmd77/devops-logger:latest
    container_name: devops_logger
    environment:
      BACKEND_URL: http://backend:5000
    volumes:
      - logger_logs:/app/logs
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  logger_logs:
EOF

# Create database initialization file
cat > /home/ubuntu/app/init.sql << 'EOF'
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Wilson', 'bob@example.com')
ON CONFLICT (email) DO NOTHING;
EOF

# Set ownership
chown -R ubuntu:ubuntu /home/ubuntu/app

# Start services
cd /home/ubuntu/app
sudo -u ubuntu docker-compose pull
sudo -u ubuntu docker-compose up -d

# Create a simple status check script
cat > /home/ubuntu/check-status.sh << 'EOF'
#!/bin/bash
echo "=== Docker Container Status ==="
docker ps
echo ""
echo "=== Application Health Check ==="
echo "Frontend: http://$(curl -s http://checkip.amazonaws.com/):8080"
echo "Backend API: http://$(curl -s http://checkip.amazonaws.com/):5000/api/data"
EOF

chmod +x /home/ubuntu/check-status.sh
chown ubuntu:ubuntu /home/ubuntu/check-status.sh
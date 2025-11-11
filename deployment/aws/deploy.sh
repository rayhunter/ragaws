#!/bin/bash
# Deployment script for txtai RAG system on AWS ECS

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-076656108307}
AWS_PROFILE=${AWS_PROFILE:-rays-admin-profile}
ECR_BACKEND_REPO=txtai-rag-backend
ECR_FRONTEND_REPO=txtai-rag-frontend
ECS_CLUSTER=txtai-rag-cluster
FRONTEND_API_URL=${FRONTEND_API_URL:-}

echo "🚀 Starting deployment..."

if [ -z "${FRONTEND_API_URL}" ]; then
  echo "❌ FRONTEND_API_URL environment variable is not set."
  echo "   Set it to the publicly reachable backend URL (e.g. https://api.example.com) before deploying."
  exit 1
fi

# Step 1: Build and push backend Docker image
echo "📦 Building backend Docker image..."
cd backend
docker build -t ${ECR_BACKEND_REPO}:latest .
docker tag ${ECR_BACKEND_REPO}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND_REPO}:latest

echo "📤 Pushing backend image to ECR..."
aws ecr get-login-password --region ${AWS_REGION} --profile ${AWS_PROFILE} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND_REPO}:latest
cd ..

# Step 2: Build and push frontend Docker image
echo "📦 Building frontend Docker image..."
cd frontend
docker build \
  --build-arg VITE_API_URL=${FRONTEND_API_URL} \
  -t ${ECR_FRONTEND_REPO}:latest .
docker tag ${ECR_FRONTEND_REPO}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND_REPO}:latest

echo "📤 Pushing frontend image to ECR..."
aws ecr get-login-password --region ${AWS_REGION} --profile ${AWS_PROFILE} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND_REPO}:latest
cd ..

# Step 3: Update ECS task definitions
echo "📝 Updating ECS task definitions..."
# Replace placeholders in task definitions
sed -i.bak "s/YOUR_ACCOUNT_ID/${AWS_ACCOUNT_ID}/g" deployment/aws/ecs-backend-task-definition.json
sed -i.bak "s/YOUR_ACCOUNT_ID/${AWS_ACCOUNT_ID}/g" deployment/aws/ecs-frontend-task-definition.json

# Register task definitions
aws ecs register-task-definition \
  --cli-input-json file://deployment/aws/ecs-backend-task-definition.json \
  --region ${AWS_REGION} \
  --profile ${AWS_PROFILE}

aws ecs register-task-definition \
  --cli-input-json file://deployment/aws/ecs-frontend-task-definition.json \
  --region ${AWS_REGION} \
  --profile ${AWS_PROFILE}

# Step 4: Update ECS services
echo "🔄 Updating ECS services..."
aws ecs update-service \
  --cluster ${ECS_CLUSTER} \
  --service txtai-rag-backend-service \
  --force-new-deployment \
  --region ${AWS_REGION} \
  --profile ${AWS_PROFILE} > /dev/null

aws ecs update-service \
  --cluster ${ECS_CLUSTER} \
  --service txtai-rag-frontend-service \
  --force-new-deployment \
  --region ${AWS_REGION} \
  --profile ${AWS_PROFILE} > /dev/null

echo "✅ Deployment complete!"
echo "📊 Monitor deployment status:"
echo "   aws ecs describe-services --cluster ${ECS_CLUSTER} --services txtai-rag-backend-service txtai-rag-frontend-service --region ${AWS_REGION} --profile ${AWS_PROFILE}"

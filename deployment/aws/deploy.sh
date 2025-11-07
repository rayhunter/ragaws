#!/bin/bash
# Deployment script for txtai RAG system on AWS ECS

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-YOUR_ACCOUNT_ID}
ECR_BACKEND_REPO=txtai-rag-backend
ECR_FRONTEND_REPO=txtai-rag-frontend
ECS_CLUSTER=txtai-rag-cluster

echo "🚀 Starting deployment..."

# Step 1: Build and push backend Docker image
echo "📦 Building backend Docker image..."
cd backend
docker build -t ${ECR_BACKEND_REPO}:latest .
docker tag ${ECR_BACKEND_REPO}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND_REPO}:latest

echo "📤 Pushing backend image to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND_REPO}:latest
cd ..

# Step 2: Build and push frontend Docker image
echo "📦 Building frontend Docker image..."
cd frontend
docker build -t ${ECR_FRONTEND_REPO}:latest .
docker tag ${ECR_FRONTEND_REPO}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND_REPO}:latest

echo "📤 Pushing frontend image to ECR..."
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
  --region ${AWS_REGION}

aws ecs register-task-definition \
  --cli-input-json file://deployment/aws/ecs-frontend-task-definition.json \
  --region ${AWS_REGION}

# Step 4: Update ECS services
echo "🔄 Updating ECS services..."
aws ecs update-service \
  --cluster ${ECS_CLUSTER} \
  --service txtai-rag-backend-service \
  --force-new-deployment \
  --region ${AWS_REGION} > /dev/null

aws ecs update-service \
  --cluster ${ECS_CLUSTER} \
  --service txtai-rag-frontend-service \
  --force-new-deployment \
  --region ${AWS_REGION} > /dev/null

echo "✅ Deployment complete!"
echo "📊 Monitor deployment status:"
echo "   aws ecs describe-services --cluster ${ECS_CLUSTER} --services txtai-rag-backend-service txtai-rag-frontend-service --region ${AWS_REGION}"


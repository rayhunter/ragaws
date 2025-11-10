#!/bin/bash
# AWS Setup Helper Script
# This script helps configure AWS credentials for the txtai RAG deployment

set -e

echo "🔐 AWS Credentials Setup Helper"
echo "================================"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed."
    echo "   Install it: https://aws.amazon.com/cli/"
    exit 1
fi

echo "✅ AWS CLI is installed"
echo ""

# Check current configuration
echo "Current AWS Configuration:"
aws configure list
echo ""

# Test credentials
echo "Testing AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ AWS credentials are valid!"
    echo ""
    aws sts get-caller-identity
else
    echo "❌ AWS credentials are invalid or expired"
    echo ""
    echo "To fix this, run one of the following:"
    echo ""
    echo "1. Reconfigure AWS CLI:"
    echo "   aws configure"
    echo ""
    echo "2. If using AWS SSO:"
    echo "   aws sso login --profile YOUR_PROFILE"
    echo ""
    echo "3. If using temporary credentials:"
    echo "   export AWS_ACCESS_KEY_ID=your_key"
    echo "   export AWS_SECRET_ACCESS_KEY=your_secret"
    echo "   export AWS_SESSION_TOKEN=your_token  # if using temporary credentials"
    echo ""
    echo "4. Check your ~/.aws/credentials file:"
    echo "   cat ~/.aws/credentials"
    echo ""
    exit 1
fi

echo ""
echo "🚀 Ready to create ECR repositories!"
echo ""
read -p "Create ECR repositories now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating ECR repositories..."
    
    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    AWS_REGION=$(aws configure get region || echo "us-east-1")
    
    echo "Account ID: $AWS_ACCOUNT_ID"
    echo "Region: $AWS_REGION"
    echo ""
    
    # Create backend repository
    echo "Creating txtai-rag-backend repository..."
    if aws ecr describe-repositories --repository-names txtai-rag-backend --region $AWS_REGION &> /dev/null; then
        echo "✅ Repository txtai-rag-backend already exists"
    else
        aws ecr create-repository \
            --repository-name txtai-rag-backend \
            --region $AWS_REGION \
            --image-scanning-configuration scanOnPush=true \
            --encryption-configuration encryptionType=AES256
        echo "✅ Created txtai-rag-backend repository"
    fi
    
    # Create frontend repository
    echo "Creating txtai-rag-frontend repository..."
    if aws ecr describe-repositories --repository-names txtai-rag-frontend --region $AWS_REGION &> /dev/null; then
        echo "✅ Repository txtai-rag-frontend already exists"
    else
        aws ecr create-repository \
            --repository-name txtai-rag-frontend \
            --region $AWS_REGION \
            --image-scanning-configuration scanOnPush=true \
            --encryption-configuration encryptionType=AES256
        echo "✅ Created txtai-rag-frontend repository"
    fi
    
    echo ""
    echo "✅ ECR repositories created successfully!"
    echo ""
    echo "Repository URIs:"
    echo "  Backend:  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/txtai-rag-backend"
    echo "  Frontend: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/txtai-rag-frontend"
fi


# AWS Credentials Troubleshooting Guide

## Issue: Invalid Security Token

The error "The security token included in the request is invalid" typically means:

1. **Temporary credentials expired** - If using temporary credentials (STS), they expire after a set time
2. **Missing session token** - Temporary credentials require `AWS_SESSION_TOKEN`
3. **Invalid credentials** - Access key or secret key is incorrect

## Solutions

### Option 1: If Using AWS SSO

```bash
# Login to AWS SSO
aws sso login --profile YOUR_PROFILE

# Or configure SSO profile
aws configure sso
```

### Option 2: If Using Temporary Credentials (STS)

Temporary credentials require three environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_SESSION_TOKEN=your_session_token  # Required for temporary credentials!
export AWS_DEFAULT_REGION=us-east-1
```

### Option 3: Configure Permanent Credentials

```bash
# Run AWS configure
aws configure

# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

### Option 4: Check Current Credentials

```bash
# View current credentials
aws configure list

# Test credentials
aws sts get-caller-identity

# View credentials file
cat ~/.aws/credentials
```

### Option 5: Use AWS Profiles

If you have multiple AWS accounts:

```bash
# List profiles
aws configure list-profiles

# Use specific profile
export AWS_PROFILE=your-profile-name

# Or use --profile flag
aws ecr create-repository --repository-name txtai-rag-backend --region us-east-1 --profile your-profile
```

## Quick Fix Script

Run the helper script:

```bash
cd deployment/aws
./setup-ecr.sh
```

This script will:
- Check if AWS CLI is installed
- Verify credentials are valid
- Create ECR repositories if credentials are working

## After Fixing Credentials

Once your credentials are valid, create the ECR repositories:

```bash
# Create backend repository
aws ecr create-repository \
  --repository-name txtai-rag-backend \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true

# Create frontend repository  
aws ecr create-repository \
  --repository-name txtai-rag-frontend \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true
```

## Verify Setup

```bash
# List repositories
aws ecr describe-repositories --region us-east-1

# Get login token (for Docker)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

